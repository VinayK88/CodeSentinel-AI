from dataclasses import dataclass, asdict

@dataclass
class FindingLifecycle:
    finding_id: str
    state: str = "detected"
    developer_disposition: str | None = None
    remediation_commit: str | None = None
    verified: bool = False

    def accept(self):
        self.state = "accepted"
        self.developer_disposition = "accepted"

    def dismiss(self, reason="false_positive"):
        self.state = "dismissed"
        self.developer_disposition = reason

    def remediate(self, commit_sha: str):
        if self.state not in {"accepted", "remediating"}:
            raise ValueError("finding must be accepted before remediation")
        self.state = "remediating"
        self.remediation_commit = commit_sha

    def verify(self):
        if not self.remediation_commit:
            raise ValueError("remediation commit required before verification")
        self.state = "verified"
        self.verified = True

    def to_dict(self):
        return asdict(self)
