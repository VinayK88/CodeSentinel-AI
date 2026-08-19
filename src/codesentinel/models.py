from dataclasses import dataclass, asdict
from typing import Literal

Severity = Literal["low", "medium", "high", "critical"]

@dataclass(frozen=True)
class Finding:
    rule_id: str
    title: str
    severity: Severity
    cwe: str
    line: int
    evidence: str
    confidence: float
    risk_score: float = 0.0

    def to_dict(self):
        return asdict(self)
