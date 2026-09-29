#!/usr/bin/env python3
"""One-command rebuild of the published ClerkBench-v1 boards.

    $ cd release/clerkbench-v1/evidence-capsule
    $ python3 rebuild.py

Recomputes, from capsule contents alone:

  * Table 4 — the ClerkBench-CH6 v1 board (founding families): ordinal
    ranks, CH6 with censoring qualifiers, capability horizon, and both R18
    cost columns ($ per L=100 attempt and oracle-verified $ per success);
  * Table 5 — the four-family ClerkBench-CH6-4fam v1 board;
  * ``leaderboard.csv`` — the Table 4 board as structured data, field by
    field (``ch6`` and ``capability`` at three decimals, so every downstream
    renderer rounds once from the same value — red-team M3).

…and asserts that every recomputed line is byte-identical to the
corresponding line of the shipped ``aggregates/tables.md`` /
``aggregates/leaderboard.csv``.

It also re-derives ``strict_correct`` for every v1 attempt straight from the
raw model output and the task's ``expected_files``, using the public scorer
frozen at ``scorers/clerkbench_scorer.py`` (a pinned copy shipped inside the
capsule itself, so a later edit to the release's shared scorer can never
silently change what a rebuild verifies; the copy was re-pinned for the
2026-09 revision — see its header).

That re-derivation is the AUTHORITY for every number below, not a
cross-check. The 2026-09 revision made the wrapper tolerance symmetric
(red-team C4), so a verdict the harness recorded at collection time can
legitimately differ from what today's scorer computes, and the raw logs are
immutable — the correction lives in the scorer and is applied at load time.
Rows whose recorded verdict differs are counted and printed as PROVENANCE,
not as a failure.

v1 differences from the v0 capsule:

  * No supersede or adjudication machinery. The eight v1 run dirs are the
    canonical collection in full — every pre-v1 row for a v1-roster config
    was purged upstream (DeepSeek checkpoint change; OpenAI-roster fresh
    collection on the frozen v1 tasks), and no v1 score was adjudicated.
    ``attempts/`` therefore ships the raw run logs verbatim, one file per
    (run dir, task manifest, config), prefixed with the run dir name.
  * Measurement-doctrine exclusions are applied at load time instead of via
    a shipped ``excluded_rows.jsonl``, and since the 2026-09 revision they
    are decided on the ARTIFACT rather than on the provider's finish reason
    (red-team M27 / M28 / m54). Rows with a truthy ``error`` and rows with
    neither a response nor a score are unmeasured and drop at load. Every
    other row is re-scored, and then: an attempt that emitted a COMPLETE
    parseable artifact is assessable and is scored whatever its finish
    reason; otherwise an attempt carrying a budget signal — ``length`` /
    ``max_tokens``, or an empty completion whose reasoning consumed >= 95%
    of the output tokens — is unmeasurable and is excluded, never a zero;
    otherwise it is a failure and is scored as one. Each branch is reported
    by count. The raw rows stay in ``attempts/`` untouched.
  * Task records are resolved per SOURCE MANIFEST, not globally by id: the
    frozen v1 task set carries 18 founding task ids whose ``founding_3inst``
    and ``founding_6inst`` records differ in content (L100–L400 RNG drift,
    caught 2026-08-16/17; only the six-instance DeepSeek-V4-Flash founding
    tier used ``founding_6inst``). The DATA-level inconsistency was fixed
    by re-collection on 2026-08-17: those 18 instances were re-run for
    DeepSeek-V4-Flash on the canonical ``founding_3inst`` content
    (``dsflash_content_fix``, 108 attempts, all completed), and the 108
    superseded 6inst-content rows were retired from the run log (the
    pre-trim log is preserved in git, commit 02e4810). Every config's
    instances 000001–000003 therefore answered 3inst-equivalent content.
    The manifest-level divergence remains a property of the two task FILES:
    each attempts file names the manifest its run was served from, rebuild
    scores each row against that manifest's record, asserts the divergence
    is confined to the known manifest set, and verifies the fix manifest is
    byte-identical to ``founding_3inst`` on every id it carries.

Requirements: Python 3.9+, standard library only. No network. Every file
read is inside this directory except ``../aggregates/tables.md`` and
``../aggregates/leaderboard.csv`` (the assertion targets, read only for a
byte-equality cross-check); verified copies travel in ``manifests/`` and are
used automatically if the sibling directory is absent.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
RELEASE = HERE.parent

# The capsule ships its own pinned copy of the public scorer (self-contained:
# a later edit to ../scorers/clerkbench_scorer.py, e.g. a grading bugfix,
# must not silently change what a rebuild verifies). Fall back to the
# release-wide copy only if the capsule's own copy is somehow absent.
_LOCAL_SCORERS = HERE / "scorers"
_SCORERS_DIR = _LOCAL_SCORERS if (_LOCAL_SCORERS / "clerkbench_scorer.py").exists() else RELEASE / "scorers"
sys.path.insert(0, str(_SCORERS_DIR))
try:
    import clerkbench_scorer
    from clerkbench_scorer import score_pilot_output
except ImportError:  # pragma: no cover
    sys.exit(
        "FATAL: cannot import the public scorer. rebuild.py expects a copy of "
        "clerkbench_scorer.py either in the capsule's own scorers/ directory "
        "or next to the capsule, in ../scorers/."
    )

# The scorer computes a Levenshtein edit distance per file purely as a
# failure-mining diagnostic ("not used for correctness", per its own
# docstring). It is quadratic in file length, which at L=400 means ~40 kB
# strings and hours of pure-Python work over 3000+ attempts. The bulk pass
# below stubs it out; a subsample is then re-scored with the real function
# to demonstrate that no verdict depends on it.
_REAL_LEVENSHTEIN = clerkbench_scorer.levenshtein_distance


def _stub_levenshtein(left: str, right: str) -> int:
    return 0 if left == right else -1

FAIL: list[str] = []


def check(ok: bool, label: str, detail: str = "") -> bool:
    if not ok:
        FAIL.append(f"{label}: {detail}" if detail else label)
    return ok


# ─────────────────────────── capsule contents ───────────────────────────


def load_json(rel: str):
    return json.loads((HERE / rel).read_text(encoding="utf-8"))


def load_jsonl(path: Path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


CANON = load_json("manifests/canonicality.json")
PRICES = {k: tuple(v) for k, v in load_json("manifests/prices.json")["prices"].items()}

FOUNDING_FAMILIES = CANON["founding_families"]
FAMILIES = CANON["families"]
SIZES = CANON["sizes"]
WIDE = CANON["width_confounded_size"]
# Crossing ladder per family (red-team M11, 2026-09 revision). Every crossing
# — capability and CH6, founding board and four-family board — iterates the
# rungs the family was actually measured on. L=800 is excluded everywhere
# (it mixes length with state width); L=25 exists only on payroll and enters
# that family's crossings there. Mirrors
# scripts/research/build_report_tables.crossing_rungs().
CROSSING_RUNGS = [L for L in SIZES if L != WIDE]
FAMILY_CROSSING_RUNGS = {
    "payroll_overtime_ledger": CANON.get("calibration_rungs_not_in_tables", []) + CROSSING_RUNGS,
}


def crossing_rungs(family: str):
    return FAMILY_CROSSING_RUNGS.get(family, CROSSING_RUNGS)
CONFIG_ORDER_HINT = CANON["config_order_hint"]
V1_ROSTER = {tuple(c) for c in CANON["v1_roster"]}
PROVISIONAL_THRESHOLD = CANON["provisional_founding_attempt_threshold"]
CANONICAL_RUN_DIRS = CANON["canonical_run_dirs"]
KNOWN_DIVERGENT_MANIFESTS = frozenset(CANON["known_divergent_task_manifests"])

# Board presentation: the v1 roster has no availability-dominated row and no
# route-comparison row (Fable 5 and the OpenRouter Opus re-collection left
# the roster), so those v0 classes are empty here; the machinery is kept so
# the rendering mirrors build_report_tables.py line for line.
AVAILABILITY_DOMINATED: set = set()
ROUTE_COMPARISON: dict = {}
BOARD_CLASS_ORDER = {"ranked": 0, "availability-dominated": 0,
                     "route-comparison": 2, "bound": 3}
RANKED_BLOCK = ("ranked", "availability-dominated")


# ───────────────────────────── hash integrity ────────────────────────────


def verify_hashes() -> None:
    manifest_path = HERE / "HASHES.json"
    if not manifest_path.exists():
        print("  HASHES.json absent — skipping integrity check")
        return
    expected = json.loads(manifest_path.read_text(encoding="utf-8"))["files"]
    on_disk = {
        str(p.relative_to(HERE))
        for p in HERE.rglob("*")
        if p.is_file() and p.name != "HASHES.json" and "__pycache__" not in p.parts
    }
    missing = sorted(set(expected) - on_disk)
    extra = sorted(on_disk - set(expected))
    bad = []
    for rel, want in sorted(expected.items()):
        f = HERE / rel
        if not f.exists():
            continue
        got = hashlib.sha256(f.read_bytes()).hexdigest()
        if got != want:
            bad.append(rel)
    check(not missing, "HASHES.json", f"{len(missing)} listed file(s) missing: {missing[:3]}")
    check(not extra, "HASHES.json", f"{len(extra)} unlisted file(s) present: {extra[:3]}")
    check(not bad, "HASHES.json", f"{len(bad)} file(s) with a changed digest: {bad[:3]}")
    print(f"  {len(expected)} files hashed, {len(bad)} mismatched, "
          f"{len(missing)} missing, {len(extra)} unlisted")


# ──────────────────────────── row assembly ───────────────────────────────


BUDGET_EXHAUSTED_REASONING_FRACTION = 0.95
# The output cap every direct provider was configured with. An empty
# completion at or near this count reached the cap the harness set.
DECLARED_OUTPUT_CAP = 131072
BUDGET_CAP_FRACTION = 0.90
# A stop point is a ceiling when this many attempts of one model land within
# BUDGET_CEILING_TOLERANCE of each other.
BUDGET_CEILING_TOLERANCE = 0.01
BUDGET_CEILING_MIN_CLUSTER = 3
# Per-model ceiling stop points, filled by set_ceiling_stops() once the corpus
# is loaded. budget_signal() reads it.
CEILING_STOPS = {}


def _reasoning_fraction(row):
    """reasoning_tokens / output_tokens, or None when the provider did not
    report the split."""
    usage = row.get("usage") or {}
    out = usage.get("output_tokens") or 0
    reasoning = (usage.get("output_tokens_details") or {}).get("reasoning_tokens")
    if not out or reasoning is None:
        return None
    return reasoning / out


def complete_artifact(row):
    """Did this attempt emit a COMPLETE parseable artifact — parse_ok and no
    missing file? Assessability turns on this, not on the provider's stop
    string. Read from the RE-DERIVED score, so the symmetric wrapper rule is
    already applied (see rescore())."""
    score = row.get("score") or {}
    if not score:
        return False
    if not (score.get("parse") or {}).get("parse_ok"):
        return False
    return not score.get("missing_files")


def empty_completion_tokens(row):
    """output_tokens for an attempt that emitted nothing visible and spent
    essentially the whole turn reasoning, else None."""
    if (row.get("output") or "").strip():
        return None
    frac = _reasoning_fraction(row)
    if frac is None or frac < BUDGET_EXHAUSTED_REASONING_FRACTION:
        return None
    return (row.get("usage") or {}).get("output_tokens") or None


def set_ceiling_stops(rows):
    """Per model, the output-token counts at which a turn demonstrably ended on
    a configured ceiling rather than on the model's own choice.

    A model does not stop at the same token count by chance. Group one MODEL's
    empty completions into bands of +/-1%; a band holding at least
    BUDGET_CEILING_MIN_CLUSTER attempts is a ceiling. Grouping is by model, not
    by (model, effort), because a thinking budget is a property of the model:
    gemini-3.7-flash stops at the same ~62,920 count at high and at medium.

    Mirrors scripts/research/build_report_tables.thinking_ceiling_stops()."""
    by_model = {}
    for r in rows:
        tok = empty_completion_tokens(r)
        if tok is not None:
            by_model.setdefault(str(r.get("model", "")), []).append(tok)
    CEILING_STOPS.clear()
    for model, toks in by_model.items():
        CEILING_STOPS[model] = {
            v for v in toks
            if sum(1 for u in toks if abs(u - v) <= v * BUDGET_CEILING_TOLERANCE)
            >= BUDGET_CEILING_MIN_CLUSTER
        }
    return CEILING_STOPS


def budget_signal(row):
    """The budget signal on this attempt, or None.

    Two forms of one event. "budget_status" is the provider saying so (length /
    max_tokens). "budget_empty" is the same exhaustion under a different status
    string: nothing visible was emitted, the reasoning trace consumed
    essentially the whole turn, AND the turn ended at a limit — a ceiling this
    model demonstrably returns to, or the declared output cap. An empty
    completion that meets neither is the model returning nothing, which is a
    failure an operator observes, and it is scored (red-team M28/m54
    follow-up)."""
    if str(row.get("response_status", "")).lower() in ("length", "max_tokens"):
        return "budget_status"
    tok = empty_completion_tokens(row)
    if tok is None:
        return None
    if tok in CEILING_STOPS.get(str(row.get("model", "")), ()):
        return "budget_empty"
    if tok >= BUDGET_CAP_FRACTION * DECLARED_OUTPUT_CAP:
        return "budget_empty"
    return None


def apply_assessability(rows):
    """Split re-scored rows into scored and unmeasurable (red-team M27 / M28 /
    m54, 2026-09 revision). Assessability is decided on the ARTIFACT, not on
    the provider's finish reason:

      1. A COMPLETE parseable artifact (parse_ok, no missing file) is
         assessable and is SCORED, whatever the finish reason — a response
         that carried every expected file is measurable evidence, and
         discarding it because the provider also said "max_tokens" threw away
         correct work.
      2. Otherwise a budget signal makes the attempt UNMEASURABLE: excluded,
         never scored as a zero (doctrine 2026-07-19, red-team C3).
      3. Otherwise it is a FAILURE and is scored as one — which is what keeps
         API-level refusals and ordinary truncations in the denominator, as
         an unattended operator would see them.

    Must be called AFTER rescore(), so branch 1 reads the re-derived artifact
    state rather than the verdict recorded at collection time.
    """
    kept, n_status, n_empty, n_restored = [], 0, 0, 0
    for r in rows:
        signal = budget_signal(r)
        if signal is None:
            kept.append(r)
            continue
        if complete_artifact(r):
            n_restored += 1
            kept.append(r)
            continue
        if signal == "budget_status":
            n_status += 1
        else:
            n_empty += 1
    print(f"  assessability: {n_restored} attempt(s) carried a complete artifact "
          f"despite a budget signal and are SCORED")
    print(f"  assessability: {n_status + n_empty} attempt(s) excluded as unmeasurable "
          f"({n_status} by response_status length/max_tokens, {n_empty} empty "
          f"completion that ended at a thinking ceiling or at the declared "
          f"output cap)")
    print(f"  {len(kept)} assessable attempts enter the cells")
    return kept


def load_rows():
    """Capsule attempt rows, transport doctrine applied at load.

    Each attempts file is the verbatim run log named
    ``<run_dir>__<manifest>-<config>.jsonl``; the run dir and source task
    manifest are recovered from the filename and stamped on every row. Rows
    with a truthy ``error``, and rows with neither a response nor a score, are
    unmeasured attempts: counted here, never scored.

    Budget-signalled rows are NOT dropped here any more. Whether an attempt is
    assessable now depends on what it emitted, which is only known after the
    re-scoring pass, so that split happens in apply_assessability() (red-team
    M27 / M28 / m54).
    """
    index = CANON["attempts_files"]
    files = sorted(p.name for p in (HERE / "attempts").glob("*.jsonl"))
    check(files == sorted(index), "attempts/",
          "files on disk differ from manifests/canonicality.json")
    kept, n_error, n_transport, n_capped, n_dupes = [], 0, 0, 0, 0
    best = {}
    for name in files:
        entry = index.get(name)
        if entry is None:
            continue
        rs = load_jsonl(HERE / "attempts" / name)
        check(
            len(rs) == entry["rows"],
            f"attempts/{name}",
            f"canonicality.json says {entry['rows']} rows, file has {len(rs)}",
        )
        run_dir = name.split("__", 1)[0]
        check(run_dir == entry["source_run_dir"], f"attempts/{name}",
              f"filename prefix {run_dir} != recorded source run dir "
              f"{entry['source_run_dir']}")
        manifest = name.split("__", 1)[1].split("-", 1)[0]
        for r in rs:
            if not str(r.get("profile", "")).startswith("ladder_L"):
                continue
            r["_run_dir"], r["_manifest"], r["_file"] = run_dir, manifest, name
            # Dedupe on the slot key, preferring non-error rows — mirrors
            # build_report_tables.main(). The purged v1 dirs should carry
            # zero collisions; any collision found is counted and reported.
            key = (r["model"], r["reasoning_effort"], r["task_id"], r["attempt_index"])
            cur = best.get(key)
            if cur is None:
                best[key] = r
            else:
                n_dupes += 1
                if cur.get("error") and not r.get("error"):
                    best[key] = r
    for r in best.values():
        if r.get("error"):
            n_error += 1  # transport-level failure recorded by the runner
            continue
        if not (r.get("score") or {}) and not (r.get("output") or "").strip():
            n_transport += 1  # no response and no score: unmeasured attempt
            continue
        kept.append(r)
    set_ceiling_stops(kept)
    n_capped = sum(1 for r in kept if budget_signal(r) is not None)
    check(n_dupes == 0, "slot uniqueness",
          f"{n_dupes} duplicate (model, effort, task, attempt) slot(s) in the "
          "purged v1 run dirs")
    print(f"  {len(best)} raw attempt rows in {len(files)} run files")
    print(f"  excluded as unmeasured: {n_error} error, {n_transport} transport")
    print(f"  {len(kept)} attempts carried forward ({n_capped} of them carry a "
          f"budget signal, resolved by apply_assessability); "
          f"{n_dupes} slot collisions")
    return kept


def load_tasks():
    """Task records keyed by (source manifest, task_id).

    The v1 frozen set has 18 founding ids whose founding_3inst and
    founding_6inst records differ in content, so a flat id-keyed dict would
    silently score six-instance rows against three-instance records (or
    vice versa). Every attempts file names its manifest; scoring goes
    through that manifest's record. Any content divergence OUTSIDE the
    known manifest pair is a capsule defect and fails the rebuild.
    """
    index = CANON["tasks_files"]
    paths = sorted((HERE / "tasks").glob("*.jsonl")) + sorted(
        (HERE / "tasks/topups").glob("*.jsonl")
    )
    check(sorted(p.stem for p in paths) == sorted(index), "tasks/",
          "files on disk differ from manifests/canonicality.json")
    manifests: dict[str, dict] = {}
    by_id: dict[str, dict[str, str]] = defaultdict(dict)
    for p in paths:
        ts = load_jsonl(p)
        entry = index.get(p.stem)
        if entry is not None:
            check(len(ts) == entry["rows"], f"tasks/{p.name}",
                  f"canonicality.json says {entry['rows']} records, file has {len(ts)}")
        manifests[p.stem] = {t["task_id"]: t for t in ts}
        for t in ts:
            by_id[t["task_id"]][p.stem] = hashlib.sha256(
                json.dumps(t, sort_keys=True).encode()
            ).hexdigest()
    divergent_sets = set()
    n_divergent_ids = 0
    for tid, per_manifest in by_id.items():
        if len(set(per_manifest.values())) > 1:
            n_divergent_ids += 1
            divergent_sets.add(frozenset(per_manifest))
    check(
        all(s <= KNOWN_DIVERGENT_MANIFESTS for s in divergent_sets),
        "task manifests",
        f"content divergence outside the known manifest set: {sorted(divergent_sets, key=sorted)}",
    )
    check(
        n_divergent_ids == CANON["known_divergent_task_id_count"],
        "task manifests",
        f"{n_divergent_ids} divergent task ids, canonicality.json records "
        f"{CANON['known_divergent_task_id_count']}",
    )
    # The 2026-08-17 content fix: the re-collection manifest must be
    # byte-identical to the canonical founding_3inst record for every id it
    # carries — that identity is what makes every config's instances
    # 000001–000003 comparable again.
    fix_name = CANON.get("content_fix_manifest")
    if fix_name:
        ref_name = CANON["content_fix_matches"]
        bad = [tid for tid in manifests.get(fix_name, {})
               if by_id[tid].get(fix_name) != by_id[tid].get(ref_name)]
        check(not bad, "content fix",
              f"{len(bad)} {fix_name} record(s) differ from {ref_name}: {bad[:3]}")
        print(f"  {len(manifests.get(fix_name, {}))} re-collected ids in "
              f"{fix_name} verified byte-identical to {ref_name}")
    n_records = sum(len(m) for m in manifests.values())
    print(f"  {len(manifests)} task manifests, {n_records} records, "
          f"{len(by_id)} distinct task ids")
    print(f"  {n_divergent_ids} ids diverge across "
          f"{sorted(KNOWN_DIVERGENT_MANIFESTS)} (known; resolved per source "
          f"manifest)")
    return manifests


# ─────────────────────── independent re-scoring pass ─────────────────────


def _verdict(row, task):
    got = score_pilot_output(row.get("output") or "", task)
    return bool(got["strict_correct"]), got.get("failure_type")


def rescore(rows, manifests) -> None:
    """Re-derive every verdict from raw output + expected_files, and ADOPT it.

    The re-derivation is the AUTHORITY, not a cross-check against the verdict
    the harness recorded at collection time. It has to be: the 2026-09 revision
    made the wrapper tolerance symmetric (red-team C4), so a verdict recorded
    under the old one-malformation rule can legitimately differ from what the
    published scorer computes today, and the raw run logs are immutable — the
    correction is applied here, at load time, and nowhere else. Each row's
    ``score`` is replaced with the re-derived score dict, so everything
    downstream (assessability, cells, both boards) reads one scorer.

    A disagreement with the recorded verdict is therefore PROVENANCE, not a
    failure: it is counted, broken down by direction, and printed. What still
    fails the rebuild is a missing task record (nothing to score against) or a
    verdict that depends on the stubbed edit-distance diagnostic.
    """
    moved, moved_to_correct = [], 0
    clerkbench_scorer.levenshtein_distance = _stub_levenshtein
    try:
        for r in rows:
            task = manifests.get(r["_manifest"], {}).get(r["task_id"])
            if task is None:
                check(False, "re-scoring",
                      f"no task record for {r['task_id']} in manifest {r['_manifest']}")
                return
            recorded = r["score"]
            score = score_pilot_output(r.get("output") or "", task)
            correct, failure = bool(score["strict_correct"]), score.get("failure_type")
            r["_rescored"] = (correct, failure)
            r["_recorded_strict_correct"] = bool(recorded.get("strict_correct"))
            if correct != bool(recorded.get("strict_correct")) or failure != recorded.get(
                "failure_type"
            ):
                moved.append(
                    f"{r['model']}/{r['reasoning_effort']} {r['task_id']}"
                    f"#{r['attempt_index']}: re-derived {correct}/{failure}, "
                    f"recorded {recorded.get('strict_correct')}/{recorded.get('failure_type')}"
                )
                if correct and not bool(recorded.get("strict_correct")):
                    moved_to_correct += 1
            r["score"] = score  # the re-derivation is the authority
        # Equivalence probe: re-score an evenly spaced subsample with the
        # real (quadratic) edit-distance function and confirm no verdict moves.
        clerkbench_scorer.levenshtein_distance = _REAL_LEVENSHTEIN
        step = max(1, len(rows) // 24)
        probe = rows[::step][:24]
        drift = [
            r for r in probe
            if _verdict(r, manifests[r["_manifest"]][r["task_id"]]) != r["_rescored"]
        ]
    finally:
        clerkbench_scorer.levenshtein_distance = _REAL_LEVENSHTEIN
    check(not drift, "re-scoring", f"{len(drift)} subsample verdict(s) depend on the "
                                   "edit-distance diagnostic")
    print(f"  re-scored {len(rows)} attempts from raw output + expected_files; the "
          f"re-derivation is the authority for every cell below")
    print(f"  {len(moved)} attempt(s) differ from the verdict recorded at collection "
          f"time ({moved_to_correct} failure -> correct) — provenance, not a defect: "
          f"the stored verdicts predate the symmetric wrapper rule (red-team C4)")
    for line in moved[:12]:
        print(f"    RE-DERIVED  {line}")
    if len(moved) > 12:
        print(f"    ... and {len(moved) - 12} more")
    print(f"  {len(probe)} attempts re-scored with the full unstubbed scorer: "
          f"{len(drift)} verdict changes")


# ───────────────────────── aggregation (canonical) ───────────────────────


def passk6(c: int, n: int) -> float:
    if n >= 6:
        return math.comb(c, 6) / math.comb(n, 6) if c >= 6 else 0.0
    return 1.0 if c == n and n > 0 else 0.0


def pava_decreasing(ys):
    """Pool-adjacent-violators fit of a non-increasing sequence, equal weights
    per rung (the pre-registered monotone estimator; board rule since the
    2026-09 revision). Mirrors scripts/research/build_report_tables.py."""
    blocks = []
    for y in ys:
        blocks.append([y, 1.0])
        while len(blocks) > 1 and blocks[-2][0] / blocks[-2][1] < blocks[-1][0] / blocks[-1][1]:
            s, n = blocks.pop()
            blocks[-1][0] += s
            blocks[-1][1] += n
    out = []
    for s, n in blocks:
        out.extend([s / n] * int(n))
    return out


def crossing(points) -> str:
    """Isotonic fit on the log-length ladder, then log-linear interpolation of
    the 50% crossing; '<L' / '>L' bounds when the fitted curve never crosses.
    Mirrors scripts/research/build_report_tables.crossing()."""
    pts = [(length, p) for length, p in points if p is not None]
    if not pts:
        return "—"
    fitted = pava_decreasing([p for _l, p in pts])
    fit = list(zip([length for length, _p in pts], fitted))
    for (l1, p1), (l2, p2) in zip(fit, fit[1:]):
        if p1 >= 0.5 > p2 and p1 != p2:
            frac = (p1 - 0.5) / (p1 - p2)
            return str(round(l1 * (l2 / l1) ** frac))
    if fit[0][1] < 0.5:
        return f"<{fit[0][0]}"
    if fit[-1][1] >= 0.5:
        return f">{fit[-1][0]}"
    return "—"


def parse_crossing(text: str):
    if text in ("—", "", None):
        return None
    if text.startswith(">"):
        return (float(text[1:]), ">")
    if text.startswith("<"):
        return (float(text[1:]), "<")
    return (float(text), "=")


def geomean_with_bounds(values):
    g = math.exp(sum(math.log(v) for v, _q in values) / len(values))
    quals = {q for _v, q in values}
    if ">" in quals and "<" not in quals:
        return g, "≥"
    if "<" in quals and ">" not in quals:
        return g, "≤"
    if quals == {"="}:
        return g, ""
    return g, "~"


def short_model(model: str) -> str:
    return (
        model.replace("openrouter/anthropic/", "")
        .replace("openrouter/google/", "")
        .replace("gpt-5.4-", "5.4-")
        .replace("claude-", "")
    )


def build_cells(rows):
    cells = defaultdict(
        lambda: {"c": 0, "n": 0, "e": 0, "out": 0, "in": 0,
                 "insts": defaultdict(lambda: [0, 0])}
    )
    for r in rows:
        L = int(r["profile"].split("_L")[1])
        k = (r["model"], r["reasoning_effort"], r["family"], L)
        u = r.get("usage") or {}
        cells[k]["n"] += 1
        cells[k]["out"] += u.get("output_tokens", 0)
        cells[k]["in"] += u.get("input_tokens", 0)
        # Cost is priced by the model that ACTUALLY answered each attempt,
        # not the requested contract model — mirrors build_report_tables.py's
        # per-row cost accumulation exactly. No v1 config routes through a
        # fallback, but the Opus 5 batch rows persist a bare answering_model
        # ("claude-opus-5"), which borrows the provider prefix from the
        # requested model id before the price lookup.
        am_raw = r.get("answering_model")
        model_id = r["model"]
        if am_raw and "/" not in am_raw and "/" in model_id:
            am = model_id.rsplit("/", 1)[0] + "/" + am_raw
        else:
            am = am_raw or model_id
        if am in PRICES:
            pin_am, pout_am = PRICES[am]
            cells[k]["cost"] = cells[k].get("cost", 0.0) + (
                u.get("input_tokens", 0) * pin_am
                + u.get("output_tokens", 0) * pout_am
            ) / 1e6
        # Budget-signalled rows that reached a cell did so because they
        # carried a complete artifact (assessability branch 1); count them so
        # the sentinel below can prove none arrived any other way.
        if budget_signal(r) is not None:
            cells[k]["t"] = cells[k].get("t", 0) + 1
        inst = cells[k]["insts"][r["task_id"]]
        inst[1] += 1
        if r["score"]["strict_correct"]:
            cells[k]["c"] += 1
            inst[0] += 1
    # Budget-signal sentinel: a budget-signalled row may now sit in a cell,
    # but ONLY because it emitted a complete artifact. What must never survive
    # is a budget-signalled row with no artifact — that is a budget zero back
    # in a capability denominator, which is what the doctrine exists to stop.
    signalled = sum(cell.get("t", 0) for cell in cells.values())
    leaked = [r for r in rows if budget_signal(r) is not None and not complete_artifact(r)]
    check(not leaked, "budget-signal sentinel",
          f"{len(leaked)} budget-signalled attempt(s) with no complete artifact "
          f"reached a cell")
    print(f"  {signalled} budget-signalled attempt(s) in cells, every one of them "
          f"carrying a complete artifact")
    return cells


def config_lists(rows, cells):
    scored, scored_founding = defaultdict(int), defaultdict(int)
    for (m, e, fam, _l), cell in cells.items():
        scored[(m, e)] += cell["n"]
        if fam in FOUNDING_FAMILIES:
            scored_founding[(m, e)] += cell["n"]
    configs = sorted(
        {(m, e) for (m, e, _f, _l) in cells if scored[(m, e)] > 0},
        key=lambda me: (
            CONFIG_ORDER_HINT.index(me[1]) if me[1] in CONFIG_ORDER_HINT else 9,
            me[0],
            me[1],
        ),
    )
    # Tables 2-4 iterate the pre-registered v1 roster only. Every capsule
    # run dir is a canonical v1 collection (no screening/extension dirs
    # exist here), so the v0 "core" restriction reduces to the roster gate.
    core_configs = [c for c in configs if c in V1_ROSTER]
    check(len(core_configs) == len(V1_ROSTER), "v1 roster",
          f"{len(core_configs)} of {len(V1_ROSTER)} roster configs have scored rows")
    return configs, core_configs, scored_founding


# ──────────────────────────── board rendering ────────────────────────────


def board_row_class(model: str, effort: str, k: int) -> str:
    """Mirrors build_report_tables.board_row_class(). Order of checks
    matters: identity (route comparison) first, then the R6 attempt-budget
    gate, and availability domination only as an annotation on a row the
    data already supports ranking. In v1 the first and third sets are
    empty, so every row is "ranked" or (k<6) a "bound"."""
    if (model, effort) in ROUTE_COMPARISON:
        return "route-comparison"
    if k < 6:
        return "bound"
    if (model, effort) in AVAILABILITY_DOMINATED:
        return "availability-dominated"
    return "ranked"


def board_row_line(b, rank) -> str:
    cost = f"${b['cost_attempt']:.2f}" if b["cost_attempt"] else "—"
    cost_succ = f"${b['cost_success']:.2f}" if b["cost_success"] else "—"
    cap = f"{b['capq']}{b['cap']:.0f}" if b["cap"] else "—"
    config = f"{b['config']}{' (p)' if b['provisional'] else ''}"
    if b["cls"] == "ranked":
        ch6_disp = f"{b['ch6q']}{b['ch6']:.0f}"
    elif b["cls"] == "availability-dominated":
        ch6_disp = f"{b['ch6q']}{b['ch6']:.0f}"
        config += " (availability-dominated)"
    elif b["cls"] == "route-comparison":
        ch6_disp = f"{b['ch6q']}{b['ch6']:.0f}"
        config += f" ({ROUTE_COMPARISON[(b['m'], b['e'])]})"
        if b["k"] == 5:
            config += " (one slot short)"
    elif b["k"] == 5:
        ch6_disp = f"unranked (one slot short; pass^5 bound ≤{b['ch6']:.0f})"
    else:
        ch6_disp = f"unranked (pass^{b['k']} bound ≤{b['ch6']:.0f})"
    if b["cls"] == "bound" and (b["m"], b["e"]) in AVAILABILITY_DOMINATED:
        config += " (availability-dominated)"
    return (f"| {rank if rank is not None else '—'} | {config} | {ch6_disp} "
            f"| {cap} | {cost} | {cost_succ} |")


def board_ranks(board):
    """Mirrors build_report_tables.board_ranks(). An availability-dominated
    row would carry a partial rank spanning every position its ≤ bound
    leaves open; the v1 board has none, so ranked rows take consecutive
    ordinals and bound rows print '—'."""
    n_block = sum(1 for b in board if b["cls"] in RANKED_BLOCK)
    out, pos = [], 0
    for b in board:
        if b["cls"] not in RANKED_BLOCK:
            out.append(None)
            continue
        pos += 1
        if b["cls"] == "ranked":
            out.append(str(pos))
        else:
            out.append(f"{pos}–{n_block}" if pos < n_block else str(pos))
    return out


def build_board(cells, core_configs, scored_founding):
    board = []
    for m, e in core_configs:
        caps, cons = [], []
        for fam in FOUNDING_FAMILIES:
            pts, cpts = [], []
            for L in crossing_rungs(fam):
                cell = cells.get((m, e, fam, L))
                if cell and cell["n"]:
                    pts.append((L, cell["c"] / cell["n"]))
                    insts = list(cell["insts"].values())
                    cpts.append((L, sum(passk6(c, n) for c, n in insts) / max(1, len(insts))))
            caps.append(parse_crossing(crossing(pts)))
            cons.append(parse_crossing(crossing(cpts)))
        if any(c is None for c in cons):
            continue
        # Rankability (red-team M4 / ruling R6): CH6 requires >=6 assessable
        # attempts on EVERY instance of EVERY measured founding cell, so the
        # config's effective k is the MINIMUM per-instance attempt count.
        # No 5-as-6 tolerance: C(c,6)/C(n,6) does not exist at n=5.
        max_k = None
        for fam in FOUNDING_FAMILIES:
            for L in SIZES:
                cell = cells.get((m, e, fam, L))
                if cell:
                    for _c, n_att in cell["insts"].values():
                        max_k = n_att if max_k is None else min(max_k, n_att)
        max_k = max_k or 0
        ch6, ch6q = geomean_with_bounds(cons)
        cap, capq = geomean_with_bounds([c for c in caps if c]) if all(caps) else (None, "")
        # R18 (2026-07-27): two distinct cost quantities.
        #   cost_attempt  — mean list-price cost of ONE L=100 attempt, both
        #                   founding families pooled (a measured quantity);
        #   cost_success  — pooled campaign dollars per observed success;
        #   cost_success_macro — the same, macro-averaged over families,
        #                   because E[c]/E[p] != E[c/p] when difficulty is
        #                   uneven. Ships in leaderboard.csv.
        # Cost is read from the per-row answering-model-priced cell["cost"]
        # accumulated in build_cells(), not recomputed here from a single
        # PRICES[m] lookup.
        c100 = n100 = 0
        cost100_sum = 0.0
        fam_costs = []
        for fam in FOUNDING_FAMILIES:
            cell = cells.get((m, e, fam, 100))
            if cell and cell["n"]:
                c100 += cell["c"]
                n100 += cell["n"]
                cost100_sum += cell.get("cost", 0.0)
                if cell.get("cost") and cell["c"]:
                    fam_costs.append(cell["cost"] / cell["c"])
        cost_attempt = cost_success = cost_macro = None
        if n100 and cost100_sum:
            cost_attempt = cost100_sum / n100
            if c100:
                cost_success = cost_attempt * n100 / c100
        if len(fam_costs) == len(FOUNDING_FAMILIES):
            cost_macro = sum(fam_costs) / len(fam_costs)
        board.append({
            "m": m, "e": e, "config": f"{short_model(m)}/{e}",
            "ch6": ch6, "ch6q": ch6q, "cap": cap, "capq": capq,
            "cost_attempt": cost_attempt, "cost_success": cost_success,
            "cost_success_macro": cost_macro, "k": max_k,
            "provisional": scored_founding[(m, e)] < PROVISIONAL_THRESHOLD,
            "cls": board_row_class(m, e, max_k),
        })
    board.sort(key=lambda b: (BOARD_CLASS_ORDER[b["cls"]], -b["ch6"]))
    for b in board:
        # Mirrors build_report_tables.py exactly: a slot-short row (k<6) is a
        # pass^5 CEILING, not a located crossing, so it cannot establish that
        # the config reaches the reference workload either — priced as a
        # bound in the figure but not frontier-defining here.
        b["frontier_eligible"] = (
            b["ch6q"] not in ("≤", "~") and b["ch6"] >= 100 and b["k"] >= 6
        )
    ranks = board_ranks(board)
    lines = [board_row_line(b, rk) for b, rk in zip(board, ranks)]
    return board, ranks, lines


def fourfam_lines(cells, configs):
    """Table 5 — mirrors build_report_tables.fourfam_full_tier_board(): the
    four-family CH6, restricted to configs measured at >=6 attempts per
    instance on EVERY family. A single sub-6 instance in any family
    disqualifies the config outright (rather than degrading to a pass^k
    bound), as does a family with no 50% crossing at all."""
    out = []
    for m, e in configs:
        cons = []
        eligible = True
        for fam in FAMILIES:
            cpts = []
            for L in crossing_rungs(fam):
                cell = cells.get((m, e, fam, L))
                if not cell or not cell["n"]:
                    continue
                insts = list(cell["insts"].values())
                if any(n_att < 6 for _c, n_att in insts):
                    eligible = False
                    break
                cpts.append((L, sum(passk6(c, n) for c, n in insts) / len(insts)))
            crossed = parse_crossing(crossing(cpts)) if eligible else None
            if crossed is None:
                eligible = False
                break
            cons.append(crossed)
        if not eligible:
            continue
        g, q = geomean_with_bounds(cons)
        out.append({"config": f"{short_model(m)}/{e}", "ch6": g, "q": q})
    out.sort(key=lambda b: -b["ch6"])
    return [f"| {b['config']} | {b['q']}{b['ch6']:.0f} |" for b in out]


# ──────────────────────── published-table extraction ─────────────────────


def _published_file(name: str, manifest_copy: str):
    src = RELEASE / "aggregates" / name
    origin = f"../aggregates/{name}"
    if not src.exists():
        src = HERE / manifest_copy
        origin = f"{manifest_copy} (fallback)"
    text = src.read_text(encoding="utf-8")
    local = HERE / manifest_copy
    if src != local and local.exists():
        check(local.read_text(encoding="utf-8") == text, f"{name} copy",
              f"{manifest_copy} differs from the shipped aggregates/{name} — "
              "the capsule is stale")
    print(f"  assertion target: {origin}")
    return text


def published_tables():
    text = _published_file("tables.md", "manifests/tables_published.md")

    sections, current = {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].split(" — ")[0].strip()
            sections[current] = []
        elif current:
            sections[current].append(line)

    def data_rows(lines):
        """Markdown table body rows, in order, one list per sub-table."""
        blocks, cur, seen_sep = [], [], False
        for line in lines:
            if line.startswith("|---"):
                seen_sep = True
                cur = []
                continue
            if seen_sep and line.startswith("| "):
                cur.append(line)
            elif seen_sep and cur:
                blocks.append(cur)
                cur, seen_sep = [], False
        if cur:
            blocks.append(cur)
        return blocks

    out = {}
    for key, name in [("table4", "Table 4"), ("table5", "Table 5")]:
        blocks = data_rows(sections.get(name, []))
        out[key] = blocks[0] if blocks else []
    return out


def compare(label, got, want) -> None:
    if got == want:
        print(f"  OK   {label}: {len(got)} rows reproduced exactly")
        return
    check(False, label, f"{len(got)} recomputed rows vs {len(want)} published")
    print(f"  FAIL {label}")
    for i in range(max(len(got), len(want))):
        g = got[i] if i < len(got) else "<missing>"
        w = want[i] if i < len(want) else "<missing>"
        if g != w:
            print(f"       row {i + 1}")
            print(f"         recomputed: {g}")
            print(f"         published : {w}")


def check_leaderboard_csv(board, ranks) -> None:
    """The board as structured data — what the paper builders read. Verified
    field by field, not just as rendered markdown. Mirrors the writer in
    build_report_tables.main(): ch6/capability at three decimals (M3; the
    one-decimal format let 107.481 ship as "107.5" and re-round to 108),
    costs at four."""
    text = _published_file("leaderboard.csv", "manifests/leaderboard.csv")
    lines = text.splitlines()
    header = lines[0]

    def n(v, fmt="{:.4f}"):
        return "" if v is None else fmt.format(v)

    got = [header]
    for b, rk in zip(board, ranks):
        note = ROUTE_COMPARISON.get((b["m"], b["e"]), "")
        got.append(
            f"{b['m']},{b['e']},{b['config']},{rk or ''},{b['cls']},"
            f"{b['ch6']:.3f},{b['ch6q']},{n(b['cap'], '{:.3f}')},{b['capq']},"
            f"{b['k']},{int((b['m'], b['e']) in AVAILABILITY_DOMINATED)},"
            f"\"{note}\",{int(b['provisional'])},{int(b['frontier_eligible'])},"
            f"{n(b['cost_attempt'])},{n(b['cost_success'])},"
            f"{n(b['cost_success_macro'])}"
        )
    if got == lines:
        print(f"  OK   leaderboard.csv: {len(got) - 1} board rows reproduced exactly")
        return
    check(False, "leaderboard.csv", f"{len(got) - 1} recomputed vs {len(lines) - 1} published")
    for i in range(max(len(got), len(lines))):
        g = got[i] if i < len(got) else "<missing>"
        w = lines[i] if i < len(lines) else "<missing>"
        if g != w:
            print(f"       row {i}\n         recomputed: {g}\n         published : {w}")


# ────────────────────────────────── main ─────────────────────────────────


def main() -> int:
    print("ClerkBench v1 evidence capsule — rebuild\n")

    print("[1/5] capsule integrity")
    verify_hashes()

    print("\n[2/5] loading capsule")
    manifests = load_tasks()
    rows = load_rows()

    print("\n[3/5] independent re-scoring (public scorer)")
    rescore(rows, manifests)

    print("\n[4/5] aggregating")
    rows = apply_assessability(rows)
    cells = build_cells(rows)
    configs, core_configs, scored_founding = config_lists(rows, cells)
    print(f"  {len(cells)} cells, {len(configs)} configurations "
          f"({len(core_configs)} on the v1 roster)")

    print("\n[5/5] published boards")
    pub = published_tables()
    board, ranks, t4 = build_board(cells, core_configs, scored_founding)
    compare("Table 4 (CH6 board: rank, CH6, capability, both cost columns)",
            t4, pub["table4"])
    compare("Table 5 (four-family CH6-4fam board)",
            fourfam_lines(cells, configs), pub["table5"])
    check_leaderboard_csv(board, ranks)

    print()
    if FAIL:
        print(f"REBUILD FAILED — {len(FAIL)} check(s) did not pass:")
        for f in FAIL:
            print(f"  - {f}")
        return 1
    print("REBUILD OK — every board number in tables.md Tables 4 and 5 (the "
          "paper's founding-family and four-family board), and every "
          "leaderboard.csv field, reproduces exactly from capsule contents.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
