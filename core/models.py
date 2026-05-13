from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ModelResponse:
    model_name: str
    provider: str
    content: str
    latency_ms: float
    token_count: int = 0
    error: Optional[str] = None
    success: bool = True


@dataclass
class ComparisonResult:
    prompt: str
    category: str
    responses: list[ModelResponse] = field(default_factory=list)
    winner: Optional[str] = None

    def to_dict(self):
        return {
            "prompt": self.prompt,
            "category": self.category,
            "responses": [
                {
                    "model_name": r.model_name,
                    "provider": r.provider,
                    "content": r.content,
                    "latency_ms": r.latency_ms,
                    "token_count": r.token_count,
                    "error": r.error,
                    "success": r.success,
                }
                for r in self.responses
            ],
            "winner": self.winner,
        }