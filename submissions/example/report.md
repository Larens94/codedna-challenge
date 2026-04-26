# Submission Report — [your-username] · [task_id]

## Setup

- **Tool:** (e.g. Claude Code, Cursor, Copilot, …)
- **Model:** (e.g. claude-sonnet-4-6, gpt-4o, deepseek-chat, …)
- **Config:** (e.g. custom CLAUDE.md, .cursorrules, no config, …)
- **Stack extras:** (RAG, vector DB, MCP — or "none")
- **CodeDNA layers activated (Run B):** (e.g. L0+L1, L0+L1+wiki, …)

## Run A — baseline (no CodeDNA)

Briefly describe how the agent approached the task without CodeDNA annotations: which files it opened first, how it navigated to the bug, how many retries were needed.

(3–6 sentences is enough)

## Run B — with CodeDNA

Describe the same for the run with CodeDNA annotations present. Did navigation change? Did the agent use `used_by:` / `rules:` / `message:` fields?

## Delta

What concretely changed between Run A and Run B? (token count, tool calls, failed edits, f1_localization, cost…)

## Why this configuration

Why did you choose this tool and config? What did you expect CodeDNA to do better or worse with your specific setup?

## Borderline cases ⚠️

List anything that could affect the validity of your submission and should be reviewed by the organiser before it counts toward the ranking:

- [ ] (none — submission is straightforward)

Examples of things to flag:
- The agent read a file that partially reveals the fix
- A test passed for the wrong reason
- You had to intervene manually at some point
- The task description was ambiguous and you interpreted it a specific way
- Run A and Run B were not run in strictly identical conditions

## Observations

Anything that surprised you — positive or negative — about the task, the tool, or the effect of CodeDNA annotations on your workflow.
