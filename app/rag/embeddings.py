import hashlib
import math


class DeterministicEmbedder:
    """Offline embedding substitute; API-compatible with a vector retriever."""

    def __init__(self, dimensions: int = 128):
        self.dimensions = dimensions

    def embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        for token in text.lower().split():
            digest = hashlib.sha256(token.encode()).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            vector[index] += 1.0 if digest[4] % 2 else -1.0
        norm = math.sqrt(sum(item * item for item in vector)) or 1.0
        return [item / norm for item in vector]

    def similarity(self, left: str, right: str) -> float:
        a, b = self.embed(left), self.embed(right)
        return sum(x * y for x, y in zip(a, b))
