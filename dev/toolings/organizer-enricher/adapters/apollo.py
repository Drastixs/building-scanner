from __future__ import annotations
import os
import time
import httpx

APOLLO_URL = "https://api.apollo.io/v1/people/match"


async def apollo_adapter(name: str, email: str = "", company: str = "") -> dict:
    api_key = os.environ.get("APOLLO_API_KEY", "")
    if not api_key:
        return {
            "success": False,
            "fields_contributed": [],
            "error": "missing APOLLO_API_KEY",
        }

    parts = name.strip().split(maxsplit=1)
    first = parts[0] if parts else name
    last = parts[1] if len(parts) > 1 else ""

    payload = {
        "api_key": api_key,
        "first_name": first,
        "last_name": last,
        "email": email or None,
        "organization_name": company or None,
        "reveal_personal_emails": True,
    }

    t0 = time.monotonic()
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.post(APOLLO_URL, json=payload)
            r.raise_for_status()
            data = r.json().get("person") or {}
    except Exception as e:
        return {
            "success": False,
            "fields_contributed": [],
            "error": str(e),
            "latency_ms": int((time.monotonic() - t0) * 1000),
        }

    latency = int((time.monotonic() - t0) * 1000)
    if not data:
        return {"success": False, "fields_contributed": [], "latency_ms": latency}

    result: dict = {"success": True, "latency_ms": latency, "fields_contributed": []}

    def _set(key: str, value):
        if value:
            result[key] = value
            result["fields_contributed"].append(key)

    _set("full_name", data.get("name"))
    _set("primary_email", data.get("email"))
    _set("company", (data.get("organization") or {}).get("name"))
    _set("job_title", data.get("title"))
    _set("location", data.get("city"))
    _set("linkedin_url", data.get("linkedin_url"))
    _set("twitter_handle", data.get("twitter_url"))

    return result
