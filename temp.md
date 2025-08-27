Hello, Rafael!
Shall we move on to the next stage of the selection process?

Technical Challenge - Deadline to submit:27/08/2025 at 12pm
After that, we'll review your project and schedule a interview with the team.

:test_tube: Security GRC – Case Study
Goal: Evaluate your practical thinking in approaching automation, technical controls, and foundational GRC concepts — no prior GRC experience is required.

:mag_right: Context
CloudWalk’s Security GRC team relies on internal bots to automate parts of its governance and compliance processes. One such bot is Erambot, which assists in risk management workflows within Eramba, our GRC platform.
Currently, Erambot performs rule-based automation and interacts with Eramba via its REST API. The team is now planning to evolve it into a more intelligent AI agent, capable of understanding context, interacting more autonomously, and using Model Context Protocol (MCP) with LLMs in the near future.

:briefcase: Your Challenge
Imagine you're leading this transformation. How would you approach the following tasks?

    Technical Control Verification:
        A new control requires that Pull Requests (PRs) in GitHub are approved by someone other than the author before being merged.
        How would you programmatically verify that this control is being followed?
        What kind of logic, sampling strategy, or API queries would you consider using?
    Automated Evidence Update:
        Assuming Eramba provides a REST API, how would you automate the submission of control evidence (e.g., audit logs, approval records, metrics)?
        How should the bot structure this interaction?
    Preparing for LLM + MCP Integration (Future Thinking):
        While Erambot does not yet use LLMs or MCP, how could you see them enhancing its functionality?
        Give a concrete example of how a bot using an LLM, structured via MCP, might reason over PR approval patterns or suggest improvements to the process.

:pushpin: Instructions

    Respond with real code (Go, Python, or Typescript — your choice).
    Feel free to make assumptions and indicate areas where you'd investigate further.
    Most importantly, we want to understand your technical reasoning and curiosity.
