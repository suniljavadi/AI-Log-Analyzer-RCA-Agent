import time


class LLMService:
    def __init__(self, mode: str = "mock"):
        self.mode = mode

    def analyze(self, context: dict) -> tuple[dict, float]:
        started = time.perf_counter()
        # The deterministic agent owns the diagnosis in mock mode; this seam is ready for an OpenAI-compatible client.
        return context, (time.perf_counter() - started) * 1000
