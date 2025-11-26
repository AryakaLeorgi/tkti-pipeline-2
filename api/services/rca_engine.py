import re
from models.schemas import RCAResult

class RCAEngine:

    def analyze(self, log: str) -> RCAResult:
        if "NullPointerException" in log:
            return RCAResult(
                root_cause="NullPointerException detected in Java module",
                category="Unit Test Failure",
                confidence=0.92
            )

        if "ImagePullBackOff" in log:
            return RCAResult(
                root_cause="Kubernetes failed to pull Docker image",
                category="Deployment Error",
                confidence=0.88
            )

        if "CVE-" in log:
            return RCAResult(
                root_cause="Security vulnerability detected in dependency",
                category="Security Scan Failure",
                confidence=0.94
            )

        return RCAResult(
            root_cause="Unknown issue. Further analysis required.",
            category="Unknown",
            confidence=0.50
        )
