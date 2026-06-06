from __future__ import annotations
import asyncio
from datetime import datetime, timezone
from typing import Optional

from schema import (
    OrganizerProfile,
    IdentityFields,
    SocialFields,
    ProfessionalFields,
    SocialPresence,
    WebPresence,
    UKCompany,
    SourceProvenance,
    make_organizer_id,
    compute_confidence,
)

# Field resolution priority: first source with a non-null value wins
FIELD_PRIORITY = {
    "full_name": ["apollo", "linkedin", "twitter"],
    "primary_email": ["apollo", "website"],
    "company": ["apollo", "linkedin", "companies_house"],
    "job_title": ["apollo", "linkedin"],
    "location": ["apollo", "linkedin"],
    "linkedin_url": ["apollo", "linkedin"],
    "twitter_handle": ["twitter", "apollo"],
    "website_url": ["apollo", "serp", "linkedin"],
    "bio": ["linkedin", "website", "twitter"],
}


def _pick(field: str, results: dict) -> Optional[str]:
    for source in FIELD_PRIORITY.get(field, []):
        val = results.get(source, {}).get(field)
        if val:
            return val
    return None


def merge_results(adapter_results: dict, organizer_id: str) -> OrganizerProfile:
    now = datetime.now(timezone.utc).isoformat()

    profile = OrganizerProfile(
        organizer_id=organizer_id,
        resolved_at=now,
        identity=IdentityFields(
            full_name=_pick("full_name", adapter_results),
            primary_email=_pick("primary_email", adapter_results),
            company=_pick("company", adapter_results),
            job_title=_pick("job_title", adapter_results),
            location=_pick("location", adapter_results),
        ),
        social=SocialFields(
            linkedin_url=_pick("linkedin_url", adapter_results),
            twitter_handle=_pick("twitter_handle", adapter_results),
            website_url=_pick("website_url", adapter_results),
        ),
        professional=ProfessionalFields(
            bio=_pick("bio", adapter_results),
            specialisms=adapter_results.get("linkedin", {}).get("specialisms", []),
        ),
        event_history=(
            adapter_results.get("luma", {}).get("events", [])
            + adapter_results.get("eventbrite", {}).get("events", [])
        ),
        social_presence=SocialPresence(
            twitter_followers=adapter_results.get("twitter", {}).get("followers"),
            linkedin_connections=adapter_results.get("linkedin", {}).get("connections"),
            recent_posts_sample=adapter_results.get("twitter", {}).get(
                "recent_posts", []
            ),
        ),
        web_presence=WebPresence(
            serp_result_count=adapter_results.get("serp", {}).get("result_count"),
            notable_press=adapter_results.get("serp", {}).get("press", []),
        ),
        uk_company=UKCompany(
            company_name=adapter_results.get("companies_house", {}).get("company_name"),
            company_number=adapter_results.get("companies_house", {}).get(
                "company_number"
            ),
            incorporated_date=adapter_results.get("companies_house", {}).get(
                "incorporated_date"
            ),
            status=adapter_results.get("companies_house", {}).get("status"),
        ),
        provenance={
            name: SourceProvenance(
                fields_contributed=data.get("fields_contributed", []),
                latency_ms=data.get("latency_ms"),
                success=data.get("success", False),
            )
            for name, data in adapter_results.items()
            if isinstance(data, dict)
        },
    )

    profile.confidence_score = compute_confidence(profile)
    return profile


async def enrich(
    name: str,
    email: str = "",
    company: str = "",
    linkedin_url: str = "",
    browser=None,
) -> OrganizerProfile:
    from adapters.apollo import apollo_adapter
    from adapters.companies_house import companies_house_adapter
    from adapters.serp import serp_adapter
    from adapters.website import website_adapter

    organizer_id = make_organizer_id(name, email)

    coros = [
        apollo_adapter(name=name, email=email, company=company),
        companies_house_adapter(name=company or name),
        serp_adapter(name=name),
        website_adapter(url=linkedin_url or "", browser=browser),
    ]

    raw = await asyncio.gather(*coros, return_exceptions=True)
    source_names = ["apollo", "companies_house", "serp", "website"]

    adapter_results: dict = {}
    for source, result in zip(source_names, raw):
        if isinstance(result, Exception):
            adapter_results[source] = {
                "success": False,
                "error": str(result),
                "fields_contributed": [],
            }
        else:
            adapter_results[source] = result

    all_failed = all(not v.get("success", False) for v in adapter_results.values())
    if all_failed:
        return OrganizerProfile(
            organizer_id=organizer_id,
            resolved_at=datetime.now(timezone.utc).isoformat(),
            confidence_score=0.0,
            provenance={
                k: SourceProvenance(
                    **{
                        kk: vv
                        for kk, vv in v.items()
                        if kk in SourceProvenance.model_fields
                    }
                )
                for k, v in adapter_results.items()
            },
            error="all_sources_failed",
        )

    return merge_results(adapter_results, organizer_id)
