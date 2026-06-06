from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import store
from models import BuildingScan, PhaseStatus

router = APIRouter(prefix="/buildings", tags=["buildings"])


class StartScanRequest(BaseModel):
    building_id: str


@router.post("", status_code=201)
def start_scan(body: StartScanRequest):
    """Register a building and kick off the evaluation pipeline."""
    bid = body.building_id.strip().lower()

    if bid in store.scans:
        raise HTTPException(status_code=409, detail=f"Scan already exists for '{bid}'")

    scan = BuildingScan(
        building_id=bid,
        created_at=datetime.now(timezone.utc).isoformat(),
        overall_status=PhaseStatus.running,
    )
    store.scans[bid] = scan

    # TODO: kick off background pipeline here
    return scan


@router.get("")
def list_scans():
    """List all registered buildings and their overall status."""
    return [
        {
            "building_id": s.building_id,
            "overall_status": s.overall_status,
            "created_at": s.created_at,
        }
        for s in store.scans.values()
    ]


@router.get("/{building_id}/status")
def get_status(building_id: str):
    """Full status of a building scan across all phases."""
    scan = _get_or_404(building_id)
    return scan


@router.get("/{building_id}/phase/a0")
def phase_a0(building_id: str):
    """Phase A0 — schematic discovery status."""
    return _get_or_404(building_id).phase_a0


@router.get("/{building_id}/phase/a1")
def phase_a1(building_id: str):
    """Phase A1 — schematic ingestion and 3D mapping status."""
    return _get_or_404(building_id).phase_a1


@router.get("/{building_id}/phase/b")
def phase_b(building_id: str):
    """Phase B — people research status."""
    return _get_or_404(building_id).phase_b


@router.get("/{building_id}/people")
def get_people(building_id: str):
    """People found for a building (from Phase B)."""
    return _get_or_404(building_id).phase_b.people


@router.get("/{building_id}/phase/c")
def phase_c(building_id: str):
    """Phase C — OSINT scan status."""
    return _get_or_404(building_id).phase_c


@router.get("/{building_id}/phase/d")
def phase_d(building_id: str):
    """Phase D — simulation status."""
    return _get_or_404(building_id).phase_d


def _get_or_404(building_id: str) -> BuildingScan:
    scan = store.scans.get(building_id.lower())
    if not scan:
        raise HTTPException(
            status_code=404, detail=f"No scan found for '{building_id}'"
        )
    return scan
