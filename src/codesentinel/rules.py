import re
from .models import Finding

RULES = [
    ("SECRET", "Potential hard-coded secret", "critical", "CWE-798", re.compile(r'(?i)(api[_-]?key|secret|token)\s*=\s*[\'\"][A-Za-z0-9_\-]{12,}'), 0.96),
    ("SHELL", "Shell command execution enabled", "high", "CWE-78", re.compile(r"shell\s*=\s*True"), 0.93),
    ("EVAL", "Dynamic code execution", "critical", "CWE-95", re.compile(r"\beval\s*\("), 0.97),
    ("SQL", "String-built SQL query", "high", "CWE-89", re.compile(r"(?i)(SELECT|INSERT|UPDATE|DELETE).*(\{|%s|\+\s*\w+)"), 0.86),
    ("TLS", "TLS certificate verification disabled", "high", "CWE-295", re.compile(r"verify\s*=\s*False"), 0.95),
    ("DEBUG", "Debug mode enabled", "medium", "CWE-489", re.compile(r"debug\s*=\s*True"), 0.88),
]

SEV_WEIGHT = {"low": 0.25, "medium": 0.45, "high": 0.72, "critical": 0.95}

def scan_diff(text: str):
    findings=[]
    for line_no, raw in enumerate(text.splitlines(), 1):
        if not raw.startswith('+') or raw.startswith('+++'):
            continue
        code=raw[1:].strip()
        for rule_id,title,severity,cwe,pattern,confidence in RULES:
            if pattern.search(code):
                risk=round(SEV_WEIGHT[severity]*confidence, 3)
                findings.append(Finding(rule_id,title,severity,cwe,line_no,code[:180],confidence,risk))
    for line_no, raw in enumerate(text.splitlines(), 1):
        if raw.startswith('-') and not raw.startswith('---') and re.search(r"require_admin|authorize\(|permission_check", raw):
            findings.append(Finding("AUTHZ", "Authorization control removed", "critical", "CWE-862", line_no, raw[1:].strip()[:180], 0.94, 0.893))
    return findings
