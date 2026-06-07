"""
Minimal per-building graph substrate (NetworkX).

Holds typed cue nodes (social / spatial / credential) with provenance, and the
only 2 edge types exercised in v1: ENABLES (cue -> attack) and DISCONFIRMS
(cue -> killed hypothesis), drawn straight from taxonomy.py. The graph lets each
specialist query its slice; it does NOT drive collide() (that is list-based).

The other 5 taxonomy edges and the weighted pathfinder are out of scope (design
"NOT in Scope").
"""

import networkx as nx

from . import taxonomy

# Which cues belong to which specialist's slice.
CUE_GRAPH = {
    # social
    "herd_entry": "social",
    "conference_day": "social",
    "no_visitor_escort": "social",
    "visitor_escort_strict": "social",
    "it_job_posting": "social",
    "hi_vis_invisible": "social",
    "appointments_verified": "social",
    # spatial
    "no_turnstile": "spatial",
    "turnstile": "spatial",
    "loading_bay": "spatial",
    "open_floor": "spatial",
    "shared_stairwell": "spatial",
    # credential
    "hid_maxiprox": "credential",
    "osdp_secure": "credential",
    "no_manifest_check": "credential",
    "manifest_checked": "credential",
}


def build_graph(profile: dict) -> nx.DiGraph:
    """Build a cue graph for one building profile with ENABLES/DISCONFIRMS edges."""
    g = nx.DiGraph()
    g.graph["building_id"] = profile["building_id"]
    for cue in profile.get("cues", []):
        g.add_node(
            cue,
            kind="cue",
            graph=CUE_GRAPH.get(cue, "unknown"),
            source=profile.get("name", "osint"),
            confidence=1.0,
        )
        if cue in taxonomy.ENABLES:
            attack = taxonomy.ENABLES[cue]
            g.add_node(attack, kind="attack")
            g.add_edge(cue, attack, rel="ENABLES")
        if cue in taxonomy.DISCONFIRMS:
            hyp = taxonomy.DISCONFIRMS[cue]
            g.add_node(hyp, kind="attack")
            g.add_edge(cue, hyp, rel="DISCONFIRMS")
    return g


def cues_for_graph(profile: dict, which: str) -> list:
    """Return the profile's cues that belong to a given specialist slice."""
    return [c for c in profile.get("cues", []) if CUE_GRAPH.get(c) == which]
