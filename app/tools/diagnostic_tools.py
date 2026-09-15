from typing import Any


class DiagnosticTools:
    def search_similar_incidents(self, error_type: str) -> dict[str, Any]:
        return {"tool": "search_similar_incidents", "status": "ok", "query": error_type}

    def get_job_history(self, job: str) -> dict[str, Any]:
        return {"tool": "get_job_history", "status": "ok", "job": job, "recent_runs": 12, "failures": 2}

    def get_execution_metrics(self, job: str) -> dict[str, Any]:
        return {"tool": "get_execution_metrics", "status": "ok", "job": job, "p95_minutes": 11.0, "baseline_minutes": 8.0}

    def get_error_logs(self, job: str) -> dict[str, Any]:
        return {"tool": "get_error_logs", "status": "ok", "job": job, "related_errors": 3}

    def check_database_status(self) -> dict[str, Any]:
        return {"tool": "check_database_status", "status": "ok", "cpu_percent": 72, "io_wait_percent": 18}

    def check_blocking_sessions(self) -> dict[str, Any]:
        return {"tool": "check_blocking_sessions", "status": "ok", "blocking_sessions": 1, "status": "warning"}

    def create_ticket(self, summary: str, approved: bool = False) -> dict[str, Any]:
        return {"tool": "create_ticket", "status": "simulated" if approved else "approval_required", "summary": summary}

    def send_alert(self, message: str, approved: bool = False) -> dict[str, Any]:
        return {"tool": "send_alert", "status": "simulated" if approved else "approval_required", "message": message}
