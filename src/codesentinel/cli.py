import argparse, json
from pathlib import Path
from .rules import scan_diff
from .validator import validate
from .evaluation import evaluate

def main():
    p=argparse.ArgumentParser(description="Review a unified diff for security-relevant changes")
    p.add_argument("--input", default="sample_data/pr_diff.txt")
    p.add_argument("--labels", default="sample_data/labels.json")
    p.add_argument("--output", default=None)
    args=p.parse_args()
    text=Path(args.input).read_text(encoding="utf-8")
    findings=validate(scan_diff(text))
    expected=[]
    labels=Path(args.labels)
    if labels.exists():
        expected=json.loads(labels.read_text(encoding="utf-8")).get("expected_rule_ids",[])
    payload={
      "input":args.input,
      "finding_count":len(findings),
      "high_risk_count":sum(f.severity in {"high","critical"} for f in findings),
      "evaluation":evaluate([f.rule_id for f in findings], expected) if expected else {},
      "findings":[f.to_dict() for f in findings],
    }
    rendered=json.dumps(payload, indent=2)
    if args.output:
        Path(args.output).write_text(rendered+"\n", encoding="utf-8")
    print(rendered)

if __name__ == "__main__": main()
