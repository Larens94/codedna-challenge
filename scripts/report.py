#!/usr/bin/env python3
"""report.py — Extract metrics from a Claude Code session JSONL and generate results.json.

exports: parse_session(jsonl_path) -> dict | main()
used_by: none (CLI entry point)
rules:   cost formula uses Sonnet 4.6 pricing — update if model changes.
         tests_pass and f1_localization are NOT set here — filled manually or by verify.py.
agent:   claude-sonnet-4-6 | anthropic | 2026-04-27 | s_20260427_challenge | initial scaffold

Usage:
    python scripts/report.py --session ~/.claude/projects/<hash>/<session>.jsonl \
                             --task task_01 \
                             --participant your-github-username \
                             --approach "codedna-v0.9"
"""

import argparse
import json
from datetime import datetime
from pathlib import Path


def parse_session(jsonl_path: Path) -> dict:
    lines = [l for l in jsonl_path.read_text().splitlines() if l.strip()]

    tokens_input = tokens_output = cache_create = cache_read = 0
    tool_calls: dict[str, int] = {}
    timestamps: list[str] = []

    for line in lines:
        event = json.loads(line)
        if event.get("type") != "assistant":
            continue

        msg = event.get("message", {})
        usage = msg.get("usage", {})
        tokens_input  += usage.get("input_tokens", 0)
        tokens_output += usage.get("output_tokens", 0)
        cache_create  += usage.get("cache_creation_input_tokens", 0)
        cache_read    += usage.get("cache_read_input_tokens", 0)

        if ts := event.get("timestamp"):
            timestamps.append(ts)

        for block in msg.get("content", []):
            if isinstance(block, dict) and block.get("type") == "tool_use":
                name = block.get("name", "unknown")
                tool_calls[name] = tool_calls.get(name, 0) + 1

    duration_min = 0.0
    if len(timestamps) >= 2:
        t0 = datetime.fromisoformat(timestamps[0].replace("Z", "+00:00"))
        t1 = datetime.fromisoformat(timestamps[-1].replace("Z", "+00:00"))
        duration_min = (t1 - t0).total_seconds() / 60

    # Stima costo Sonnet 4.6 ($/1M tokens)
    cost = (
        tokens_input  * 3.0
        + cache_create * 3.75
        + cache_read   * 0.30
        + tokens_output * 15.0
    ) / 1_000_000

    return {
        "tokens_input":        tokens_input,
        "tokens_output":       tokens_output,
        "cache_creation":      cache_create,
        "cache_read":          cache_read,
        "cost_usd":            round(cost, 4),
        "tool_calls_total":    sum(tool_calls.values()),
        "tool_calls_breakdown": dict(sorted(tool_calls.items(), key=lambda x: -x[1])),
        "duration_min":        round(duration_min, 1),
    }


def main():
    parser = argparse.ArgumentParser(description="Generate results.json from Claude Code session")
    parser.add_argument("--session",     required=True, help="Path to .jsonl session file")
    parser.add_argument("--task",        required=True, help="Task ID (e.g. task_01)")
    parser.add_argument("--participant", required=True, help="GitHub username")
    parser.add_argument("--approach",    default="codedna-v0.9", help="Config approach label")
    parser.add_argument("--tools",       default="claude-code | claude-sonnet-4-6")
    parser.add_argument("--out",         default=None, help="Output path (default: submissions/<participant>/results.json)")
    args = parser.parse_args()

    session_path = Path(args.session).expanduser()
    if not session_path.exists():
        raise FileNotFoundError(f"Session file not found: {session_path}")

    metrics = parse_session(session_path)

    result = {
        "task":                args.task,
        "participant":         args.participant,
        "approach":            args.approach,
        "tools":               args.tools,
        "config_files":        [],
        **metrics,
        "files_touched":       [],
        "f1_localization":     None,
        "tests_pass":          None,
        "notes":               "",
        "session_jsonl":       str(session_path),
    }

    out_path = Path(args.out) if args.out else Path(f"submissions/{args.participant}/results.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2))

    print(f"results.json written to {out_path}")
    print(f"  tokens:   {metrics['tokens_input']:,} in / {metrics['tokens_output']:,} out / {metrics['cache_read']:,} cache_read")
    print(f"  cost:     ${metrics['cost_usd']}")
    print(f"  tools:    {metrics['tool_calls_breakdown']}")
    print(f"  duration: {metrics['duration_min']} min")
    print()
    print("Next: fill in files_touched, f1_localization, tests_pass, then open a PR.")


if __name__ == "__main__":
    main()
