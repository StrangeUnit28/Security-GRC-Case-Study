# Security-GRC-Case-Study

## Description

This project addresses a technical challenge focused on automating and improving security governance, risk, and compliance (GRC) processes. The main goal is to develop solutions that verify technical controls in software development workflows, automate evidence collection for compliance, and prepare for future integration with AI and Model Context Protocol (MCP) technologies. Specifically, the project aims to ensure that all GitHub Pull Requests (PRs) are approved by someone other than the author before being merged, supporting compliance and audit requirements.


## Planning

The project is structured in three main stages, each designed to address a specific aspect of the challenge and demonstrate a practical, technical approach to automation and GRC controls:

### 1. Technical Control Verification

I will develop a script or service that interacts with the GitHub API to retrieve Pull Request (PR) data for relevant repositories. The logic will:
- Identify all merged PRs within a defined amount.
- For each PR, compare the author with the list of approvers (reviewers who approved the PR).
- Flag any PRs where the author is also the approver, or where no independent approval is present.
- Optionally, provide reporting or alerting mechanisms (e.g., dashboards, notifications) to highlight non-compliance.
This approach ensures that technical controls are verifiable, repeatable, and can be integrated into CI/CD pipelines or compliance monitoring tools.

### 2. Automated Evidence Update


### 3. Preparing for LLM + MCP Integration

## Video

A video will be provided to explain the project, its structure, and the reasoning behind each implementation decision.

## Improvements

This section will cover areas for further investigation and potential enhancements.

## Bonus