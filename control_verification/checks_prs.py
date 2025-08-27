
import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = os.getenv("GITHUB_OWNER")
REPO = os.getenv("GITHUB_REPO")
PER_PAGE = int(os.getenv("GITHUB_PER_PAGE", 50))

headers = {"Authorization": f"Bearer {TOKEN}"}


def get_merged_prs():
    """Fetch merged PRs."""
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls"
    params = {"state": "closed", "per_page": PER_PAGE}
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    prs = resp.json()
    return [pr for pr in prs if pr.get("merged_at")]


def get_reviews(pr_number):
    """Fetch reviews for a PR."""
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls/{pr_number}/reviews"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()


def get_pr_approval_status():
    """Return (compliant, violations) lists for merged PRs."""
    merged_prs = get_merged_prs()
    violations = []
    compliant = []
    for pr in merged_prs:
        pr_number = pr["number"]
        author = pr["user"]["login"]
        reviews = get_reviews(pr_number)
        approvals = [
            r for r in reviews
            if r["state"].upper() == "APPROVED" and r["user"]["login"] != author
        ]
        if not approvals:
            violations.append(pr)
        else:
            compliant.append(pr)
    return compliant, violations


def check_prs():
    """Check if merged PRs were self-approved only."""
    merged_prs = get_merged_prs()
    violations = []

    for pr in merged_prs:
        pr_number = pr["number"]
        author = pr["user"]["login"]

        reviews = get_reviews(pr_number)
        approvals = [
            r for r in reviews
            if r["state"].upper() == "APPROVED" and r["user"]["login"] != author
        ]

        if not approvals:
            violations.append({
                "pr_number": pr_number,
                "title": pr["title"],
                "author": author,
                "merged_at": pr["merged_at"]
            })

    return violations


if __name__ == "__main__":
    violations = check_prs()
    if violations:
        print("Violations found:")
        for v in violations:
            print(f" - PR #{v['pr_number']} ({v['title']}) by {v['author']} merged at {v['merged_at']} with no external approval")
    else:
        print("All merged PRs had proper approvals.")
