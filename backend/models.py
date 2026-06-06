from enum import Enum
from pydantic import BaseModel


class PhaseStatus(str, Enum):
    pending = "pending"
    running = "running"
    complete = "complete"
    failed = "failed"
    skipped = "skipped"


# Phase A0 — Schematic Discovery
class PhaseA0(BaseModel):
    status: PhaseStatus = PhaseStatus.pending
    documents_found: int = 0
    documents: list[str] = []
    sources_searched: list[str] = []


# Phase A1 — Schematic Ingestion + 3D Mapping
class BuildingFeatures(BaseModel):
    stairs: list[str] = []
    lifts: list[str] = []
    entry_points: list[str] = []
    restricted_zones: list[str] = []


class PhaseA1(BaseModel):
    status: PhaseStatus = PhaseStatus.pending
    documents_total: int = 0
    documents_processed: int = 0
    features: BuildingFeatures = BuildingFeatures()


# Phase B — People Research
class Person(BaseModel):
    name: str
    role: str | None = None
    source: str | None = None
    enriched: bool = False
    linkedin_url: str | None = None
    email: str | None = None


class PhaseBSubStage(str, Enum):
    website_scout = "website_scout"
    linkedin_search = "linkedin_search"
    enrichment = "enrichment"


class PhaseB(BaseModel):
    status: PhaseStatus = PhaseStatus.pending
    current_stage: PhaseBSubStage | None = None
    website_indexed: bool = False
    website_pages_found: int = 0
    people: list[Person] = []
    sources_searched: list[str] = []


# Phase C — OSINT
class PhaseCSubStage(str, Enum):
    camera_scan = "camera_scan"
    access_control_scan = "access_control_scan"
    services_scan = "services_scan"


class PhaseC(BaseModel):
    status: PhaseStatus = PhaseStatus.pending
    current_stage: PhaseCSubStage | None = None
    cameras_found: list[str] = []
    rfid_systems: list[str] = []
    exposed_services: list[dict] = []


# Phase D — Simulation
class SimulationScenario(BaseModel):
    name: str
    approach: str
    outcome: str | None = None
    notes: str | None = None


class PhaseD(BaseModel):
    status: PhaseStatus = PhaseStatus.pending
    scenarios_total: int = 0
    scenarios_complete: int = 0
    scenarios: list[SimulationScenario] = []


# Top-level scan
class BuildingScan(BaseModel):
    building_id: str
    created_at: str
    overall_status: PhaseStatus = PhaseStatus.pending
    phase_a0: PhaseA0 = PhaseA0()
    phase_a1: PhaseA1 = PhaseA1()
    phase_b: PhaseB = PhaseB()
    phase_c: PhaseC = PhaseC()
    phase_d: PhaseD = PhaseD()
