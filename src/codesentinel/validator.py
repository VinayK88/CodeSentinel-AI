from dataclasses import replace
from .models import Finding

SEV_BONUS = {"low": 0.0, "medium": 0.05, "high": 0.1, "critical": 0.15}

def validate(findings: list[Finding]) -> list[Finding]:
    seen=set(); out=[]
    for f in findings:
        fingerprint=(f.rule_id, f.evidence)
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        context_bonus = 0.05 if any(k in f.evidence.lower() for k in ("admin", "token", "password", "query")) else 0.0
        score=min(1.0, f.risk_score + SEV_BONUS[f.severity] + context_bonus)
        out.append(replace(f, risk_score=round(score,3)))
    return sorted(out, key=lambda x: x.risk_score, reverse=True)
