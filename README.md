# CodeDNA Challenge

> **Can your agent configuration navigate a codebase better than CodeDNA — at the same level?**

An open benchmark for researchers and developers. Solve the same real multi-file bugs using any **Level 0 configuration** — CodeDNA annotations, a custom CLAUDE.md, plain .cursorrules, no config at all — and compare results objectively.

## Prizes

| Rank | Prize |
|------|-------|
| 🥇 1st | €200 |
| 🥈 2nd | €100 |
| 🥉 3rd | €50 |

Winners announced once we reach a minimum number of valid submissions.
Results published in real time on the leaderboard.

---

## The fairness rule: symmetric stacks

CodeDNA is always the **control**. Every submission is compared against a CodeDNA run at the **same stack level**.

### CodeDNA stack levels

CodeDNA v0.9 ships multiple layers — participants choose which ones to activate:

| CodeDNA layer | What it adds |
|---------------|-------------|
| **L0** — `.codedna` manifest | Repo-level package map injected at session start |
| **L1** — module headers | `exports:` `used_by:` `rules:` `related:` `agent:` `message:` in every file |
| **L2** — function Rules: | Docstring-level constraints at every cross-file function call |
| **L3** — semantic naming | Variable names encode type + origin + domain |
| **wiki** — knowledge vault | `wiki:` field + `codedna wiki bootstrap/sync` → Obsidian vault + narrative project wiki |

### Comparison rule

| Your submission | Required CodeDNA control run |
|-----------------|------------------------------|
| Any config, no extras | CodeDNA L0+L1 ← already published |
| Your config + knowledge base / docs | CodeDNA L0+L1+wiki |
| Your config + RAG | CodeDNA L0+L1+wiki + same RAG setup |
| Your config + vector DB / MCP / Skills | CodeDNA L0+L1+wiki + same extras |

**You can bring any stack — as long as CodeDNA has the same stack in the paired comparison.**

The organiser (@Larens94) publishes the CodeDNA reference runs first. If you want to test at a higher stack level, request the corresponding CodeDNA run by opening an issue.

---

## Rules

1. **Minimum participants:** the leaderboard and prizes activate when **at least 20 valid submissions** are received across all tasks. Before that threshold, submissions are collected but not ranked.

2. **Validity:** a submission is valid only if `task_tests_pass: true` AND `regression_tests_pass: true`, verified by CI. Invalid or failing submissions are discarded without notice.

3. **No cheating:** submissions that hardcode expected outputs, read ground-truth files before starting, or otherwise circumvent genuine agent navigation are disqualified. The organiser (@Larens94) reviews all submissions manually.

4. **Mini report required:** every submission must include a `report.md` (max 1 page) covering:
   - What configuration you used and why
   - How the agent approached the task (navigation strategy)
   - Any **borderline cases** — ambiguous annotations, edge cases in the task, or anything you think should be reviewed before it counts toward the ranking
   - Anything that surprised you (positive or negative)

5. **Symmetric stack:** if you add tools beyond Level 0 (RAG, vector DB, MCP), a matching CodeDNA run at the same stack level is required. The organiser publishes CodeDNA reference runs — open an issue to request one at a higher stack level.

6. **One submission per task per participant.** You may resubmit if your previous submission was invalid (tests failed), but you must open a new PR with a new `report.md` explaining what changed.

7. **Results are public.** All submissions — including failed ones — are visible in the repo for transparency.

---

## How to participate

1. **Choose a task** from the `tasks/` folder
2. **Clone this repo** and work on `project/` with your agent + configuration
3. **Run the tests** — they must pass (CI verifies this, not self-reported)
4. **Fill in `results.json`** with your metrics (token usage, cost, files touched)
5. **Open a PR** adding `submissions/<your-username>/` with:
   - `results.json` — your metrics
   - `config/` — your configuration files (CLAUDE.md, .cursorrules, etc.)
   - Optional: `session.jsonl` or a link to your raw session trace

**Submissions with invalid or non-passing tests are discarded.**
The organiser (@Larens94) reviews all submissions before the leaderboard updates.

---

## Metrics

Every submission is evaluated on:

**Fix correctness**
| Metric | Description |
|--------|-------------|
| `task_tests_pass` | Task-specific failing tests now pass (the bug is fixed) |
| `regression_tests_pass` | Full test suite still green — no regressions introduced |
| `patch_lines` | Lines changed in the final patch (smaller = more surgical) |

**Navigation quality**
| Metric | Description |
|--------|-------------|
| `f1_localization` | Did the agent find the right files? (harmonic mean of precision + recall on ground-truth files) |
| `retry_count` | How many times did you re-invoke the agent because the patch was incomplete? |

**Token efficiency**
| Metric | Description |
|--------|-------------|
| `tokens_input` | Input tokens consumed |
| `tokens_output` | Output tokens generated |
| `cache_read` | Cache tokens reused (lower cost) |
| `cost_usd` | Total session cost in USD across all retries |
| `tool_calls_total` | Total tool calls — fewer = less navigation waste |

**Multi-agent (optional — if your run uses more than one agent)**
| Metric | Description |
|--------|-------------|
| `agent_count` | Number of agents in the session |
| `message_adoption_rate` | % of files where agents used `message:` for coordination (CodeDNA only) |
| `framework_conflicts` | Architectural conflicts detected (e.g. two agents using different frameworks) |

**Why these metrics matter — existing CodeDNA data:**

| Dimension | Without CodeDNA | With CodeDNA |
|-----------|----------------|--------------|
| Files matching official patch (Django #13495, Claude Sonnet) | 6 / 7 | **7 / 7** |
| Failed edits (same task) | 5 | **0** |
| High-risk runs — recall < 50% → incomplete patch (SWE-bench, 3 models) | 52% | **25%** |
| Tool calls (Gemini 2.5 Pro) | baseline | **−14.3%** |
| Team velocity (5-agent SaaS, DeepSeek R1) | 1× | **1.6×** |

CodeDNA doesn't just help the agent find the right files — it eliminates failed edits entirely on dependency-chain tasks. This challenge verifies whether that holds on new projects and new models.

Ranking: `task_tests_pass` + `regression_tests_pass` first → `f1_localization` DESC → `cost_usd` ASC (all retries summed).

---

## Generating your results.json automatically

If you used **Claude Code**, run:

```bash
python scripts/report.py \
  --session ~/.claude/projects/<hash>/<session-id>.jsonl \
  --task task_01 \
  --participant your-github-username \
  --approach "codedna-v0.9"
```

This reads your session JSONL and fills in all token/cost/tool-call metrics automatically.
You still need to fill in `files_touched` manually.

For other tools (Cursor, Copilot, OpenCode), fill `results.json` manually from your tool's usage stats.

---

## Tasks

Tasks are proposed and validated by the research community before the challenge opens.

**Requirements for a valid task:**
- Real bug from an open source Python project (not already in SWE-bench)
- Multi-file fix: patch touches 2–6 files
- Deterministic test suite: a specific test fails before the fix and passes after
- The project is frozen at a specific commit — everyone works on identical code

**To propose a task:** open an issue with the label `task-proposal` including the GitHub issue URL, the commit to freeze, and the failing test.

The challenge opens once at least **3 validated tasks** are ready and **20 participants** have signed up.

The organiser (@Larens94) publishes the CodeDNA reference runs on each task as the baseline everyone competes against.

| Task | Project | Difficulty | Files affected |
|------|---------|------------|----------------|
| task_01 | open for proposals | — | — |
| task_02 | open for proposals | — | — |
| … | up to 10 tasks | — | — |

---

## Leaderboard

→ **[View live leaderboard](https://larens94.github.io/codedna-challenge)**

---

## What this challenge is about

This is not a marketing exercise. CodeDNA was designed to solve a specific problem: AI agents spend too much of their context budget navigating the wrong files. The hypothesis is that embedding navigation metadata directly in source files — at Level 0, with zero external infrastructure — is enough to measurably improve agent performance.

We already have benchmark data on SWE-bench Django tasks. This challenge invites the community to test the hypothesis on different projects, with different models, and with competing configurations.

If your approach beats CodeDNA, that is a valid and interesting result. Publish it.

---

## Contact

- GitHub: [@Larens94](https://github.com/Larens94)
- CodeDNA spec & paper: [github.com/Larens94/codedna](https://github.com/Larens94/codedna)
- Questions: open an issue in this repo
