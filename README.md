> ⚠️ **DRAFT — not yet open.** Tasks are being finalized. Watch this repo for the launch announcement.

# CodeDNA Challenge

> **Does CodeDNA improve your workflow — regardless of your stack?**

An open ablation benchmark for researchers and developers. Run the same real multi-file bug-fix task **twice with your own setup** — once without CodeDNA, once with the full CodeDNA setup (annotations + agent configuration + wiki) — and measure the delta objectively.

## Prizes (symbolic)

| Rank | Prize |
|------|-------|
| 🥇 1st | €200 |
| 🥈 2nd | €100 |
| 🥉 3rd | €50 |

Prizes are symbolic and funded by the organiser. Winners announced once at least 20 valid submissions are received across all tasks.

---

## The design: within-stack ablation

This is **not** "your config vs CodeDNA." It is an ablation study:

| Run | What changes |
|-----|-------------|
| **Run A — baseline** | Your tool + your model + your config, *without* CodeDNA |
| **Run B — with CodeDNA** | Exact same tool, model, and config — plus the **full CodeDNA setup** |

The only variable that changes between Run A and Run B is CodeDNA. Everything else is held constant: same bug, same model, same tool.

**Full CodeDNA setup (Run B)** means three things working together — annotations alone are not enough:

1. **Source annotations** — `codedna init` writes `exports:` `used_by:` `rules:` `related:` `agent:` `message:` into every file
2. **Agent configuration** — the CodeDNA `CLAUDE.md` (or equivalent) tells the agent how to read and act on those annotations; without it the agent ignores them
3. **Wiki** — `codedna wiki sync` generates the narrative project wiki; this gives the agent a semantic sky-view of the codebase before it starts navigating

**You can bring any stack** (RAG, vector DB, MCP, Cursor, Copilot, multi-agent pipelines) on top of this. The ablation works regardless — Run A is your stack without CodeDNA, Run B is your stack with the full CodeDNA setup.

> Full installation guide and configuration reference: **[github.com/Larens94/codedna](https://github.com/Larens94/codedna)**

### What CodeDNA adds (Run B only)

| Layer | What it adds |
|-------|-------------|
| **L0** — `.codedna` manifest | Repo-level package map injected at session start |
| **L1** — module headers | `exports:` `used_by:` `rules:` `related:` `agent:` `message:` in every file |
| **L2** — function Rules: | Docstring-level constraints at every cross-file function call |
| **L3** — semantic naming | Variable names encode type + origin + domain |
| **wiki** | `wiki:` field + `codedna wiki sync` → narrative project wiki |

---

## Rules

1. **Minimum participants:** the leaderboard and prizes activate when **at least 20 valid submissions** are received across all tasks. Before that threshold, submissions are collected but not ranked.

2. **Validity:** a submission is valid only if `task_tests_pass: true` AND `regression_tests_pass: true` in **both** Run A and Run B, verified by CI. Invalid or failing submissions are discarded without notice.

3. **No cheating:** submissions that hardcode expected outputs, read ground-truth files before starting, or otherwise circumvent genuine agent navigation are disqualified. The organiser (@Larens94) reviews all submissions manually.

4. **Mini report required:** every submission must include a `report.md` (max 1 page) covering:
   - What tool, model, and configuration you used
   - How the agent approached the task in Run A and Run B (navigation strategy)
   - Any **borderline cases** — anything that could affect validity and should be reviewed before counting
   - What changed between Run A and Run B, and what surprised you

5. **Symmetric stack:** Run A and Run B must use the same tool, model, and configuration files. The only permitted difference is the full CodeDNA setup (annotations + CLAUDE.md protocol + wiki).

6. **One submission per task per participant.** You may resubmit if your previous submission was invalid (tests failed), but you must open a new PR with a new `report.md` explaining what changed.

7. **Results are public.** All submissions — including failed ones — are visible in the repo for transparency.

---

## How to participate

Every submission contains **two runs on the same task**: Run A (no CodeDNA) and Run B (with CodeDNA). You run both. The comparison is self-contained in your PR — the judge does not run anything.

1. **Choose a task** from the `tasks/` folder
2. **Run A — baseline:** run your agent on the frozen project. No CodeDNA annotations.
3. **Run B — with CodeDNA:** set up the full CodeDNA stack on the same frozen project:
   - `codedna init` — annotate all source files
   - Add the CodeDNA `CLAUDE.md` (from [github.com/Larens94/codedna](https://github.com/Larens94/codedna)) so the agent reads and uses the annotations
   - `codedna wiki sync` — generate the project wiki
   - Then run the same agent on the same task
4. **Open a PR** adding `submissions/<your-username>/` with:
   ```
   submissions/<your-username>/
   ├── baseline/
   │   ├── results.json     # Run A — no CodeDNA
   │   └── session.jsonl    # optional — session trace (Claude Code, Cursor, etc.)
   ├── codedna/
   │   ├── results.json     # Run B — with CodeDNA
   │   └── session.jsonl    # optional
   ├── config/              # your config files (CLAUDE.md, .cursorrules, etc.)
   └── report.md            # mini report covering both runs
   ```

**The judge (@Larens94) reviews each PR for validity and stack symmetry before it counts toward the ranking.**
CI verifies that tests pass — invalid or failing submissions are discarded.

---

## Metrics

Both Run A and Run B are measured on the same set of metrics. The delta between them is the primary signal.

**Fix correctness**
| Metric | Description |
|--------|-------------|
| `task_tests_pass` | Task-specific failing tests now pass (the bug is fixed) |
| `regression_tests_pass` | Full test suite still green — no regressions introduced |
| `patch_lines` | Lines changed in the final patch (smaller = more surgical) |
| `failed_edits` | Failed edit attempts during the session |

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
| `message_adoption_rate` | % of files where agents used `message:` for coordination (Run B only) |
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

Ranking: `task_tests_pass` + `regression_tests_pass` (both runs) first → `f1_localization` (Run B) DESC → `cost_usd` (Run B) ASC.

---

## Collecting metrics

**Claude Code** — extract from your session JSONL at `~/.claude/projects/<hash>/<session-id>.jsonl`:
- Rows with `"type": "assistant"` contain `message.usage` with `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`
- Run `/cost` inside the session for a live summary

**Other tools** (Cursor, Copilot, OpenCode) — fill `results.json` manually from your tool's usage statistics.

See `submissions/example/` for the full `results.json` template.

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

| Task | Project | Difficulty | Files affected |
|------|---------|------------|----------------|
| task_01 | open for proposals | — | — |
| … | up to 10 tasks | — | — |

---

## Leaderboard

Coming soon — published at challenge launch.

---

## What this challenge is about

This is not a marketing exercise. CodeDNA was designed to solve a specific problem: AI agents spend too much of their context budget navigating the wrong files. The hypothesis is that embedding navigation metadata directly in source files — at Level 0, with zero external infrastructure — is enough to measurably improve agent performance.

We already have benchmark data on SWE-bench Django tasks. This challenge invites the community to test the hypothesis on different projects, different models, and different stacks — and to provide controlled evidence for or against it.

If CodeDNA makes no difference on your stack, that is a valid and interesting result. Publish it.

---

## Contact

- GitHub: [@Larens94](https://github.com/Larens94)
- CodeDNA spec & paper: [github.com/Larens94/codedna](https://github.com/Larens94/codedna)
- Questions or task proposals: open an issue in this repo or email [fabrizio.corpora@gmail.com](mailto:fabrizio.corpora@gmail.com)
