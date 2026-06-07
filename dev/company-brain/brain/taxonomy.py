"""
Central cue taxonomy for the company brain.

Single source of truth for:
  - the legal set of cue TAGS profiles/lessons may use
  - ENABLES edges (cue -> attack it makes possible)
  - DISCONFIRMS edges (cue -> hypothesis it kills)

Profiles validate their cues against CUES at load time, so a misspelled tag is a
load error (not a silent empty `why` at recall time). Eng-review decision #7.

Only 2 edge types are exercised in v1 (ENABLES / DISCONFIRMS); the other 5
taxonomy edges from the methodology are deferred (see design "NOT in Scope").
"""

# --- cue tags -------------------------------------------------------------

# Cues that OPEN attack surface
CUES_ENABLING = {
    "hid_maxiprox",  # 125 kHz prox reader, cloneable
    "herd_entry",  # crowd flows in together at peak
    "no_turnstile",  # lobby has no physical mantrap
    "conference_day",  # event swells the lobby with unbadged guests
    "loading_bay",  # goods-in entrance, lower scrutiny
    "no_manifest_check",  # deliveries not checked against a manifest
    "it_job_posting",  # public IT contractor req -> pretext cover
    "open_floor",  # no internal segmentation past reception
    "no_visitor_escort",  # visitors roam unescorted
    "hi_vis_invisible",  # hi-vis / maintenance dress is culturally ignored
    "shared_stairwell",  # public-area stairwell reaches secure floors
}

# Cues that CLOSE attack surface (high-diagnosticity disconfirmers)
CUES_DISCONFIRMING = {
    "turnstile",  # physical mantrap at lobby
    "osdp_secure",  # OSDP Secure Channel readers (no Wiegand replay)
    "visitor_escort_strict",  # visitors escorted at all times
    "manifest_checked",  # deliveries verified against a manifest
    "appointments_verified",  # reception live-verifies appointments
}

CUES = CUES_ENABLING | CUES_DISCONFIRMING

# --- edges ----------------------------------------------------------------

# cue -> attack it ENABLES
ENABLES = {
    "hid_maxiprox": "clone_badge",
    "herd_entry": "tailgate",
    "no_turnstile": "tailgate",
    "conference_day": "blend_tailgate",
    "loading_bay": "delivery_pretext",
    "no_manifest_check": "delivery_pretext",
    "it_job_posting": "it_contractor_pretext",
    "open_floor": "roam_unescorted",
    "no_visitor_escort": "roam_unescorted",
    "hi_vis_invisible": "maintenance_pretext",
    "shared_stairwell": "stairwell_cascade",
}

# cue -> hypothesis/attack it DISCONFIRMS
DISCONFIRMS = {
    "turnstile": "tailgate",
    "osdp_secure": "clone_badge",
    "visitor_escort_strict": "it_contractor_pretext",
    "manifest_checked": "delivery_pretext",
    "appointments_verified": "it_contractor_pretext",
}


class UnknownCueError(ValueError):
    """Raised when a profile/lesson uses a cue tag not in the taxonomy."""


def validate_cues(cues, where="profile"):
    """Raise UnknownCueError if any cue is not in the taxonomy. Returns cues."""
    unknown = [c for c in cues if c not in CUES]
    if unknown:
        raise UnknownCueError(
            f"{where} uses unknown cue tag(s) {unknown}; "
            f"add them to brain/taxonomy.py or fix the spelling"
        )
    return cues
