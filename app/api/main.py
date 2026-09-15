from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database.models import Incident, get_db
from app.database.seed import seed_database
from app.monitoring.logging import configure_logging
from app.monitoring.middleware import request_context
from app.services.analyzer import LogAnalyzer
from app.services.catalog import build_incidents
from app.services.schemas import AnalyzeRequest, AnalysisResult, IncidentResponse


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging(get_settings().log_level)
    seed_database()
    yield


app = FastAPI(title="AI Log Analyzer & Root Cause Analysis Agent", version="1.0.0", lifespan=lifespan)
app.add_middleware(BaseHTTPMiddleware, dispatch=request_context)


def get_analyzer() -> LogAnalyzer:
    return LogAnalyzer(build_incidents())


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "ai-log-analyzer", "mode": get_settings().llm_mode}


@app.post("/api/v1/analyze", response_model=AnalysisResult)
def analyze(payload: AnalyzeRequest, analyzer: LogAnalyzer = Depends(get_analyzer)) -> AnalysisResult:
    return analyzer.analyze(payload.raw_log, payload.approve_actions)


@app.get("/api/v1/incidents", response_model=list[IncidentResponse])
def incidents(limit: int = 50, db: Session = Depends(get_db)) -> list[IncidentResponse]:
    if limit < 1 or limit > 500:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 500")
    rows = db.scalars(select(Incident).order_by(Incident.timestamp.desc()).limit(limit)).all()
    return [IncidentResponse(incident_id=row.incident_id, timestamp=row.timestamp, system=row.system, job=row.job, error_type=row.error_type, error_message=row.error_message, root_cause=row.root_cause, resolution=row.resolution, severity=row.severity, duration=row.duration, metadata=row.metadata_json) for row in rows]


@app.get("/api/v1/incidents/{incident_id}", response_model=IncidentResponse)
def incident(incident_id: str, db: Session = Depends(get_db)) -> IncidentResponse:
    row = db.scalar(select(Incident).where(Incident.incident_id == incident_id))
    if row is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return IncidentResponse(incident_id=row.incident_id, timestamp=row.timestamp, system=row.system, job=row.job, error_type=row.error_type, error_message=row.error_message, root_cause=row.root_cause, resolution=row.resolution, severity=row.severity, duration=row.duration, metadata=row.metadata_json)
