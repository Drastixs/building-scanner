#!/usr/bin/env python3
"""
find_ranges.py — given an organization name, find the IPv4/IPv6 CIDR ranges
registered or announced to it, deduped into a ready-to-use blocklist.

Sources (all free, no API key):
  1. BGPView        (api.bgpview.io)    — global; BGP-routed prefixes + RIR name matches
  2. ARIN Whois-RWS (whois.arin.net)    — North America; direct allocations AND
                                          detailed SWIP reassignments (the Tier-2
                                          "business with a static block" case)
  3. RIPE DB search (rest.db.ripe.net)  — Europe / Middle East; allocations + SWIP

Usage:
  ./find_ranges.py "Acme Corporation"
  ./find_ranges.py "Acme Corp" --cidrs-only > acme-blocklist.txt
  ./find_ranges.py "Acme Corp" --json
  ./find_ranges.py "Acme Corp" --v4-only           # skip IPv6

Notes / honest limits:
  * Only finds STATIC / OWNED space that someone registered. Dynamic broadband
    (most small offices, all apartments) is invisible — it belongs to the ISP.
  * The registered address is the registrant's admin address — usually right,
    but can be an HQ or an ISP regional office rather than the exact building.
  * Simple SWIP reassignments (ARIN "customer" records, no Org) can't be reversed
    by name via the public API; if you suspect one, run `whois <a-known-ip>` by hand.
  * Name matching is fuzzy. Eyeball the NAME/ADDRESS columns before trusting a CIDR.
"""

import argparse
import datetime
import ipaddress
import json
import logging
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

TIMEOUT = 25
UA = "find-ranges/1.0 (ip-range lookup)"
MAX_ASNS = 25  # safety cap on per-ASN prefix expansion

# Everything (run log + saved results) lands in ./ip-search/ next to this script.
OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ip-search")
log = logging.getLogger("find_ranges")


def setup_logging(verbose=False):
    """Log to ./ip-search/find_ranges.log (full debug) and to stderr (info)."""
    os.makedirs(OUTDIR, exist_ok=True)
    log.setLevel(logging.DEBUG)
    fh = logging.FileHandler(os.path.join(OUTDIR, "find_ranges.log"))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s  %(levelname)-7s %(message)s"))
    ch = logging.StreamHandler(sys.stderr)
    ch.setLevel(logging.DEBUG if verbose else logging.INFO)
    ch.setFormatter(logging.Formatter("%(message)s"))
    log.handlers[:] = [fh, ch]


def _slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "org"


def _get(url, accept="application/json"):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read()


def _get_json(url):
    return json.loads(_get(url).decode("utf-8", "replace"))


def _as_list(x):
    """ARIN/RIPE JSON collapses single-element arrays to objects. Normalize."""
    if x is None:
        return []
    return x if isinstance(x, list) else [x]


class Results:
    def __init__(self, drop_v6=False):
        self.rows = {}  # cidr -> (source, name, address)
        self.drop_v6 = drop_v6

    def add_cidr(self, cidr, source, name="", address=""):
        try:
            net = ipaddress.ip_network(cidr, strict=False)
        except ValueError:
            return
        if self.drop_v6 and net.version == 6:
            return
        key = str(net)
        # keep the most descriptive row if we see a dupe
        if key not in self.rows or (not self.rows[key][1] and name):
            self.rows[key] = (source, name.strip(), address.strip())

    def add_range(self, start, end, source, name="", address=""):
        try:
            a = ipaddress.ip_address(start.strip())
            b = ipaddress.ip_address(end.strip())
        except ValueError:
            return
        for net in ipaddress.summarize_address_range(a, b):
            self.add_cidr(str(net), source, name, address)


# ---------------------------------------------------------------- BGPView ----
def query_bgpview(org, res, want_v6=True):
    before = len(res.rows)
    log.info("[bgpview] querying api.bgpview.io ...")
    try:
        data = _get_json(
            "https://api.bgpview.io/search?query_term=" + urllib.parse.quote(org)
        )
    except Exception as e:
        log.warning("[bgpview] search failed: %s", e)
        return
    d = data.get("data", {})

    # direct prefix matches
    for fam, flag in (("ipv4_prefixes", True), ("ipv6_prefixes", want_v6)):
        if not flag:
            continue
        for p in d.get(fam, []):
            res.add_cidr(
                p.get("prefix", ""),
                "bgpview",
                p.get("description") or p.get("name") or "",
                "",
            )

    # expand each matched ASN into all its announced prefixes
    asns = [a.get("asn") for a in d.get("asns", []) if a.get("asn")]
    if len(asns) > MAX_ASNS:
        log.warning(
            "[bgpview] %d ASNs matched; expanding only first %d", len(asns), MAX_ASNS
        )
    for asn in asns[:MAX_ASNS]:
        log.debug("[bgpview] expanding AS%s prefixes", asn)
        try:
            pd = _get_json(f"https://api.bgpview.io/asn/{asn}/prefixes")["data"]
        except Exception as e:
            log.warning("[bgpview] AS%s prefixes failed: %s", asn, e)
            continue
        for fam, flag in (("ipv4_prefixes", True), ("ipv6_prefixes", want_v6)):
            if not flag:
                continue
            for p in pd.get(fam, []):
                res.add_cidr(
                    p.get("prefix", ""),
                    f"bgpview/AS{asn}",
                    p.get("description") or p.get("name") or "",
                    "",
                )
        time.sleep(0.4)  # be polite to a free API
    log.info("[bgpview] +%d ranges", len(res.rows) - before)


# ------------------------------------------------------------------- ARIN ----
def query_arin(org, res):
    before = len(res.rows)
    log.info("[arin] querying whois.arin.net ...")
    try:
        data = _get_json(
            "https://whois.arin.net/rest/orgs;name="
            + urllib.parse.quote(org, safe="")
            + "*"
        )
    except urllib.error.HTTPError as e:
        if e.code == 404:
            log.info("[arin] no matching orgs (404)")
            return
        log.warning("[arin] org search failed: %s", e)
        return
    except Exception as e:
        log.warning("[arin] org search failed: %s", e)
        return

    orgs = _as_list(data.get("orgs", {}).get("orgRef"))
    log.info("[arin] %d matching org(s)", len(orgs))
    for o in orgs:
        handle = o.get("@handle")
        name = o.get("@name", "")
        if not handle:
            continue
        log.debug("[arin] org %s (%s) -> nets", handle, name)
        try:
            nets = _get_json(f"https://whois.arin.net/rest/org/{handle}/nets")
        except Exception as e:
            log.warning("[arin] nets for %s failed: %s", handle, e)
            continue
        for n in _as_list(nets.get("nets", {}).get("netRef")):
            start = n.get("@startAddress")
            end = n.get("@endAddress")
            if start and end:
                res.add_range(start, end, "arin", name, "")
        time.sleep(0.2)
    log.info("[arin] +%d ranges", len(res.rows) - before)


# ------------------------------------------------------------------- RIPE ----
def query_ripe(org, res, want_v6=True):
    before = len(res.rows)
    log.info("[ripe] querying rest.db.ripe.net ...")
    types = ["inetnum", "inet6num"] if want_v6 else ["inetnum"]
    tf = "".join("&type-filter=" + t for t in types)
    url = (
        "https://rest.db.ripe.net/search.json?flags=no-referenced"
        "&query-string=" + urllib.parse.quote(org) + tf
    )
    try:
        data = _get_json(url)
    except Exception as e:
        log.warning("[ripe] search failed: %s", e)
        return
    for obj in _as_list(data.get("objects", {}).get("object")):
        otype = obj.get("type")
        pk = obj.get("primary-key", {}).get("attribute", [])
        rng = next(
            (a.get("value") for a in pk if a.get("name") in ("inetnum", "inet6num")),
            None,
        )
        if not rng:
            continue
        # pull a descriptive name (netname/descr/org) from attributes
        attrs = obj.get("attributes", {}).get("attribute", [])
        name = next(
            (
                a.get("value")
                for a in attrs
                if a.get("name") in ("netname", "descr", "org")
            ),
            "",
        )
        if otype == "inet6num":
            res.add_cidr(rng.strip(), "ripe", name, "")
        elif " - " in rng:
            start, end = rng.split(" - ", 1)
            res.add_range(start, end, "ripe", name, "")
        else:
            res.add_cidr(rng.strip(), "ripe", name, "")
    log.info("[ripe] +%d ranges", len(res.rows) - before)


# ------------------------------------------------------------------ main ----
def main():
    ap = argparse.ArgumentParser(description="Find an org's registered IP CIDR ranges.")
    ap.add_argument("org", help='organization name, e.g. "Acme Corporation"')
    ap.add_argument(
        "--cidrs-only",
        action="store_true",
        help="print only collapsed CIDRs, one per line (for a blocklist)",
    )
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument("--v4-only", action="store_true", help="skip IPv6")
    ap.add_argument("--no-bgpview", action="store_true")
    ap.add_argument("--no-arin", action="store_true")
    ap.add_argument("--no-ripe", action="store_true")
    ap.add_argument(
        "--no-save",
        action="store_true",
        help="don't write a results file into ./ip-search/",
    )
    ap.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="show debug-level logging on the console",
    )
    args = ap.parse_args()

    setup_logging(args.verbose)
    want_v6 = not args.v4_only
    res = Results(drop_v6=args.v4_only)

    log.info("=== search: %r (v6=%s) ===", args.org, want_v6)
    if not args.no_bgpview:
        query_bgpview(args.org, res, want_v6)
    if not args.no_arin:
        query_arin(args.org, res)
    if not args.no_ripe:
        query_ripe(args.org, res, want_v6)

    if not res.rows:
        log.error(
            "No registered ranges found. The org likely has no owned/static "
            "space (dynamic broadband only), or the name didn't match WHOIS "
            "records. Try a shorter/legal-entity form of the name."
        )
        sys.exit(1)

    nets = [ipaddress.ip_network(c) for c in res.rows]
    v4 = ipaddress.collapse_addresses(n for n in nets if n.version == 4)
    v6 = ipaddress.collapse_addresses(n for n in nets if n.version == 6)
    collapsed = [str(n) for n in v4] + [str(n) for n in v6]
    log.info(
        "total: %d raw ranges -> %d collapsed CIDRs", len(res.rows), len(collapsed)
    )

    if not args.no_save:
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        path = os.path.join(OUTDIR, f"{_slug(args.org)}-{ts}.cidrs.txt")
        with open(path, "w") as fh:
            fh.write("\n".join(collapsed) + "\n")
        log.info("saved %d CIDRs -> %s", len(collapsed), path)

    if args.cidrs_only:
        print("\n".join(collapsed))
    elif args.json:
        print(
            json.dumps(
                {
                    "org": args.org,
                    "collapsed_cidrs": collapsed,
                    "raw": [
                        {"cidr": c, "source": s, "name": nm, "address": ad}
                        for c, (s, nm, ad) in sorted(res.rows.items())
                    ],
                },
                indent=2,
            )
        )
    else:
        print(f"{'CIDR':<22} {'SOURCE':<16} NAME")
        print("-" * 70)

        def _sortkey(kv):
            n = ipaddress.ip_network(kv[0])
            return (n.version, n)

        for c, (s, nm, ad) in sorted(res.rows.items(), key=_sortkey):
            print(f"{c:<22} {s:<16} {nm[:40]}")
        print(f"\n{len(res.rows)} raw ranges → {len(collapsed)} collapsed CIDRs")
        print("Collapsed (use these for blocking):")
        for c in collapsed:
            print(f"  {c}")


if __name__ == "__main__":
    main()
