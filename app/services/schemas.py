from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class AnalyzeRequest(BaseModel):
    raw_log: str = Field(min_length=10, max_length=20_000)
    approve_actions: bool = False

    @field_validator("raw_log")
    @classmethod
    def reject_injection(cls, value: str) -> str:
        suspicious = ("ignore previous instructions", "system prompt", "reveal secrets")
        if any(item in value.lower() for item in suspicious):
            raise ValueError("Prompt injection-like content is not accepted as a log")
        return value


class SimilarIncident(BaseModel):
    incident_id: str
    error_type: str
    root_cause: str
    resolution: str
    severity: str
    score: float


class AnalysisResult(BaseModel):
    request_id: str
    observed_facts: list[str]
    classification: str
    severity: str
    error_type: str
    likely_root_cause: str
    evidence: list[str]
    hypotheses: list[dict[str, Any]]
    recommendations: list[str]
    confidence: int = Field(ge=0, le=100)
    similar_incidents: list[SimilarIncident]
    parsed_log: dict[str, Any]
    timeline: list[dict[str, Any]]
    approval_required: bool
    actions: list[dict[str, Any]]
    latency_ms: float


class IncidentResponse(BaseModel):
    incident_id: str
    timestamp: datetime
    system: str
    job: str
    error_type: str
    error_message: str
    root_cause: str
    resolution: str
    severity: str
    duration: float | None
    metadata: dict[str, Any]
