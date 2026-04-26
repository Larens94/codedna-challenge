"""generate.py — Aggregate all submissions/*/results.json into dashboard/leaderboard.json.

exports: load_submissions(root) -> list[dict] | generate(root) -> None | main()
used_by: none (CLI entry point + GitHub Actions)
rules:   Only submissions with tests_pass=true are included in the ranked table.
         All submissions (pass and fail) are included in the raw dump for transparency.
         Sort order: f1_localization DESC, cost_usd ASC.
agent:   claude-sonnet-4-6 | anthropic | 2026-04-27 | s_20260427_challenge | initial scaffold
"""

import json
from datetime import datetime, timezone
from pathlib import Path


def load_submissions(root: Path) -> list[dict]:
    submissions = []
    for path in sorted((root / "submissions").glob("*/results.json")):
        if path.parent.name == "example":
            continue
        try:
            data = json.loads(path.read_text())
            data["_participant"] = path.parent.name
            submissions.append(data)
        except Exception:
            pass
    return submissions


def generate(root: Path) -> None:
    submissions = load_submissions(root)

    passing  = [s for s in submissions if s.get("tests_pass") is True]
    failing  = [s for s in submissions if s.get("tests_pass") is not True]

    # Rules: f1 DESC, cost ASC
    passing.sort(key=lambda s: (-s.get("f1_localization", 0), s.get("cost_usd", 9999)))

    leaderboard = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_submissions": len(submissions),
        "ranked": passing,
        "failed": failing,
    }

    out = root / "dashboard" / "leaderboard.json"
    out.write_text(json.dumps(leaderboard, indent=2))
    print(f"leaderboard.json written — {len(passing)} passing, {len(failing)} failed")


def main():
    root = Path(__file__).parent.parent
    generate(root)


if __name__ == "__main__":
    main()
