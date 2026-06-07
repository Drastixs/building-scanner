# Building Device Scanner

A command-line OSINT tool: give it a company URL and it prints the network
devices in that organisation's IP space — cameras, RFID/access-control readers,
building-automation services, and exposed remote access — each with an `IP:port`,
a reachable URL, and a Shodan host link. Results are cached per building so you
can re-query without rescanning.

All Shodan/RDAP traffic is forced through a Surfshark WireGuard VPN; the scan
aborts before sending anything if the tunnel isn't the active default route, so
your real IP is never exposed. It is **passive** — it reads Shodan's index and
public certificate-transparency logs, and never probes the devices it finds.

---

## Setup

Requires [`uv`](https://docs.astral.sh/uv/) and a Shodan API key.

```bash
uv sync
```

Put your key in `../../.env` (one level above the repo root, never committed):

```
SHODAN_API_KEY=your_key_here
```

Connect Surfshark (full-tunnel WireGuard) before scanning. The preflight checks
that the default route is the `surfshark_wg` interface and aborts otherwise.

---

## Usage

```bash
uv run python scan.py <company-url>          # scan, print, and cache
uv run python scan.py <company-url> --id hq  # cache under a custom building id
uv run python scan.py list                   # list cached buildings
uv run python scan.py show <building-id>      # reprint a cached result (no rescan)
```

### Example

```bash
uv run python scan.py mit.edu
```

```
[*] VPN preflight…
[+] Tunnelled via surfshark_wg → egress 138.199.29.143
[*] Attributing IP space for mit.edu (CT logs → RDAP)…
[+] org='Massachusetts Institute of Technology'  cidrs=['18.0.0.0/11', '128.30.0.0/16', '128.52.0.0/16']
[*] Scanning: camera…
[*] Scanning: access_control…
[*] Scanning: building_service…

18 device(s) for mit.edu (org: Massachusetts Institute of Technology):

CATEGORY         PRODUCT                  URL                          SHODAN
-----------------------------------------------------------------------------
camera           -                        rtsp://18.18.134.16:554      https://www.shodan.io/host/18.18.134.16
camera           -                        rtsp://18.27.130.103:554     https://www.shodan.io/host/18.27.130.103
remote_access    Remote Desktop Protocol  18.25.5.154:3389             https://www.shodan.io/host/18.25.5.154
...
```

---

## How it works

1. **VPN preflight** — confirm the default route egresses via the `surfshark_wg`
   tunnel (and the egress IP isn't your ISP). Abort if not.
2. **Attribution** — the apex domain is usually CDN-fronted, so resolving it gives
   the CDN's IP, not the org's. Instead we enumerate subdomains from certificate
   transparency (CertSpotter + crt.sh) plus an infrastructure wordlist, resolve
   them, look each IP up via **RDAP** (`rdap.arin.net`, follows redirects to other
   RIRs), drop CDN/cloud-owned blocks, and keep the dominant org's real netblocks.
3. **Discovery** — run the `DEVICE_QUERIES` fingerprint list over Shodan against
   those CIDRs, deduped by `IP:port`.
4. **Classify** — label each device by its actual signal (port/product), not just
   which query found it, so e.g. an RDP host caught by a broad query isn't
   mislabelled a camera.
5. **Cache** — write to `camera_index.json` (gitignored), keyed by building id.

### Device categories

The fingerprint list lives in `DEVICE_QUERIES` in `scan.py` and is easy to extend.

| Category | Looks for |
|---|---|
| `camera` | RTSP:554, Hikvision / Dahua / Axis, screenshot-enabled hosts |
| `access_control` | HID VertX, Lenel, Genetec, Honeywell, RFID |
| `building_service` | BACnet (47808), Modbus (502) |
| `remote_access` | exposed RDP (3389) / VNC (assigned at classification time) |

---

## Files

```
scan.py            the whole tool (attribution + discovery + cache + CLI)
vpn.py             VPN preflight (route check) + httpx client
pyproject.toml     deps: httpx, python-dotenv
camera_index.json  scan cache (gitignored)
```

---

## Choosing a target

Works best on organisations that **own their IP space** and whose subdomains
resolve into it (universities, large enterprises). CDN-fully-fronted sites with no
resolvable org subdomains will return no netblocks. `CertSpotter`'s free tier is
rate-limited (a few queries/hour without a key); when it's throttled, attribution
falls back to crt.sh and the infrastructure wordlist.

---

## Security & scope

- VPN-gated: no request leaves outside the WireGuard tunnel.
- Passive: reads Shodan + CT logs only; never connects to or probes found devices.
- Intended for authorised security research and testing only.
