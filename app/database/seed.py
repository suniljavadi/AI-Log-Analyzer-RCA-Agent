from sqlalchemy import select

from app.database.models import Incident, SessionLocal, init_db
from app.services.catalog import build_incidents


def seed_database() -> None:
    init_db()
    with SessionLocal() as session:
        if session.scalar(select(Incident.id).limit(1)) is not None:
            return
        for item in build_incidents():
            session.add(Incident(incident_id=item["incident_id"], timestamp=item["timestamp"], system=item["system"], job=item["job"], error_type=item["error_type"], error_message=item["error_message"], root_cause=item["root_cause"], resolution=item["resolution"], severity=item["severity"], duration=item["duration"], metadata_json=item["metadata"]))
        session.commit()
