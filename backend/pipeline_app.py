#!/usr/bin/env python3
"""Blueprint Pipeline API — add a building by address, discover its public blueprints
with the local OpenAI agent (A0), ingest them into a 3D model (A1), and serve the
graph + traversal data for client rendering.

    uv run uvicorn pipeline_app:app --port 8001        # serve
    uv run uvicorn pipeline_app:app --reload           # dev

This is a separate app from api.py (the VPN-gated device scanner, Phase C); both expose
a /buildings surface for different concerns, so they run as separate processes/ports.

Flow:
    POST /buildings {address}        → match internal DB, report enriched?
    POST /buildings/{id}/discover    → A0 (subprocess: planning-scout OpenAI agent)
    GET  /buildings/{id}/discover    → poll phase + docs_found
    POST /buildings/{id}/ingest      → A1 (in-proc: extract→graph→building→routes)
    GET  /buildings/{id}/ingest      → poll docs_processed/total + low_confidence_floors
    GET  /buildings/{id}/graph       → {nodes, edges, floors}   (3D render)
    GET  /buildings/{id}/routes      → {floors, connectors, rooms, entrances, edges}
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

import store
from routers import buildings


@asynccontextmanager
async def lifespan(app: FastAPI):
    store.load_jobs()  # recover job registry; mark interrupted runs failed
    yield


app = FastAPI(
    title="Building Blueprint Pipeline API",
    version="1.0",
    description="Address → blueprint discovery (A0) → 3D ingestion (A1) → graph/routes.",
    lifespan=lifespan,
)
app.include_router(buildings.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "buildings": len(store.list_slugs())}
