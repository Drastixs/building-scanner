"""Blueprint pipeline routes: add a building by address, run discovery (A0) and
ingestion (A1) as pollable background jobs, then serve the 3D graph + traversal graph.

    POST /buildings                 add by address (fuzzy-match the internal DB)
    GET  /buildings                 list known buildings + status
    GET  /buildings/{id}            one building, full record + phase status
    POST /buildings/{id}/discover   run A0 (download blueprints)        202 / 409 / 200-noop
    GET  /buildings/{id}/discover   poll A0: phase, docs_found
    POST /buildings/{id}/ingest     run A1 (build 3D model)             202 / 409 / 422
    GET  /buildings/{id}/ingest     poll A1: docs_processed/total, low_confidence_floors
    GET  /buildings/{id}/graph      building.json {nodes, edges, floors}   (3D render)
    GET  /buildings/{id}/routes     routes.json  {floors, connectors, ...} (traversal)
"""

import json

from fastapi import APIRouter, BackgroundTasks, HTTPException

import address as address_mod
import store
from models import AddBuildingRequest, AddBuildingResponse
from workers.discover import run_discover
from workers.ingest import run_ingest

router = APIRouter(prefix="/buildings", tags=["buildings"])


def _require(slug: str) -> str:
    if not store.exists(slug):
        raise HTTPException(404, f"No building {slug!r}")
    return slug


# ── Add + list ──────────────────────────────────────────────────────────────────
@router.post("", status_code=201, response_model=AddBuildingResponse)
def add_building(body: AddBuildingRequest):
    """Match the address against the internal building DB (or mint a new slug), record
    it, and report whether it's already enriched (has blueprint PDFs)."""
    try:
        m = address_mod.match_or_create(body.address)
    except ValueError as e:
        raise HTTPException(422, str(e))

    slug = m["slug"]
    if store.read_meta(slug).get("created_at"):
        store.write_meta(slug, address=body.address)
    else:
        store.write_meta(slug, address=body.address, created_at=store.now())

    return AddBuildingResponse(
        id=slug,
        created=m["created"],
        matched_existing=m["matched_existing"],
        match_score=m["score"],
        enriched=store.enriched(slug),
        doc_count=store.doc_count(slug),
    )


@router.get("")
def list_buildings():
    return [
        {
            "id": slug,
            "enriched": store.enriched(slug),
            "doc_count": store.doc_count(slug),
            "overall_status": store.overall_status(slug),
        }
        for slug in store.list_slugs()
    ]


@router.get("/{slug}")
def get_building(slug: str):
    _require(slug)
    return {
        "id": slug,
        "address": store.read_meta(slug).get("address"),
        "enriched": store.enriched(slug),
        "doc_count": store.doc_count(slug),
        "overall_status": store.overall_status(slug),
        "discover": store.get_job(slug, "discover"),
        "ingest": store.get_job(slug, "ingest"),
        "has_graph": (store.building_dir(slug) / "building.json").exists(),
        "has_routes": (store.building_dir(slug) / "routes.json").exists(),
    }


# ── A0: discover ──────────────────────────────────────────────────────────────────
@router.post("/{slug}/discover", status_code=202)
def start_discover(slug: str, bg: BackgroundTasks):
    _require(slug)
    if store.enriched(slug):
        return {"status": "already_enriched", "doc_count": store.doc_count(slug)}
    if store.is_running(slug, "discover"):
        raise HTTPException(409, "discovery already running for this building")

    address = store.read_meta(slug).get("address")
    if not address:
        raise HTTPException(422, "no address on record — POST /buildings first")

    job = store.set_job(
        slug, "discover", status="running", started_at=store.now(), error=None
    )
    bg.add_task(run_discover, slug, address)
    return {
        "job_id": f"{slug}:discover",
        "building": slug,
        "phase": "discover",
        "status": job["status"],
    }


@router.get("/{slug}/discover")
def discover_status(slug: str):
    _require(slug)
    job = store.get_job(slug, "discover") or {"status": "pending"}
    prog = {}
    pf = store.building_dir(slug) / "progress.json"
    if pf.exists():
        try:
            prog = json.loads(pf.read_text())
        except (json.JSONDecodeError, OSError):
            prog = {}
    return {
        "status": job.get("status", "pending"),
        "phase": prog.get("phase"),
        "phase_index": prog.get("phase_index"),
        "phase_total": prog.get("phase_total"),
        "note": prog.get("note"),
        # max(): the agent's self-report vs. what actually landed on disk — trust the higher.
        "docs_found": max(prog.get("docs_found", 0), store.doc_count(slug)),
        "error": job.get("error"),
    }


# ── A1: ingest ────────────────────────────────────────────────────────────────────
@router.post("/{slug}/ingest", status_code=202)
def start_ingest(slug: str, bg: BackgroundTasks):
    _require(slug)
    if store.doc_count(slug) == 0:
        raise HTTPException(422, "no blueprint PDFs — run /discover first")
    if store.is_running(slug, "ingest"):
        raise HTTPException(409, "ingestion already running for this building")

    job = store.set_job(
        slug, "ingest", status="running", started_at=store.now(), error=None
    )
    bg.add_task(run_ingest, slug)
    return {
        "job_id": f"{slug}:ingest",
        "building": slug,
        "phase": "ingest",
        "status": job["status"],
    }


@router.get("/{slug}/ingest")
def ingest_status(slug: str):
    _require(slug)
    job = store.get_job(slug, "ingest") or {"status": "pending"}
    return {
        "status": job.get("status", "pending"),
        "docs_processed": job.get("docs_processed", 0),
        "docs_total": job.get("docs_total", store.doc_count(slug)),
        "current_stage": job.get("current_stage"),
        "floors_extracted": job.get("floors_extracted", 0),
        "low_confidence_floors": job.get("low_confidence_floors", []),
        "skipped_sheets": job.get("skipped_sheets", []),
        "error": job.get("error"),
    }


# ── Graph + routes ────────────────────────────────────────────────────────────────
def _serve_json(slug: str, filename: str):
    _require(slug)
    f = store.building_dir(slug) / filename
    if not f.exists():
        raise HTTPException(404, "not_ingested")
    return json.loads(f.read_text())


@router.get("/{slug}/graph")
def get_graph(slug: str):
    """3D render data: {nodes, edges, floors}."""
    return _serve_json(slug, "building.json")


@router.get("/{slug}/routes")
def get_routes(slug: str):
    """Traversal skeleton: {floors, connectors, rooms, entrances, edges}."""
    return _serve_json(slug, "routes.json")
