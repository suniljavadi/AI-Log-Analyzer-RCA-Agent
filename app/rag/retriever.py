from typing import Any

from app.rag.embeddings import DeterministicEmbedder


class IncidentRetriever:
    def __init__(self, incidents: list[dict[str, Any]], embedder: DeterministicEmbedder | None = None):
        self.incidents = incidents
        self.embedder = embedder or DeterministicEmbedder()

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        scored = []
        for incident in self.incidents:
            text = f"{incident['error_type']} {incident['error_message']} {incident['root_cause']}"
            score = self.embedder.similarity(query, text)
            if incident["error_type"].lower() in query.lower():
                score += 0.35
            scored.append({**incident, "score": round(max(0.0, min(1.0, score)), 3)})
        return sorted(scored, key=lambda item: item["score"], reverse=True)[:top_k]
