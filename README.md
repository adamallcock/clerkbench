# ClerkBench — public release (v1)

This is the data and code release for *ClerkBench: Measuring the Consistency
Horizon of Language Models on Long Deterministic Workloads* (Allcock, 2026).
It lets anyone re-score every attempt behind the paper and rebuild its board
with one command.

## What ClerkBench is

Frontier language models already ace most accuracy benchmarks. ClerkBench
asks a harder question: how *long* a fully specified clerical workload —
billing, payroll, ledger replay, gateway spend tracking — a model can
execute before its output stops being trustworthy. Each task instance is
generated from a seed (input files, an explicit rulebook, and an exactly
computable correct answer), so test items are unlikely to have appeared
verbatim in training data and the metric cannot saturate: every model, no
matter how capable, lands somewhere on the ladder of workload lengths it can
sustain. This release scores every configuration on one frozen task set
(below); the generator's freshness is a property of the benchmark, not of
this board.

We run each instance repeatedly rather than once, and report two lengths
instead of a percentage: the **capability horizon**, the workload length at
which a model's chance of producing a perfect artifact on a single attempt
drops to 50%, and the stricter **consistency horizon (ClerkBench-CH6)**,
the length at which getting it right on *every one of six attempts* drops
to 50%. Both are grounded in a byte-exact grader — a model's output either
reconstructs the expected file tree exactly, or it doesn't — so every
published number can be recomputed independently from a raw model
transcript.

## Date convention

Every timestamp in the evidence capsule (`started_at`, `completed_at` on
each attempt row) is UTC, written as ISO 8601 with an explicit `+00:00`
offset, and every date in this README is a UTC date. The board's first
attempt started 2026-08-15T15:52Z and its last completed 2026-09-26T00:43Z.
Collection came in two blocks on the same frozen task set:

- **2026-08-15..2026-08-18**: the first nine configurations, including the
  top-ups at each configuration's pass@1 bracket. The only collection on
  2026-08-18 is the DeepSeek-V4-Flash content-fix re-collection
  (2026-08-18T00:13–02:30Z; see "Provenance exceptions").
- **2026-09-25..2026-09-26**: five more configurations (GPT-6 Astra, GPT-6
  Sol, GPT-6 Luna, Claude Opus 5.5, DeepSeek V4.1 Flash) and the top-ups
  that brought every in-range CH6 bracket to six seed instances.

Documents written in local (US Eastern) time — git commit dates, some
research logs, and run-directory names such as `gpt6luna-v1-20260924` — can
show the previous day. Run-directory names carry the local date a collection
was started and are labels, not windows.

## The board

Fourteen configurations from four laboratories, measured on all four
families (`banded_meter_billing`, `fee_ledger_dropzero`,
`payroll_overtime_ledger`, `spent_tracking_gateway`) at workload lengths
L∈{50, 100, 200, 400}, with an extra L=25 rung on payroll, six attempts per
instance. The two **founding families** (meter and ledger) carry up to six
seed instances per cell and define the headline score; payroll and gateway
carry three and enter only the four-family variant (ClerkBench-CH6-4fam).

| # | Config | ClerkBench-CH6 | CH6-4fam | Capability horizon | $ / L=100 attempt |
|---|---|---|---|---|---|
| 1–2 | gpt-6-astra / high | ≥400 | ≥400 | ≥400 | 0.31 |
| 1–2 | anthropic/claude-opus-5.5 / high | ≥317 | ∼167 | ≥400 | 0.18 |
| 3 | gpt-5.5 / high | 147 | 157 | 259 | 0.37 |
| 4 | deepseek/deepseek-flash / default (V4.1 Flash) | 138 | 116 | 301 | 0.03 |
| 5–13 | anthropic/claude-opus-5 / high | ≤100 | ≤114 | ≥400 | 0.28 |
| 6 | gpt-5.6-sol / high | 94 | 112 | 197 | 0.27 |
| 7 | gemini/gemini-3.7-flash / medium | 92 | 100 | 147 | 0.07 |
| 8 | deepseek/deepseek-v4-pro / default | 81 | 98 | 258 | 0.13 |
| 9 | gpt-6-sol / high | 79 | ≤84 | 145 | 0.06 |
| 10–13 | deepseek/deepseek-v4-flash / default | ≤77 | ≤74 | 214 | 0.06 |
| 11–13 | gpt-5.6-luna / high | ≤50 | ≤42 | ≤50 | 0.02 |
| 11–13 | gpt-5.6-terra / high | ≤50 | ≤42 | ≤56 | 0.10 |
| 11–13 | gpt-6-luna / high | ≤50 | ≤42 | ≤50 | 0.01 |
| — | gemini/gemini-3.7-flash / high | unranked (≤100 ceiling) | — | 243 | 0.17 |

`≥`/`≤` mark a crossing censored above L=400 or below L=50 in at least one
family; `∼` marks mixed censoring. A bound takes a rank interval, not a rank.
Structured data: `aggregates/leaderboard.csv` and `aggregates/fourfam.csv`;
bootstrap intervals in `aggregates/ch6_bootstrap.csv`.

| Config | Route | Collected (UTC) |
|---|---|---|
| gpt-5.5, gpt-5.6-sol | OpenAI direct, flex tier | 2026-08-16; top-ups 2026-09-25 |
| gpt-5.6-terra, gpt-5.6-luna | OpenAI direct, flex tier | 2026-08-15..16 |
| gpt-6-astra, gpt-6-sol, gpt-6-luna | OpenAI direct, flex tier | 2026-09-25 |
| anthropic/claude-opus-5 | Anthropic **Batch** API | 2026-08-15..16; top-ups 2026-09-25..26 |
| anthropic/claude-opus-5-5 | Anthropic **Batch** API | 2026-09-25 |
| gemini/gemini-3.7-flash — high and medium | Gemini direct, standard tier | 2026-08-15..16; medium top-up 2026-09-26 |
| deepseek/deepseek-v4-pro | DeepSeek direct | 2026-08-15..17; top-up 2026-09-25 |
| deepseek/deepseek-v4-flash | DeepSeek direct | 2026-08-15..18 |
| deepseek/deepseek-flash (V4.1 Flash) | DeepSeek direct, off-peak | 2026-09-25 |

Per-configuration windows, routes, sampling, thinking controls, output
budgets and service tiers are in `aggregates/serving_cards.csv`. Serving
notes that materially shape the board:

- **List-price reporting rule.** Published costs use undiscounted list
  prices. Flex, batch and off-peak discounts (up to 50%) reduced what the
  collection *paid*, never what is *reported*. Every cost column derives
  from `evidence-capsule/manifests/prices.json` (also
  `aggregates/unit_prices.csv`, with verification dates). Two list prices
  were corrected on 2026-09-07 after re-verification against the providers'
  pages: Opus 5 output is $25/MTok, not $10 (the $10 was the cache-write
  column), and GPT-5.6 Terra is $2/$12 per MTok input/output, not
  $0.5/$3.
- **Gemini 3.7 Flash** was collected on the standard tier (the flex tier
  load-shed during the collection window) with an explicit 131,072-token
  output budget; the server's silent default truncates otherwise. At high
  effort it runs out of thinking budget on most workloads beyond L=100, so
  too few attempts are assessable to estimate pass^6 and the arm is
  reported as an unranked ceiling (see "Budget-stopped attempts" below). The
  medium arm is ranked; two of its ledger L=400 slots that ended at the
  thinking ceiling were re-drawn.
- **Anthropic.** Both Opus configurations ran through the Batch API with
  adaptive thinking (temperature unset, as adaptive thinking forbids it).
  Only Opus 5's last top-up (36 of its 396
  rows, collected after a harness fix) carries a thinking-token count; for
  the other 360 rows its `high` effort is recorded only as the request
  parameter. From the Opus 5.5 collection on,
  the harness requests summarized thinking and reads the billed thinking
  count: all 342 Opus 5.5 rows report reasoning tokens and carry a thinking
  summary. Two Opus 5.5 slots lost to a provider billing error were re-run
  in place.
- **DeepSeek.** The rows are alias-based. V4 Pro serves the 0813 checkpoint
  (the alias moved on 2026-08-13 per the provider changelog, two days before
  collection began), and the provider still named that checkpoint when the
  2026-09-25 top-up ran. V4 Flash serves the 0731 checkpoint; the provider
  retired it on 2026-09-10, and its API name now routes to V4.1 Flash, which
  was collected on 2026-09-25 under the alias `deepseek-flash`. Every
  DeepSeek row reports reasoning tokens, the evidence that thinking was on
  (no reasoning parameter is sent at effort `default`). V4 Flash ran the
  founding families at six instances per cell (`founding_6inst`); 18 of its
  founding instances were re-collected on 2026-08-18 to fix a task-content
  divergence (see "Provenance exceptions").
- **Seed depth.** Every configuration has three seed instances per cell.
  Six-instance top-ups went first to the rungs bracketing each
  configuration's pass@1 crossing, then to every in-range CH6 bracket that
  lacked them, so all 15 in-range brackets carry six seeds at both rungs; a
  further top-up six-seeded Claude Opus 5's meter L=50 and L=100 to test the
  dip that censors its meter crossing. Per-cell depth is in
  `aggregates/seed_depth.csv`.

## What's included in this release

- `scorers/clerkbench_scorer.py` — the deterministic, byte-exact artifact
  grader, extracted as a single self-contained, stdlib-only Python file,
  unchanged from the v0 release. Given a task record and a raw model output
  string, it reproduces the exact score (`strict_correct`, `failure_type`,
  per-file diagnostics, etc.) that the internal harness recorded for every
  attempt behind the board.
- `scorers/scorer_selftest.py` — the gold/corrupted/null self-test harness:
  for every demo instance it verifies that a gold reconstruction scores
  correct, a single-byte corruption of an expected file is caught and
  correctly classified, and an empty submission is caught as a parse
  failure.
- `demo/` — the public demo instances (all four families, two workload
  lengths each, seed 990001), unchanged from the v0 release. Demo instances
  were never part of any scored run.
- `figures/` — the paper's data figures as published: `pass1_curves.pdf`
  (Figure 2), `cost_frontier.pdf` (Figure 3) and `passk_nano.pdf`
  (Figure 4).
- `aggregates/` — the aggregate data behind every published number, copied
  from the generated pipeline outputs.
  - **How crossings are located.** Every 50% crossing (CH6 per family and
    the capability horizon) comes from the pre-registered monotone
    estimator: an isotonic fit (pool-adjacent-violators, equal weights) on
    log length, interpolated log-linearly. `crossing_sensitivity.csv`
    recomputes the board under two alternatives. Under the first-downward-
    bracket rule Claude Opus 5 would score 154 instead of a ≤100 bound (its
    meter pass^6 curve is worst at L=50, which six seed instances confirm),
    DeepSeek V4 Flash 109 instead of ≤77, and DeepSeek V4 Pro 77; under the
    last-straddle rule V4 Pro moves to 126.
  - **Table numbering.** `tables.md` keeps the pipeline's internal numbering,
    which differs from the paper's. `tables.md` Table 4 (the ClerkBench-CH6
    leaderboard: ranked rows plus the Gemini-high bound row) is the paper's
    Table 2 (§3.2), which prints the ranked rows; `tables.md` Table 5 (the
    four-family ClerkBench-CH6-4fam board) is Table 2's four-family column;
    `tables.md` Table 1 (pass@1 by length) underlies the paper's per-attempt
    success table (Appendix A.3).
  - **Board files.** `leaderboard.csv`, `fourfam.csv`, `ch6_bootstrap.csv`
    (bootstrap intervals, equivalence-test labels and the board-reproduction
    gate's outputs), `crossing_sensitivity.csv`, `seed_depth.csv` (seed
    instances with six assessable attempts per cell, with each
    configuration's CH6 and capability brackets), `ch6_null_excess.csv` (the
    pre-registered primary endpoint: the consistency horizon predicted from
    pass@1 alone, and the measured excess over it, with paired bootstrap
    intervals), `chk_by_k.csv` (consistency horizons at each k = 1..6),
    `serving_cards.csv`, `refusal_counts.csv` (zero throughout),
    `unit_prices.csv`, and `cost_by_rung.csv` (mean list-price cost per
    attempt at each L, founding families pooled).
  - **Outcome files.** `failure_decomposition.csv` counts every outcome per
    configuration × family × L, with total rows marked `all`. Across the
    fourteen configurations: 5,313 raw attempts, 5,254 scored, 3,240
    correct, and 2,014 failures (1,989 content mismatches, 3 empty outputs,
    22 other parse failures, no wrapper-only slips, no refusals); 272
    attempts are correct only after the class-based wrapper normalization;
    55 attempts were scored despite a budget signal and 59 were excluded at a
    budget (see "Provenance exceptions"). Also `payroll_mechanism_v1.csv` (a
    mechanical classification of every payroll failure by mechanism, from
    an independent re-simulation gated on reproducing all four gold files
    byte-exactly; not an adjudication), `wrapper_slip_census.csv` and
    `wrapper_slip_counterfactual.csv` (the output-wrapper slip census and
    the board under strict, published and one-model wrapper handling),
    `homogeneity_v1.csv` (the per-cell instance-homogeneity screen: exact and
    chi-square p-values with Benjamini–Hochberg flags), `pool_schedule.csv`
    and `lever_schedule.csv` (entity-pool sizes, events per entity and
    per-rung hardness levers, read from the frozen manifests).
  - `pass1_by_length.csv` — per-`(config, family, length)` pass rates with
    Wilson CIs. **Scope warning:** this file and `tables.md` (whose header
    reads "7676 ladder attempts across 47 configs") are a superset of the
    board. Of its 449 data rows, 238 come from the fourteen board
    configurations: 224 at the board rungs (4 families × L∈{50, 100, 200,
    400}) plus the fourteen payroll L=25 rows. The other 211 rows, from 33
    configurations (claude-fable-5, claude-opus-4.8, gemini-3.1/3.5,
    gpt-5.4-nano/mini, gpt-5-mini/nano, an OpenRouter open-weight panel, and
    others), are earlier-campaign and screening rows kept for continuity and
    are **not** part of the board. The gpt-5.4-nano payroll rows were scored
    on the pre-regeneration payroll content described under "Provenance
    exceptions". `tables.md` Table 3 (first-divergence depth) is empty for
    every board configuration.
  - **The L=25 rung.** 26 of those rows sit at L=25. The fourteen board
    payroll rows enter payroll's crossings (payroll's ladder is
    L∈{25, 50, 100, 200, 400}), and so the four-family score; the founding
    families have no L=25 rung on the board. The other 12 rows — the
    gpt-5.4-nano calibration on all four families, and an OpenRouter
    screening panel (deepseek-v4-flash at two temperatures, two Qwen3.6
    configurations) on the founding families — enter no published crossing.
  - Quick-look SVG versions of the curves and the frontier
    (`curves_*.svg`, `cost_frontier.svg`, `passk_nano.svg`) are the
    pipeline's report figures; the paper's figures are in `figures/`.
- `evidence-capsule/` — the complete evidence behind every published
  number. **Task set:** 25 task manifests (six primary manifests, including
  the content-fix manifest, and 19 top-up manifests) with 291 records
  covering **75 distinct task ids**; because 18 founding ids carry two
  different contents (below), that is **93 distinct (id, content)
  records**, and because two contents each appear under two ids, **91
  distinct instance contents**. Every record ships in full (prompt, input
  files, expected artifacts, operation spec). **Attempts:** all 5,313 raw
  model attempts in 48 files from the 20 canonical run directories (5,254
  scored; 59 stopped at a budget before producing an artifact and are
  excluded as unmeasurable, but kept verbatim in the logs). Plus sha256 of
  every file and `rebuild.py`, which re-derives every attempt's
  `strict_correct` from the raw output with the pinned public scorer and
  recomputes the ranked CH6 board (`tables.md` Table 4), the four-family
  board (`tables.md` Table 5), and `leaderboard.csv` field by field,
  asserting byte-equality against the shipped `aggregates/`. One command,
  standard library only, no network:

  ```
  cd evidence-capsule && python3 rebuild.py
  ```

  Unlike the v0 capsule there is no supersede or adjudication machinery: the
  20 run directories are the canonical collection in full (earlier rows for
  every board configuration were purged upstream), and no score was
  adjudicated — no adjudication pass was run on this board, so "no attempt
  required adjudication" should be read as "none was examined", not as a
  cleared audit. `evidence-capsule/manifests/canonicality.json` records each
  attempts file's source run directory, row count, and sha256.
- `PREREGISTRATION_DEVIATIONS.md` — every gate and item of the v1
  pre-registration plan, whether it was met, and what stands in its place
  where it was not (the paper's reproducibility section summarizes it).
- `docs/preregistration/` — the five planning documents the paper and the
  deviations ledger cite: the pre-registration plan, the execution plan,
  the uncertainty-review rulings and their adjudication, and the top-up
  freeze. Each is byte-identical to the version committed in the
  development repository, and its index lists the commit, the UTC commit
  date and the sha256; every one was committed before the collection it
  governs.
- `earlier-campaign/tools-control/` — raw run logs for all five arms of
  the paper's tool-availability control (Appendix A.5), with an index
  mapping each file to its arm.
- `CITATION.cff` and `.zenodo.json` — citation and archive metadata.

### Earlier-campaign analyses cited by the paper

Several analyses the paper relies on were collected in an earlier campaign
(2026-07, the v0 release) on earlier task content, not on the frozen task
set; the paper marks them "earlier campaign". They ship as follows:

| Analysis | File | Ships in |
|---|---|---|
| Emission control (215 scored calls, three-model panel, L∈{100,400}, both founding families; paper §3.3) | `emission_control.csv` | this release (`aggregates/`, byte-identical to the v0 copy) |
| Prefix-truncation control (standalone / in-context / within-run survival; paper §3.3) | `truncation_table.csv` | this release (`aggregates/`, byte-identical to the v0 copy) |
| gpt-5.4-nano/xhigh pass^k calibration (20 attempts per instance; paper §3.4, Figure 4) | `passk_nano.csv`, `nano_calibration_cost.csv` | this release (`aggregates/`, four families). Its payroll L≥50 rows were scored on the pre-regeneration payroll content (below) |
| Tool-availability control (paper Appendix A.5) | raw run logs, all five arms | this release (`earlier-campaign/tools-control/`) |

## Provenance exceptions (documented, fixed in the data)

### 1. Founding-family id divergence and the DeepSeek-V4-Flash re-collection

The frozen task set carries 18 founding task ids (meter and dropzero,
L∈{100, 200, 400}, instances 000001–000003) whose `founding_3inst` and
`founding_6inst` manifest records differ in content — RNG drift caught by
an adversarial check on 2026-08-16/17. Only the six-instance
DeepSeek-V4-Flash founding tier had run on `founding_6inst`; every other
configuration ran on `founding_3inst`.

The redraw also produced two **cross-id duplicates**: the `founding_6inst`
record for meter L0100 instance 000001 is content-identical to the
`founding_3inst` (and `dsflash_content_fix`) record for meter L0100
instance 000003, and the `founding_6inst` dropzero L0400 instance 000001
is content-identical to `founding_3inst` dropzero L0400 instance 000003.
No configuration was scored on both members of either pair: the shipped
`founding_6inst` attempts at L≥100 cover instances 000004–000006 only, so
no published score is affected.

The data-level inconsistency was fixed by re-collection on 2026-08-18
(2026-08-18T00:13–02:30Z): those 18 instances were re-run for V4-Flash on
the canonical `founding_3inst` content (`dsflash_content_fix`, 108
attempts, all completed), and the 108 superseded 6inst-content rows were
**retired from the shipped run log**. The shipped
`founding_6inst-deepseek_deepseek-v4-flash-default.jsonl` therefore has
180 rows, not the 288 the run produced. The retired rows are not in this
release; they live in the development repository's git history — the full
288-row log is the version committed at `02e4810` (the last commit before
the trim, which landed in `58663af`). Every configuration's instances
000001–000003 therefore answered 3inst-equivalent content, and V4-Flash is
ranked on both boards. The divergence persists only as a property of the
two task FILES, both of which ship in the capsule: every attempt is scored
against the manifest its run was served from (recovered from the attempts
filename), and `rebuild.py` asserts the divergence is confined to the known
manifest set and that `dsflash_content_fix` is byte-identical to
`founding_3inst` on every id it carries.

### 2. Budget-stopped attempts and re-drawn slots

An attempt that hit an output or thinking budget is judged on what it
emitted, not on the provider's finish reason:

- **Scored:** 55 attempts carried a complete, parseable artifact despite a
  budget stop and are scored like any other; all are
  gemini/3.7-flash/high rows, and 28 are byte-exact.
- **Excluded, never scored as zeros:** 59 attempts stopped before any
  artifact existed — 38 flagged by the provider's finish status and 21
  empty completions that ended at a thinking ceiling the model returns to or
  at the declared output cap. Of the 21, 18 are gemini/3.7-flash/high, 2
  gemini/3.7-flash/medium and 1 gpt-6-luna. All 59 rows stay in the shipped
  logs.
- **Failures:** an empty completion that ended well short of any ceiling is
  the model returning nothing, and is scored as a failure (2 attempts).

A configuration is ranked only when every instance has six assessable
attempts, so an occasional loss is re-drawn: gemini/3.7-flash/medium (two
ledger L=400 slots) and gpt-6-luna (one ledger L=400 slot) each carry a
re-drawn attempt 7 in the same file, next to the excluded original.
gemini/3.7-flash/high runs out of budget systematically beyond L=100, so
redrawing cannot help, and it is reported as an unranked ceiling.

Three earlier losses were replaced in place rather than appended, so their
original rows are absent from the shipped logs:

- DeepSeek-V4-Flash dropzero L400 instance 000004, attempt 3 (capped
  2026-08-15T18:53Z): re-run in Stage 2 and replaced in place in commit
  `02e4810`; the capped row is present in the run log from `616af2e`
  through that commit's parent, `1fb18ef`.
- one stochastic DeepSeek-V4-Flash cap during the 2026-08-18 content-fix
  re-collection: re-run before the log was first committed (`58663af`), so
  the capped row is not recoverable from the repository.
- two claude-opus-5-5 slots that failed with a provider billing error (a
  transport failure, not an outcome) on 2026-09-25, re-run with the
  harness's resume mode.

Consequently the shipped run logs are the canonical collection but are not
a verbatim transcript of everything the collection requested: the 108
retired rows, the two replaced DeepSeek-V4-Flash capped rows and the two
replaced Opus 5.5 error rows are absent, as described here.

### 3. Payroll L≥50 instances differ from the 2026-07-18 screening instances of the same ids

The 12 `payroll_overtime_ledger` ids at L∈{50, 100, 200, 400}
(`…s20260703.000001–3`) carry **different content** from the records of the
same ids used in the 2026-07-18 payroll screening ladder and the
gpt-5.4-nano calibration
(`results/relbench/pilot/runs/payroll-gateway-pilot-20260718/*.tasks.jsonl`):
different employee tables, event streams, `operation_spec` counts and gold
on 12/12 ids, with the rulebook text before "Source files:" byte-identical.
Cause: the ladder generator draws every size from one shared seeded RNG
stream, and adding the L=25 rung to the ladder shifted the stream before
every L≥50 instance while the seeded ids stayed fixed. The board uses only
current-content attempts, so no board score is affected, but the
earlier-campaign payroll analyses (the nano pass^k payroll rows, and the
gpt-5.4-nano payroll rows in `pass1_by_length.csv`) were computed on the
earlier content. `canonicality.json`'s `known_divergent_task_id_count` (18)
covers the founding ids only; the 12 payroll ids are an additional,
cross-campaign divergence recorded here.

## What's withheld, and why

The task-family **generators** — the code that samples task parameters and
computes ground truth via simulation — are not included, permanently:
releasing them would allow unlimited regeneration of in-distribution
training data. Note what this does and does not protect: every prompt in
the capsule contains the complete rulebook that specifies the simulator
plus the event schema, so a reader can implement the simulator from the
release. Contamination protection therefore rests on **seed retirement**,
not on generator secrecy.

**Publishing this capsule retires every scored seed, in all four
families.** A retired seed is never scored again, in any version, on any
leaderboard, so withholding it would protect nothing — and releasing it
makes the reproducibility claim checkable by anyone rather than taken on
trust. This supersedes the v0 release's statement (`SPLITS.md`, v0 README)
that the payroll and gateway seeds would "carry forward" into v1 and stay
private: they were scored here and are published and retired.

Consequences a reader should draw:

- **The board is a closed snapshot.** No configuration can be added to it
  after publication, because the instances it was scored on are retired.
  This release lets anyone re-score all 5,313 transcripts and recompute
  every board; it does not let anyone place a new model on this board.
- **A later board must use fresh seeds for all four families**, and its
  rows will not be instance-comparable to these (one seed instance can move
  a horizon by tens of events; see the paper's uncertainty discussion).
  Comparisons across boards are between distributions, not shared
  instances.
- **The founding seeds were carried over from v0.** The founding ladder
  reused the `s20260703` seed epoch, and 18 of the 24 `founding_3inst`
  records that have a v0 counterpart are byte-identical (prompt, input
  files, expected artifacts) to instances shipped in the v0 release bundle
  (`release/clerkbench-v0-preprint/evidence-capsule/tasks/` in the
  development repository; ids differ only by the `.s20260703` segment):
  meter L50 and L100 instances 000001–000003, and dropzero L50, L100, L200
  and L400 instances 000001–000003. The other six (meter L200/L400,
  000001–000003) differ because of the meter-ladder RNG drift documented in
  the development repository's `results/relbench/pilot/PROVENANCE.md`. The
  v0 `SPLITS.md` had said these seeds "retire at v1" and that no v1 entry
  may be produced from them; that rule was not followed for the founding
  families, and the retirement is instead effected by this release. On
  distribution: the v0 bundle has been in the development repository since
  2026-07-29/30 (commits `e3aa370`, `3bc3df2`); that repository was private
  on GitHub when checked (2026-09-07) and carries no `CITATION.cff`,
  `.zenodo.json`, DOI, or Zenodo/arXiv record for ClerkBench, and we know of
  no distribution of the v0 bundle before collection began on 2026-08-15.
- **No verbatim-reproduction holdout pass was run.** The v0 README lists
  such a pass as a release-checklist item; no record of one exists for this
  board, so this release makes no private-holdout claim.

## How to run the scorer

The scorer has no dependencies beyond the Python standard library.

Score one model output against one task:

```
python scorers/clerkbench_scorer.py <task.json> <output.txt>
```

`task.json` is a task record with at least an `expected_files` field (and,
for abstention-style tasks, `variant` and `expected_block`); `output.txt` is
the raw model output text. The score dict is printed as JSON.

Run the full self-test suite against the bundled demo instances:

```
python scorers/scorer_selftest.py
```

This exits nonzero if any gold/corrupted/null check fails for any demo
instance.

## License

The benchmark data, demo instances, aggregate score data, and this
documentation are licensed under the Creative Commons Attribution 4.0
International License (CC BY 4.0). The code (`scorers/`, `evidence-capsule/scorers/` and
`evidence-capsule/rebuild.py`) is licensed under the Apache License,
Version 2.0. See `LICENSE` and `LICENSE-DATA-DOCS.md` for full terms.

## Citing

Please cite the paper and this archive; `CITATION.cff` carries both.
