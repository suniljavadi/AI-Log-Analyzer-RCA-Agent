from typing import Any


class DiagnosticAgent:
    recommendations = {
        "SQL Timeout": ["Check blocking sessions.", "Review execution plan and indexes.", "Check database CPU and IO.", "Review recent data growth."],
        "SQL Deadlock": ["Inspect deadlock graphs.", "Compare transaction access order.", "Review lock duration and isolation level."],
        "Connection Failure": ["Verify endpoint and port.", "Check connection pool capacity.", "Review database/network availability."],
        "API Timeout": ["Inspect upstream latency.", "Check API gateway timeout settings.", "Review request payload and dependency health."],
        "File Missing": ["Verify upstream file delivery.", "Check path and permissions.", "Review scheduler dependency completion."],
        "Memory Error": ["Inspect process memory limits.", "Review batch size and leaks.", "Check host memory pressure."],
    }

    def diagnose(self, parsed: dict[str, Any], similar: list[dict[str, Any]], tools: list[dict[str, Any]]) -> dict[str, Any]:
        error_type = parsed["error_type"]
        duration, expected = parsed.get("duration"), parsed.get("expected_duration")
        facts = [f"Observed {error_type}: {parsed['error_message']}"]
        evidence = []
        if duration is not None and expected is not None:
            facts.append(f"Execution duration was {duration:g} minutes versus {expected:g} minutes expected.")
            if duration > expected * 1.5:
                evidence.append("Execution duration increased significantly above baseline.")
        if similar:
            evidence.append(f"Retrieved {len(similar)} historical incidents with related error signatures.")
        cause = self._cause(error_type, similar)
        alternatives = self._alternatives(error_type, similar)
        confidence = min(96, 65 + (15 if evidence else 0) + (10 if similar else 0))
        return {"observed_facts": facts, "likely_root_cause": cause, "evidence": evidence or ["The supplied log contains an error signature but limited corroborating telemetry."], "hypotheses": alternatives, "recommendations": self.recommendations.get(error_type, ["Collect service logs and metrics.", "Compare with the last successful run.", "Escalate to the owning engineering team."]), "confidence": confidence, "severity": self._severity(error_type, duration, expected)}

    @staticmethod
    def _cause(error_type: str, similar: list[dict[str, Any]]) -> str:
        if similar and similar[0].get("root_cause"):
            return similar[0]["root_cause"]
        return {"SQL Timeout": "Database query timeout.", "SQL Deadlock": "Concurrent transactions contended for locks.", "API Timeout": "Upstream dependency exceeded the request timeout."}.get(error_type, "Insufficient evidence to determine a single root cause.")

    @staticmethod
    def _alternatives(error_type: str, similar: list[dict[str, Any]]) -> list[dict[str, Any]]:
        causes = [item["root_cause"] for item in similar[1:4] if item.get("root_cause")]
        if not causes:
            causes = {"SQL Timeout": ["Blocking", "Missing index", "Increased data volume", "Database resource contention"], "Connection Failure": ["Service unavailable", "Network policy change", "Connection pool exhaustion"]}.get(error_type, ["Transient dependency issue", "Configuration drift", "Resource contention"])
        return [{"hypothesis": cause, "confidence": "medium" if i else "low", "status": "hypothesis"} for i, cause in enumerate(causes)]

    @staticmethod
    def _severity(error_type: str, duration: float | None, expected: float | None) -> str:
        if error_type in {"Memory Error", "Disk Space", "Data Quality Failure"}:
            return "CRITICAL" if error_type == "Disk Space" else "HIGH"
        if error_type in {"SQL Timeout", "SQL Deadlock", "API 500", "SSIS Failure"}:
            return "HIGH"
        if error_type == "Unknown Error":
            return "MEDIUM"
        return "MEDIUM"
