"""verify.py — Verify that a submission's patch passes the task tests and compute F1.

exports: compute_f1(touched, ground_truth) -> float | verify(task, submission_dir) -> dict | main()
used_by: none (CLI entry point + GitHub Actions)
rules:   F1 is file-localization only — does NOT measure patch correctness beyond test pass.
         test execution runs in a subprocess inside project/anyio — do NOT import anyio directly.
         results.json is updated in-place with tests_pass and f1_localization.
agent:   claude-sonnet-4-6 | anthropic | 2026-04-27 | s_20260427_challenge | initial scaffold
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def compute_f1(touched: list[str], ground_truth: list[str]) -> float:
    """Compute file-localization F1 between agent-touched files and ground truth.

    Rules:   Both lists are normalized to repo-relative paths before comparison.
             Returns 0.0 if either list is empty.
    """
    if not touched or not ground_truth:
        return 0.0
    touched_set = {Path(f).as_posix() for f in touched}
    gt_set      = {Path(f).as_posix() for f in ground_truth}
    tp = len(touched_set & gt_set)
    precision = tp / len(touched_set)
    recall    = tp / len(gt_set)
    if precision + recall == 0:
        return 0.0
    return round(2 * precision * recall / (precision + recall), 4)


def verify(task: str, submission_dir: Path) -> dict:
    root = Path(__file__).parent.parent
    task_dir  = root / "tasks" / task
    gt_path   = task_dir / "ground_truth.json"
    test_file = task_dir / "failing_test.py"
    results_path = submission_dir / "results.json"

    if not results_path.exists():
        raise FileNotFoundError(f"results.json not found in {submission_dir}")

    results = json.loads(results_path.read_text())
    ground_truth = json.loads(gt_path.read_text())

    # Run tests
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(test_file), "-v", "--tb=short"],
        cwd=root / "project" / "anyio",
        capture_output=True,
        text=True,
    )
    tests_pass = proc.returncode == 0

    # Compute F1
    f1 = compute_f1(
        results.get("files_touched", []),
        ground_truth["files_in_patch"],
    )

    # Update results.json in-place
    results["tests_pass"]      = tests_pass
    results["f1_localization"] = f1
    results_path.write_text(json.dumps(results, indent=2))

    return {"tests_pass": tests_pass, "f1_localization": f1, "stdout": proc.stdout}


def main():
    parser = argparse.ArgumentParser(description="Verify a challenge submission")
    parser.add_argument("--task",       required=True, help="Task ID (e.g. task_01)")
    parser.add_argument("--submission", required=True, help="Path to submission directory")
    args = parser.parse_args()

    result = verify(args.task, Path(args.submission))
    status = "PASS" if result["tests_pass"] else "FAIL"
    print(f"tests:          {status}")
    print(f"f1_localization: {result['f1_localization']}")
    if not result["tests_pass"]:
        print(result["stdout"])
        sys.exit(1)


if __name__ == "__main__":
    main()
