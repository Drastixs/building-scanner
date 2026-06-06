from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field
import hashlib


class IdentityFields(BaseModel):
    full_name: Optional[str] = None
    primary_email: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    location: Optional[str] = None


class SocialFields(BaseModel):
    linkedin_url: Optional[str] = None
    twitter_handle: Optional[str] = None
    website_url: Optional[str] = None


class ProfessionalFields(BaseModel):
    bio: Optional[str] = None
    specialisms: list[str] = Field(default_factory=list)
    years_active: Optional[int] = None


class EventRecord(BaseModel):
    source: str
    event_name: str
    event_date: Optional[str] = None
    attendee_estimate: Optional[int] = None


class SocialPresence(BaseModel):
    twitter_followers: Optional[int] = None
    linkedin_connections: Optional[str] = None
    recent_posts_sample: list[str] = Field(default_factory=list)


class WebPresence(BaseModel):
    serp_result_count: Optional[int] = None
    notable_press: list[str] = Field(default_factory=list)
    first_seen_date: Optional[str] = None


class UKCompany(BaseModel):
    company_name: Optional[str] = None
    company_number: Optional[str] = None
    incorporated_date: Optional[str] = None
    status: Optional[str] = None


class SourceProvenance(BaseModel):
    fields_contributed: list[str] = Field(default_factory=list)
    latency_ms: Optional[int] = None
    success: bool = False


class OrganizerProfile(BaseModel):
    organizer_id: str
    resolved_at: str
    confidence_score: float = 0.0
    identity: IdentityFields = Field(default_factory=IdentityFields)
    social: SocialFields = Field(default_factory=SocialFields)
    professional: ProfessionalFields = Field(default_factory=ProfessionalFields)
    event_history: list[EventRecord] = Field(default_factory=list)
    social_presence: SocialPresence = Field(default_factory=SocialPresence)
    web_presence: WebPresence = Field(default_factory=WebPresence)
    uk_company: UKCompany = Field(default_factory=UKCompany)
    provenance: dict[str, SourceProvenance] = Field(default_factory=dict)
    error: Optional[str] = None


def make_organizer_id(name: str, email: str = "") -> str:
    key = f"{name.lower().strip()}:{email.lower().strip()}"
    return hashlib.sha256(key.encode()).hexdigest()[:16]


def compute_confidence(profile: OrganizerProfile) -> float:
    identity_score = (
        sum(
            [
                bool(profile.identity.full_name),
                bool(profile.identity.primary_email),
                bool(profile.identity.company),
                bool(profile.identity.job_title),
                bool(profile.identity.location),
            ]
        )
        / 5
        * 0.4
    )

    social_score = (
        sum(
            [
                bool(profile.social.linkedin_url),
                bool(profile.social.twitter_handle),
                bool(profile.social.website_url),
            ]
        )
        / 3
        * 0.2
    )

    event_score = (min(len(profile.event_history), 3) / 3) * 0.2

    web_score = (
        sum(
            [
                bool(profile.web_presence.serp_result_count),
                bool(profile.web_presence.notable_press),
            ]
        )
        / 2
        * 0.1
    )

    company_score = bool(profile.uk_company.company_number) * 0.1

    return round(
        identity_score + social_score + event_score + web_score + company_score, 3
    )
