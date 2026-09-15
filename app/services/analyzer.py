import time
import uuid
from typing import Any

from app.agents.diagnostic_agent import DiagnosticAgent
from app.parsers.log_parser import LogParser
from app.parsers.normalizer import LogNormalizer
from app.rag.retriever import IncidentRetriever
from app.services.schemas import AnalysisResult, SimilarIncident
from app.tools.diagnostic_tools import DiagnosticTools


class LogAnalyzer:
    def __init__(self, incidents: list[dict[str, Any]]):
        self.parser = LogParser()
        self.normalizer = LogNormalizer()
        self.retriever = IncidentRetriever(incidents)
        self.agent = DiagnosticAgent()
        self.tools = DiagnosticTools()

    def analyze(self, raw_log: str, approve_actions: bool = False) -> AnalysisResult:
        started = time.perf_counter()
        request_id = str(uuid.uuid4())
        parsed = self.normalizer.normalize(self.parser.parse(raw_log))
        query = f"{parsed['error_type']} {parsed['error_message']}"
        similar_raw = self.retriever.search(query)
        similar = [SimilarIncident(**{key: item[key] for key in ('incident_id', 'error_type', 'root_cause', 'resolution', 'severity', 'score')}) for item in similar_raw]
        tool_results = [self.tools.get_job_history(parsed['job']), self.tools.get_execution_metrics(parsed['job']), self.tools.check_database_status()]
        if parsed["error_type"] == "SQL Timeout":
            tool_results.append(self.tools.check_blocking_sessions())
        diagnosis = self.agent.diagnose(parsed, similar_raw, tool_results)
        actions = [self.tools.create_ticket(f"{parsed['error_type']} for {parsed['job']}", approve_actions), self.tools.send_alert(f"{diagnosis['severity']}: {diagnosis['likely_root_cause']}", approve_actions)]
        timeline = [{"event": "received", "timestamp": parsed["timestamp"].isoformat()}, {"event": "parsed_and_classified", "error_type": parsed["error_type"]}, {"event": "retrieved_evidence", "count": len(similar)}, {"event": "diagnosed", "severity": diagnosis["severity"]}]
        return AnalysisResult(request_id=request_id, classification=parsed["error_type"], error_type=parsed["error_type"], parsed_log=parsed, similar_incidents=similar, timeline=timeline, approval_required=not approve_actions, actions=actions, latency_ms=round((time.perf_counter() - started) * 1000, 2), **diagnosis)
