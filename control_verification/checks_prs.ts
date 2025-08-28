import { Octokit } from "@octokit/rest";
import * as dotenv from "dotenv";

dotenv.config();

const TOKEN = process.env.GITHUB_TOKEN || "";
const OWNER = process.env.GITHUB_OWNER || "";
const REPO = process.env.GITHUB_REPO || "";
const PER_PAGE = parseInt(process.env.GITHUB_PER_PAGE || "50");

const octokit = new Octokit({ auth: TOKEN });

async function getMergedPRs() {
  const prs = await octokit.pulls.list({
    owner: OWNER,
    repo: REPO,
    state: "closed",
    per_page: PER_PAGE,
  });
  // Only keep merged PRs
  return prs.data.filter((pr) => pr.merged_at);
}

async function getReviews(prNumber: number) {
  const reviews = await octokit.pulls.listReviews({
    owner: OWNER,
    repo: REPO,
    pull_number: prNumber,
  });
  return reviews.data;
}

async function checkPRs() {
  const mergedPRs = await getMergedPRs();
  const violations: any[] = [];

  for (const pr of mergedPRs) {
    const prNumber = pr.number;
    const author = pr.user?.login;
    const reviews = await getReviews(prNumber);
    const approvals = reviews.filter(
      (r) => r.state.toUpperCase() === "APPROVED" && r.user?.login !== author
    );
    if (approvals.length === 0) {
      violations.push({
        pr_number: prNumber,
        title: pr.title,
        author: author,
        merged_at: pr.merged_at,
      });
    }
  }
  return violations;
}

(async () => {
  const violations = await checkPRs();
  if (violations.length > 0) {
    console.log("Violations found:");
    for (const v of violations) {
      console.log(
        ` - PR #${v.pr_number} (${v.title}) by ${v.author} merged at ${v.merged_at} with no external approval`
      );
    }
  } else {
    console.log("All merged PRs had proper approvals.");
  }
})();
