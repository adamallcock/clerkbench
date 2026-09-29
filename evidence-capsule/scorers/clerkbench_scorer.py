#!/usr/bin/env python3
"""ClerkBench deterministic scorer (self-contained, stdlib-only).

PINNED CAPSULE COPY. The capsule ships its own copy of the scorer so a later
edit to ``release/clerkbench-v1/scorers/clerkbench_scorer.py`` cannot silently
change what ``rebuild.py`` verifies. This copy was UPDATED for the 2026-09
revision (red-team C4): the wrapper tolerance became symmetric — defined by
malformation class rather than by the single malformation one configuration
happened to produce — so the capsule's re-derivation uses the same rule the
published boards are built on. Re-pinning it here is deliberate: leaving the
old rule in the capsule would make the capsule reproduce a board the paper no
longer publishes. The two copies are byte-identical apart from this note.

This module is extracted verbatim (logic-for-logic) from the internal
research harness's scoring functions:

  - ``BLOCKED_RE``, ``blocked_line`` and ``score_pilot_output`` from
    ``scripts/research/reliability_abstention_pilot.py``
  - ``FILE_BLOCK_START_RE``, ``validate_relative_path``,
    ``parse_file_blocks`` and ``score_file_tree`` from
    ``scripts/research/copybench_file_output.py``
  - ``normalize_transport``, ``find_first_diff``, ``classify_wrapper_type``,
    ``_has_source_marker_wrapper``, ``classify_content_error``,
    ``classify_failure``, ``levenshtein_distance`` and ``score_output`` from
    ``scripts/research/copybench_nano_probe.py``

It contains ONLY parsing and scoring code: no task generator, no simulator,
no prompt-building helper, and no provider/network code. Given a task record
(with ``expected_files`` and, for abstention-style tasks, ``expected_block``
and ``variant``) and a raw model output string, it recomputes the score dict
the paper's tables are built from.

Wrapper tolerance (2026-09 revision, red-team C4)
------------------------------------------------
The file-block delimiter is the transport wrapper the harness asks for, not
the clerical work under test, so ``normalize_file_delimiters`` canonicalizes a
malformed delimiter LINE that still unambiguously identifies the intended
marker. That tolerance is defined by MALFORMATION CLASS — 1-3 closing
brackets, internal whitespace after ``<<<`` and around ``END FILE``, trailing
whitespace, and an END marker glued to the end of a content line — and it
applies to EVERY model equally. The previous rule recognised a single
malformation (the two-bracket ``">>`` close), which in practice was one
configuration's slip, so equivalent slips by other models were graded as parse
failures even when every file's content was byte-exact. Nothing about content
grading changed: the bytes between the markers are still compared exactly, and
verdicts re-derived under this scorer supersede any verdict recorded at
collection time under the earlier rule.

Usage:
    python clerkbench_scorer.py <task.json> <output.txt>

``task.json`` must contain (at minimum) the fields ``expected_files`` and,
optionally, ``variant`` and ``expected_block`` (matching the shape of a
ClerkBench task/demo-instance record). ``output.txt`` is the raw model
output text to score. The resulting score dict is printed as JSON.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

# ─── Regexes (module-level constants used by the parsers below) ───

BLOCKED_RE = re.compile(r'<<<BLOCKED reason="([a-z_]+)" item="([^"]+)">>>')
FILE_BLOCK_START_RE = re.compile(r'^<<<FILE path="([^"]+)">>>[ \t]*$', re.MULTILINE)

# Transport-wrapper slip normalization. The file-block delimiter is the
# wrapper WE ask the model to emit, not the model's clerical work, so a
# malformed delimiter that still unambiguously identifies the intended marker
# is canonicalized before parsing — the same treatment ``normalize_transport``
# gives CRLF/whitespace.
#
# The rule is defined by MALFORMATION CLASS, not by model: every output is put
# through the same patterns, and any model that produces one of these slips
# receives the same tolerance (2026-09 revision, red-team C4 — the earlier rule
# recognised only the two-bracket ``">>`` close, which in practice was one
# model's slip, and graded every other model's equivalent slip as a parse
# failure even when each file's content was byte-exact). The classes are:
#
#   * 1-3 closing brackets on either marker (``>``, ``>>``, ``>>>``);
#   * optional internal whitespace after ``<<<`` and around ``END FILE``;
#   * trailing whitespace on the delimiter line;
#   * an END marker glued to the end of a content line with no preceding
#     newline (the newline the parser needs is inserted back).
#
# Four or more brackets are NOT a recognised slip and are left untouched: the
# intent is no longer unambiguous. Every pattern is anchored to a delimiter
# LINE (``^...$`` under re.MULTILINE) — exactly where the parser looks for the
# delimiter — so the fix touches only the wrapper and never a
# ``<<<FILE ...>>`` that happens to appear inside file CONTENT. The content
# between markers is still compared byte-exactly; nothing here forgives a
# clerical error. Canonical delimiters pass through unchanged, so the whole
# pass is a no-op for any output already emitting ``>>>``.
FILE_OPEN_DELIM_RE = re.compile(
    r'^<<<[ \t]*FILE[ \t]+path="([^"]+)"[ \t]*>{1,3}[ \t]*$', re.MULTILINE
)
END_FILE_DELIM_RE = re.compile(r'^<<<[ \t]*END[ \t]+FILE[ \t]*>{1,3}[ \t]*$', re.MULTILINE)
# Zero-width: an END marker that begins mid-line (the previous character is not
# a newline). Substituting a newline at that position restores the line break
# the parser's ``"\n<<<END FILE>>>"`` end marker requires.
END_FILE_GLUED_RE = re.compile(
    r'(?<=[^\n])(?=<<<[ \t]*END[ \t]+FILE[ \t]*>{1,3}[ \t]*$)', re.MULTILINE
)


# ─── Abstention escape-hatch helper ───


def blocked_line(reason: str, item: str) -> str:
    return f'<<<BLOCKED reason="{reason}" item="{item}">>>'


# ─── Path safety ───


def validate_relative_path(path: str) -> None:
    """Reject unsafe output paths."""
    pure = Path(path)
    if pure.is_absolute() or ".." in pure.parts or not path or "\\" in path:
        raise ValueError(f"Unsafe relative path: {path!r}")


# ─── File-block parsing ───


def normalize_file_delimiters(output: str) -> str:
    """Transport-wrapper normalization for the file-block delimiter.

    Applied to the raw output BEFORE the block boundaries are located, so it
    only ever touches the delimiter wrapper: any delimiter LINE that
    unambiguously identifies the intended marker is rewritten to its canonical
    form, ``<<<FILE path="...">>>`` or ``<<<END FILE>>>``. The tolerance is
    defined by MALFORMATION CLASS and applies to every model equally — 1-3
    closing brackets, internal whitespace after ``<<<`` and around
    ``END FILE``, trailing whitespace, and an END marker glued to the end of a
    content line (see the comment block above the patterns).

    This is the same transport treatment as ``normalize_transport``'s
    CRLF/whitespace handling: we grade the file CONTENT between the delimiters
    byte-exactly, but we tolerate a malformed wrapper our own harness asked the
    model to produce. Canonical delimiters are rewritten to themselves, so the
    pass is a no-op for any output already emitting ``>>>``.
    """
    output = END_FILE_GLUED_RE.sub("\n", output)
    output = FILE_OPEN_DELIM_RE.sub(r'<<<FILE path="\1">>>', output)
    output = END_FILE_DELIM_RE.sub("<<<END FILE>>>", output)
    return output


def parse_file_blocks(output: str) -> tuple[dict[str, str], dict[str, Any]]:
    """Parse ``<<<FILE path="...">>> ... <<<END FILE>>>`` blocks from model output."""
    output = normalize_file_delimiters(output)
    matches = list(FILE_BLOCK_START_RE.finditer(output))
    if not matches:
        return {}, {"parse_ok": False, "extra_text": output.strip(), "errors": ["no_file_blocks"]}

    files: dict[str, str] = {}
    errors: list[str] = []
    consumed_ranges: list[tuple[int, int]] = []
    for match_index, match in enumerate(matches):
        path = match.group(1)
        try:
            validate_relative_path(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        content_start = match.end()
        if content_start < len(output) and output[content_start] == "\n":
            content_start += 1
        next_start = (
            matches[match_index + 1].start()
            if match_index + 1 < len(matches)
            else len(output)
        )
        segment = output[content_start:next_start]
        end_marker = "\n<<<END FILE>>>"
        end_index = segment.find(end_marker)
        if end_index < 0:
            errors.append(f"missing end marker for {path}")
            continue
        content = segment[:end_index]
        consumed_end = content_start + end_index + len(end_marker)
        consumed_ranges.append((match.start(), consumed_end))
        if path in files:
            errors.append(f"duplicate file block for {path}")
            continue
        files[path] = content

    extra_parts: list[str] = []
    cursor = 0
    for start, end in consumed_ranges:
        extra_parts.append(output[cursor:start])
        cursor = end
    extra_parts.append(output[cursor:])
    extra_text = "".join(extra_parts).strip()
    return files, {
        "parse_ok": not errors,
        "extra_text": extra_text,
        "errors": errors,
    }


# ─── Per-file literal comparison and diff diagnostics ───


def normalize_transport(text: str) -> str:
    """Normalize transport newlines without otherwise forgiving the output."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def find_first_diff(output: str, target: str) -> dict[str, Any]:
    """Return the first differing offset and characters."""
    for index, (observed, expected) in enumerate(zip(output, target, strict=False)):
        if observed != expected:
            return {"index": index, "expected": expected, "observed": observed}
    if len(output) == len(target):
        return {"index": None, "expected": None, "observed": None}
    index = min(len(output), len(target))
    return {
        "index": index,
        "expected": target[index] if index < len(target) else None,
        "observed": output[index] if index < len(output) else None,
    }


def _has_source_marker_wrapper(before: str, after: str) -> bool:
    """Return whether before/after look like copied source delimiters."""
    marker_tokens = [
        "BEGIN_",
        "END_",
        "<",
        "</",
        "SOURCE",
        "[[",
        "---",
    ]
    if not before or not after:
        return False
    return any(token in before for token in marker_tokens) and any(
        token in after for token in marker_tokens
    )


def classify_wrapper_type(output: str, target: str) -> str:
    """Classify exact-target-in-extra-text failures for diagnostics."""
    if output == target or target not in output:
        return "none"
    if output == f"{target}\n":
        return "terminal_newline"
    if output.strip() == target:
        return "outer_whitespace"
    if output.count(target) > 1:
        return "repeat_extra"

    before, _match, after = output.partition(target)
    before_stripped = before.strip()
    after_stripped = after.strip()
    stripped_output = output.strip()

    if stripped_output.startswith("```") and stripped_output.endswith("```"):
        return "code_fence"
    if _has_source_marker_wrapper(before_stripped, after_stripped):
        return "source_marker"
    if before_stripped and not after_stripped:
        return "label_prefix"
    if after_stripped and not before_stripped:
        return "label_suffix"
    if before_stripped or after_stripped:
        return "explanation"
    return "target_present_extra_text"


def classify_content_error(
    output: str,
    target: str,
    *,
    strict_correct: bool,
    wrapper_type: str,
) -> str:
    """Classify content-oriented errors without replacing strict correctness."""
    if strict_correct:
        return "none"
    if wrapper_type != "none":
        return "output_contract"
    if not output.strip():
        return "non_answer"
    if output in target:
        return "missing_content"
    if output.casefold() == target.casefold():
        return "case_drift"
    if "".join(output.split()) == "".join(target.split()):
        return "whitespace_drift"
    return "literal_content_mismatch"


def classify_failure(output: str, target: str, strict_correct: bool) -> str:
    """Classify common exact-copy failure modes."""
    if strict_correct:
        return "none"
    if not output.strip():
        return "non_answer"
    if output == f"{target}\n":
        return "terminal_newline_only"
    if output.strip() == target.strip():
        return "outer_whitespace_mismatch"
    if output in target:
        return "subsection_only"
    wrapper_type = classify_wrapper_type(output, target)
    if wrapper_type != "none":
        return f"target_present_{wrapper_type}"
    if target in output:
        return "target_present_extra_text"
    if output.casefold() == target.casefold():
        return "case_mismatch"
    if "".join(output.split()) == "".join(target.split()):
        return "whitespace_mismatch"
    if output.upper() == target.upper() or output.lower() == target.lower():
        return "case_transform_drift"
    return "literal_mismatch"


def levenshtein_distance(left: str, right: str) -> int:
    """Compute edit distance for diagnostics; not used for correctness."""
    if left == right:
        return 0
    if len(left) < len(right):
        left, right = right, left
    previous = list(range(len(right) + 1))
    for left_index, left_char in enumerate(left, start=1):
        current = [left_index]
        for right_index, right_char in enumerate(right, start=1):
            insert_cost = current[right_index - 1] + 1
            delete_cost = previous[right_index] + 1
            replace_cost = previous[right_index - 1] + (left_char != right_char)
            current.append(min(insert_cost, delete_cost, replace_cost))
        previous = current
    return previous[-1]


def score_output(output: str, target: str) -> dict[str, Any]:
    """Score exact string output and return useful failure-mining diagnostics."""
    normalized_output = normalize_transport(output)
    normalized_target = normalize_transport(target)
    strict_correct = normalized_output == normalized_target
    first_diff = find_first_diff(normalized_output, normalized_target)
    target_count = normalized_output.count(normalized_target) if normalized_target else 0
    terminal_newline_only = normalized_output == f"{normalized_target}\n"
    strict_text_v0 = strict_correct or terminal_newline_only
    wrapper_type = classify_wrapper_type(normalized_output, normalized_target)
    return {
        "strict_correct": strict_correct,
        "raw_exact": output == target,
        "strict_text_v0": strict_text_v0,
        "target_present": normalized_target in normalized_output,
        "target_count": target_count,
        "terminal_newline_only": terminal_newline_only,
        "wrapper_type": wrapper_type,
        "content_error_type": classify_content_error(
            normalized_output,
            normalized_target,
            strict_correct=strict_correct,
            wrapper_type=wrapper_type,
        ),
        "output_is_target_substring": bool(normalized_output)
        and normalized_output in normalized_target
        and not strict_correct,
        "output_length": len(normalized_output),
        "target_length": len(normalized_target),
        "length_delta": len(normalized_output) - len(normalized_target),
        "first_diff_index": first_diff["index"],
        "first_diff_expected": first_diff["expected"],
        "first_diff_observed": first_diff["observed"],
        "failure_type": classify_failure(normalized_output, normalized_target, strict_correct),
        "edit_distance": levenshtein_distance(normalized_output, normalized_target),
    }


# ─── File-tree scoring ───


def score_file_tree(output: str, expected_files: dict[str, str]) -> dict[str, Any]:
    """Score parsed file blocks against expected file contents."""
    observed_files, parse = parse_file_blocks(output)
    expected_paths = set(expected_files)
    observed_paths = set(observed_files)
    missing = sorted(expected_paths - observed_paths)
    extra = sorted(observed_paths - expected_paths)
    per_file: dict[str, Any] = {}
    mismatched: list[str] = []
    for path in sorted(expected_paths & observed_paths):
        file_score = score_output(observed_files[path], expected_files[path])
        per_file[path] = file_score
        if not file_score["strict_correct"]:
            mismatched.append(path)
    files_exact = (
        bool(parse["parse_ok"])
        and not missing
        and not extra
        and not mismatched
    )
    format_exact = files_exact and not parse["extra_text"]
    if not parse["parse_ok"]:
        failure_type = "parse_failed"
    elif missing:
        failure_type = "missing_files"
    elif extra:
        failure_type = "extra_files"
    elif mismatched:
        failure_type = "file_mismatch"
    elif parse["extra_text"]:
        failure_type = "output_contract_extra_text"
    else:
        failure_type = "none"
    first_mismatch = mismatched[0] if mismatched else None
    return {
        "strict_correct": files_exact and format_exact,
        "answer_correct": files_exact,
        "files_exact": files_exact,
        "format_exact": format_exact,
        "failure_type": failure_type,
        "missing_files": missing,
        "extra_files": extra,
        "mismatched_files": mismatched,
        "first_mismatch_file": first_mismatch,
        "first_mismatch": per_file.get(first_mismatch) if first_mismatch else None,
        "expected_file_count": len(expected_files),
        "observed_file_count": len(observed_files),
        "parse": parse,
        "per_file": per_file,
    }


# ─── Top-level entry point: ok/blocked pilot scoring ───


def score_pilot_output(output: str, task: dict[str, Any]) -> dict[str, Any]:
    """Score one model output for an ok or blocked ClerkBench task.

    ``task`` must provide ``expected_files`` (dict[str, str]) for "ok"
    variant tasks, and ``expected_block`` (dict with ``reason``/``item``)
    for "blocked" variant tasks. Tasks without a ``variant`` field are
    treated as "ok".
    """
    match = BLOCKED_RE.search(output)
    observed_files, _parse = parse_file_blocks(output)
    if task.get("variant", "ok") == "ok":
        if match and not observed_files:
            return {
                "strict_correct": False,
                "answer_correct": False,
                "failure_type": "false_block",
                "observed_block": {"reason": match.group(1), "item": match.group(2)},
            }
        score = score_file_tree(output, dict(task["expected_files"]))
        if match:
            score["failure_type"] = (
                score["failure_type"] if score["failure_type"] != "none" else "block_plus_files"
            )
            score["strict_correct"] = False
        return score
    expected_block = dict(task["expected_block"])
    if observed_files:
        return {
            "strict_correct": False,
            "answer_correct": False,
            "failure_type": "fabrication",
            "observed_file_count": len(observed_files),
        }
    if not match:
        return {
            "strict_correct": False,
            "answer_correct": False,
            "failure_type": "missing_block",
        }
    observed = {"reason": match.group(1), "item": match.group(2)}
    block_exact = observed == expected_block
    format_exact = output.strip() == blocked_line(**expected_block)
    if block_exact:
        failure_type = "none" if format_exact else "block_extra_text"
    else:
        failure_type = "block_wrong_details"
    return {
        "strict_correct": block_exact and format_exact,
        "answer_correct": block_exact,
        "failure_type": failure_type,
        "observed_block": observed,
        "expected_block": expected_block,
    }


def _main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(f"usage: {argv[0]} <task.json> <output.txt>", file=sys.stderr)
        return 2
    task_path, output_path = Path(argv[1]), Path(argv[2])
    task = json.loads(task_path.read_text(encoding="utf-8"))
    output = Path(output_path).read_text(encoding="utf-8")
    score = score_pilot_output(output, task)
    print(json.dumps(score, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv))
