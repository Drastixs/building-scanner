"""Request/response models for the blueprint pipeline API.

Status payloads (discover/ingest progress, graph, routes) are assembled as plain dicts
in the router because they're read live off disk and vary in shape; the pydantic models
here cover the typed request bodies and the stable summary responses.
"""

from pydantic import BaseModel


class AddBuildingRequest(BaseModel):
    address: str


class BuildingSummary(BaseModel):
    id: str
    enriched: bool
    doc_count: int
    overall_status: str


class AddBuildingResponse(BaseModel):
    id: str
    created: bool
    matched_existing: bool
    match_score: float
    enriched: bool
    doc_count: int


class JobAccepted(BaseModel):
    job_id: str
    building: str
    phase: str
    status: str
