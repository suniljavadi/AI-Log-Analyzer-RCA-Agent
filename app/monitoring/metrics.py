from dataclasses import dataclass, field


@dataclass
class AnalysisMetrics:
    request_id: str
    classification: str = ""
    diagnosis: str = ""
    confidence: int = 0
    retrieval_latency_ms: float = 0.0
    llm_latency_ms: float = 0.0
    tool_calls: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
