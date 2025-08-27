
import requests
import datetime
import json
import os
from control_verification.checks_prs import get_pr_approval_status
from control_verification.pr_compliance_report import generate_report


class ErambotEvidenceUploader:
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_token}"
        })

    def submit_evidence(self, control_id: str, evidence_data: dict) -> dict:
        url = f"{self.base_url}/api/controls/{control_id}/evidences"
        payload = {
            "timestamp": datetime.datetime.now().isoformat() + "Z",
            "evidence_type": evidence_data.get("type", "log"),
            "description": evidence_data.get("description", "Automated evidence upload"),
            "source": evidence_data.get("source", "Erambot"),
            "content": evidence_data.get("content", {}),
        }
        headers = {"Content-Type": "application/json"}
        response = self.session.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code == 201:
            print(f"Evidence submitted for control {control_id}")
        else:
            print(f"Failed to submit evidence: {response.status_code} {response.text}")
        return response.json()

    def submit_pdf_evidence(self, control_id: str, pdf_path: str, description: str = "Automated PDF evidence upload") -> dict:
        url = f"{self.base_url}/api/controls/{control_id}/evidences"
        files = {
            "file": (os.path.basename(pdf_path), open(pdf_path, "rb"), "application/pdf")
        }
        data = {
            "timestamp": datetime.datetime.now().isoformat() + "Z",
            "evidence_type": "report",
            "description": description,
            "source": "Erambot"
        }
        response = self.session.post(url, data=data, files=files)
        if response.status_code == 201:
            print(f"PDF evidence submitted for control {control_id}")
        else:
            print(f"Failed to submit PDF evidence: {response.status_code} {response.text}")
        return response.json()


if __name__ == "__main__":
    # Use environment variables or config for these
    ERAMBA_URL = os.getenv("ERAMBA_URL", "https://eramba.company.com")
    API_TOKEN = os.getenv("ERAMBA_API_TOKEN", "YOUR_ERAMBA_API_TOKEN")
    CONTROL_ID = os.getenv("ERAMBA_CONTROL_ID", "CTRL-1234")

    bot = ErambotEvidenceUploader(ERAMBA_URL, API_TOKEN)

    # Get real violations from the control verification logic
    compliant, violations = get_pr_approval_status()

    # Generate and send PDF report as evidence
    pdf_path = generate_report(compliant, violations)
    bot.submit_pdf_evidence(control_id=CONTROL_ID, pdf_path=pdf_path, description="Automated PR compliance PDF report")

    # Optionally, still send individual violation records as structured evidence
    for v in violations:
        evidence = {
            "type": "approval_record",
            "description": f"Pull request #{v['number']} ({v['title']}) merged by {v['author']} without external approval.",
            "source": "GitHub API",
            "content": {
                "pr_id": v['number'],
                "author": v['author'],
                "merged_at": v['merged_at']
            }
        }
        bot.submit_evidence(control_id=CONTROL_ID, evidence_data=evidence)
