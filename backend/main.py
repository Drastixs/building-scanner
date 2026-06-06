from fastapi import FastAPI
from routers import buildings

app = FastAPI(title="Building Scanner API")

app.include_router(buildings.router)


@app.get("/health")
def health():
    return {"status": "ok"}
