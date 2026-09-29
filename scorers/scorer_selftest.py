#!/usr/bin/env python3
"""Null/gold/corrupted self-test harness for the ClerkBench scorer.

For every demo instance under ../demo/*.jsonl, this verifies:

  1. A gold reconstruction (the expected files rendered back through the
     scorer's own file-block format) scores strict_correct=True.
  2. A single-byte corruption of one expected file scores strict_correct=False
     with a literal-mismatch-type failure (the per-file diagnostic reports
     ``failure_type == "literal_mismatch"``).
  3. An empty submission scores strict_correct=False with a parse-type
     failure (``failure_type == "parse_failed"``).

This is the same null-submission discipline described in the paper's
Availability paragraph: "the byte-exact artifact grader and its
gold/corrupted/null self-test harness". It exits nonzero if any check fails
for any demo instance.

Usage:
    python scorer_selftest.py [path/to/demo/dir]

Defaults to the ``demo/`` directory alongside this script's parent
(``../demo``).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clerkbench_scorer import score_pilot_output  # noqa: E402

DEFAULT_DEMO_DIR = Path(__file__).resolve().parent.parent / "demo"


def render_expected_output(files: dict[str, str]) -> str:
    """Render expected files using the scorer's own file-block format.

    This is a test-harness helper (not part of the scorer): it exists only
    to reconstruct a "gold" submission text from a task's expected_files so
    the self-test can round-trip it through score_pilot_output.
    """
    return "\n".join(
        f'<<<FILE path="{path}">>>\n{content}\n<<<END FILE>>>' for path, content in files.items()
    )


def corrupt_one_byte(content: str) -> str:
    """Flip a single character in the middle of a string to a distinct byte."""
    if not content:
        # Degenerate case: an empty expected file. Corrupt by adding a byte.
        return "#"
    index = len(content) // 2
    original = content[index]
    # '#' is not alnum-adjacent under case-folding or whitespace-collapsing,
    # so this cannot accidentally satisfy any of the scorer's forgiving
    # classifications (case_mismatch, whitespace_mismatch, etc.) -- it must
    # fall through to a literal mismatch.
    replacement = "#" if original != "#" else "~"
    return content[:index] + replacement + content[index + 1 :]


def load_demo_instances(demo_dir: Path) -> list[dict]:
    instances: list[dict] = []
    for path in sorted(demo_dir.glob("*.jsonl")):
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                instances.append(json.loads(line))
    return instances


def check_instance(task: dict) -> list[str]:
    """Run the three checks for one task; return a list of failure messages."""
    failures: list[str] = []
    task_id = task.get("task_id", "<unknown>")
    expected_files = task["expected_files"]

    # 1. Gold reconstruction must score strict_correct=True.
    gold_output = render_expected_output(expected_files)
    gold_score = score_pilot_output(gold_output, task)
    if gold_score.get("strict_correct") is not True:
        failures.append(
            f"[{task_id}] gold reconstruction did not score strict_correct=True: "
            f"{json.dumps(gold_score)}"
        )

    # 2. Single-byte corruption of one expected file must score
    #    strict_correct=False with a literal-mismatch-type per-file failure.
    corrupt_path = sorted(expected_files)[0]
    corrupted_files = dict(expected_files)
    corrupted_files[corrupt_path] = corrupt_one_byte(corrupted_files[corrupt_path])
    corrupted_output = render_expected_output(corrupted_files)
    corrupted_score = score_pilot_output(corrupted_output, task)
    if corrupted_score.get("strict_correct") is not False:
        failures.append(
            f"[{task_id}] single-byte corruption of {corrupt_path} did not score "
            f"strict_correct=False: {json.dumps(corrupted_score)}"
        )
    else:
        first_mismatch = corrupted_score.get("first_mismatch") or {}
        per_file_failure = first_mismatch.get("failure_type")
        if per_file_failure != "literal_mismatch":
            failures.append(
                f"[{task_id}] single-byte corruption of {corrupt_path} did not "
                f"produce a literal_mismatch-type failure (got "
                f"{per_file_failure!r}): {json.dumps(corrupted_score)}"
            )

    # 3. Empty submission must score strict_correct=False with a parse-type
    #    failure.
    empty_score = score_pilot_output("", task)
    if empty_score.get("strict_correct") is not False:
        failures.append(
            f"[{task_id}] empty output did not score strict_correct=False: "
            f"{json.dumps(empty_score)}"
        )
    elif empty_score.get("failure_type") != "parse_failed":
        failures.append(
            f"[{task_id}] empty output did not produce a parse-type failure "
            f"(got {empty_score.get('failure_type')!r}): {json.dumps(empty_score)}"
        )

    return failures


def main(argv: list[str]) -> int:
    demo_dir = Path(argv[1]) if len(argv) > 1 else DEFAULT_DEMO_DIR
    instances = load_demo_instances(demo_dir)
    if not instances:
        print(f"No demo instances found under {demo_dir}", file=sys.stderr)
        return 2

    all_failures: list[str] = []
    for task in instances:
        all_failures.extend(check_instance(task))

    print(f"Checked {len(instances)} demo instances from {demo_dir}.")
    if all_failures:
        print(f"FAILED: {len(all_failures)} check(s) did not pass:", file=sys.stderr)
        for message in all_failures:
            print(f"  - {message}", file=sys.stderr)
        return 1

    print("PASSED: gold/corrupted/null checks all passed for every demo instance.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
