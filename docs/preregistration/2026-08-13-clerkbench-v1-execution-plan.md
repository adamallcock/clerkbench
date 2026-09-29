# ClerkBench v1 — Execution Plan (Plan A-new vs Plan B-new)

Execution runbook for the powered v1 collection. This is the *how to run it*
layer; the estimands, power math, per-event instrumentation spec, equivalence
tests, and decision gates live in
[`2026-08-13-clerkbench-v1-preregistration-plan.md`](2026-08-13-clerkbench-v1-preregistration-plan.md)
and are referenced, not repeated. Budget basis reconciled in
[`2026-07-27-v1-protocol-and-budget.md`](2026-07-27-v1-protocol-and-budget.md)
(superseded roster/prices below).

All dollar figures are **spend** (with the intended flex/batch tiers applied);
the paper still reports undiscounted **list** prices. Two prices are still
estimates and marked ⚠️ — confirm before spending.

---

## 0. The decision this plan serves

Run one of two campaigns against the same locked roster:

| | Plan A-new | Plan B-new |
|---|---|---|
| Design | 6×6 at every (config, family, rung) | 6-instance depth only at each config's two crossing-bracketing rungs; 3×6 elsewhere |
| Spend | **~$430** | **~$170–210** |
| Buys | uniform support, cleanest methods, four-family CH6 at full depth for all 8 | valid 6-instance crossings for every ranked number; four-family CH6 for the ranked set |
| Forgoes | nothing (except rank separation, unaffordable under any plan) | uniform depth at non-informative rungs; needs a bracketing freeze |
| Complexity | low — collect everything | medium — 3×6 pass → identify brackets → top-up |

**Recommendation:** **A-new.** For the *old* roster, B beat A because five
configs had reusable 3×6 data, so B only paid for top-ups. With the new roster,
**six of eight configs are new checkpoints/effort tiers with zero reusable
data** — they get collected in full either way — so B's saving shrinks to
"don't go to 6 instances at 2–3 non-bracketing rungs," worth roughly $200 for a
large jump in operational complexity (a mid-campaign bracketing freeze, a
two-stage collection, a weaker methods paragraph). At a ~$430 ceiling the
simplicity and uniform support of A are worth the delta. **Fall back to B-new
only if the confirmed Opus 5.0 / DS-Pro prices push A materially above ~$500.**

---

## 1. Locked roster (8 configs)

| # | Config | Effort | Route / tier | $/call (spend) | Data status |
|---|---|---|---|---|---|
| 1 | GPT-5.5 | high | OpenAI direct + **flex** | $0.125 | ♻️ reuse v0 founding 3×6 |
| 2 | GPT-5.6 Sol | high | OpenAI direct + **flex** | $0.100 | ♻️ reuse v0 founding 3×6 |
| 3 | GPT-5.6 Terra | high | OpenAI direct + **flex** | $0.010 | 🆕 −80% price; full collect |
| 4 | GPT-5.6 Luna | high | OpenAI direct + **flex** | $0.006 | 🆕 −5× price; full collect |
| 5 | Gemini 3.7 Flash | high | Gemini direct + **flex** | $0.066 ⚠️ | 🆕 replaces 3.1 Pro; full collect |
| 6 | Claude Opus 5.0 | high | Anthropic **batch** | $0.220 ⚠️ | 🆕 upgrade from 4.8; full collect |
| 7 | DeepSeek V4 Pro | default | DeepSeek direct | $0.150 | 🔥 new ckpt (+2.5×); **purge old**, full collect |
| 8 | DeepSeek V4 Flash | default | DeepSeek direct | $0.0225 ⚠️ | 🔥 new ckpt; **purge old**, full collect |

Dropped from v0: Gemini 3.1 Pro, Gemini 3.5 Flash, gpt-5.4-nano.
`$/call` is campaign-average (≈ 30% below the L100 board figure because short
rungs are cheap).

⚠️ **Confirm before spending:** Opus 5.0 list price (assumed = 4.8's $5/$25),
Gemini 3.7 Flash base (assumed 50% of 3.5-Flash's $1.5/$9), DS-Flash new-ckpt
multiplier (assumed +2.5×). Update `scripts/research/pricing.py` entries + the
`verified` date for all four, then re-run the cost estimate.

---

## 2. Pre-flight (must all complete before any spend)

### 2.1 Purge the superseded DeepSeek checkpoints
Both DeepSeek models changed checkpoints; old and new **cannot** be pooled.
1. Identify the old run dirs: `deepseek-flash0731-20260730`, any
   `deepseek-screen-*` V4-Pro dirs, and the preview flash dirs already in
   `FLASH0731_PREVIEW_RUN_DIRS`.
2. Add every old DeepSeek run dir to `EXCLUDED_RUN_DIRS` in
   `scripts/research/build_report_tables.py` (and mirror in
   `regime_analysis.py` / `depth_null_analysis.py` if used). Do **not** delete
   the raw JSONL — exclusion keeps provenance immutable.
3. Regenerate the board and confirm both old DeepSeek rows disappear and no
   stale cells remain (`ch6_bootstrap.py` parity gate must still pass).
4. New checkpoints collect into fresh dirs `deepseek-v4-pro-<ckpt>-<date>` /
   `deepseek-v4-flash-<ckpt>-<date>`.

### 2.2 Land the per-event instrumentation (gating dependency)
The v0 divergence-depth statistic was invalid (artifact-byte vs event-time).
Per preregistration §3, **before collection**:
1. Generator emits a dense `out/event_trace.tsv` for every family — one row per
   event, in seq order, carrying the post-event state hash — so the first
   divergent *event* is directly readable for **all** families (fixes the
   ledger, whose `checkpoint.tsv` is account-ordered and L-decoupled).
2. Scorer reports `first_divergent_event` (event index / L) alongside the
   existing byte offset; the depth-null pipeline consumes the event field.
3. Re-run the v0 meter cross-check to confirm the new field reproduces the
   corrected event-depth result (0 BH-significant cells) — a regression anchor.
4. This is a **build task, not an API cost**, but it blocks Stage 2.

### 2.3 Pre-registration freezes (commit before spend, per preregistration §5–6)
- **Config list + serving configs** (this table), snapshot-dated.
- **Seed sets**: the exact instance seeds per (family, rung); shared across
  configs for paired analysis.
- **Bracketing rule** (Plan B only): the two crossing-bracketing rungs per
  (config, family) are identified from the Stage-1 3×6 data by a *pre-declared*
  rule, then frozen before any 6-instance top-up.
- **Scoring**: publish **strict** and **delimiter-normalized** scores side by
  side; the ranked score uses one, pre-declared.
- **Adjudication**: blinded policy; raw and adjudicated boards both shipped.
- **Endpoint**: excess-horizon (CH6 − pass@1-null) is primary; the raw
  CH6-vs-capability gap is descriptive only.

### 2.4 Price + tier verification
Confirm the four ⚠️ prices and that each route accepts the intended tier:
OpenAI flex on 5.x, Gemini flex on 3.7 Flash, Anthropic **batch** on Opus 5.0
(50% off, ~24h SLA), DeepSeek direct (off-peak discount *not* assumed — add it
if you want a further ~50% on DeepSeek).

---

## 3. Collection matrix

Ladder rungs: **L ∈ {25 (payroll only), 50, 100, 200, 400}**; L=800 excluded
from horizon estimation (width-confounded). Families: `banded_meter_billing`,
`fee_ledger_dropzero`, `payroll_overtime_ledger`, `spent_tracking_gateway`.
"Instances" = seeds; "attempts" = repeats per instance.

### Plan A-new — full universality
6 instances × 6 attempts at every (config, family, rung).

| Config | new attempts | $/call | line cost |
|---|--:|--:|--:|
| GPT-5.5 (reuse) | ~400 | 0.125 | ~$50 |
| GPT-5.6 Sol (reuse) | ~400 | 0.100 | ~$40 |
| GPT-5.6 Terra | ~720 | 0.010 | ~$7 |
| GPT-5.6 Luna | ~720 | 0.006 | ~$5 |
| Gemini 3.7 Flash | ~720 | 0.066 | ~$48 |
| Opus 5.0 (batch) | ~720 | 0.220 | ~$158 |
| DeepSeek V4 Pro | ~720 | 0.150 | ~$108 |
| DeepSeek V4 Flash | ~720 | 0.0225 | ~$16 |
| **Total** | | | **~$430** |

### Plan B-new — bracketing-first tiered depth
`3×6 founding pass (also the crossing locator) → freeze bracketing rungs →
top-up to 6 instances there → fill payroll/gateway to 6-att at bracketing`.
5.5/Sol skip the founding pass (v0 data).

| Config | new attempts | $/call | line cost |
|---|--:|--:|--:|
| GPT-5.5 (reuse; top-up only) | ~120 | 0.125 | ~$15 |
| GPT-5.6 Sol (reuse; top-up only) | ~120 | 0.100 | ~$12 |
| GPT-5.6 Terra | ~300 | 0.010 | ~$3 |
| GPT-5.6 Luna | ~300 | 0.006 | ~$2 |
| Gemini 3.7 Flash | ~300 | 0.066 | ~$20 |
| Opus 5.0 (batch) | ~300 | 0.220 | ~$66 |
| DeepSeek V4 Pro (normal support) | ~300 | 0.150 | ~$45 |
| DeepSeek V4 Flash (**full 6×6**) | ~576 | 0.0225 | ~$13 |
| **Total (LOCKED variant)** | | | **~$175** |

**LOCKED (2026-08-15):** run **Plan B-new** with the "uniformity where it's
nearly free" full-6×6 slot moved from DS-Pro to **DS-Flash** — at +2.5× DS-Pro
no longer earns uniform depth, while DS-Flash at $0.0225/call gets full 6×6 for
~$13. DS-Pro drops to normal per-config support (~$45). Campaign ceiling
**~$175** (+ optional ~$212 n=20 replication subset).

---

## 4. Execution sequencing

Run cheap→expensive so a mistake is caught on a $2 config, not a $150 one.

**Stage 0 — probe + calibration (~$5).**
Probe-first one instance at L=400 on each new config (largest, most likely to
hit a cap or a serving quirk); confirm output budget, tier acceptance, token
accounting, and `answering_model` capture. Cheap-model sanity on nano-class if
desired. Hard-gate: no full run until every probe row scores and prices sane.

**Stage 1 — founding 3×6 (B only; part of A's full pass).**
Collect founding families 3 inst × 6 att at all rungs for the six new configs.
For B, this doubles as the crossing locator: apply the frozen bracketing rule.
Order: Terra → Luna → DS-Flash → Gemini 3.7 Flash → DS-Pro → Opus 5.0.

**Stage 2 — main depth.**
- A-new: fill to 6×6 at every cell (incl. payroll/gateway).
- B-new: 6-instance top-up at the two bracketing rungs per (config, family);
  fill payroll/gateway to 6-att at bracketing rungs; payroll L25 universal.
Attempt-major ordering (all attempts of one instance before the next) to
maximize prompt-cache hits (~53% measured in v0).

**Stage 3 — replication subset (~$212, optional but recommended; preregistration §2).**
n=20 attempts per instance on a small sample (both founding families, rungs
25/50/100) on **one cheap config** (Terra or DS-Flash) to test whether the
nano instance-trap replicates at a higher tier. Priced separately from A/B.

**Resumability:** every stage writes per-attempt JSONL keyed by
(model, effort, task_id, attempt_index); reruns dedupe on that key, so a killed
run resumes without recollection.

---

## 5. Per-provider serving configs (exact)

Driven by `reliability_abstention_pilot.py` adapters. Output budget at provider
maxima; report list prices regardless of tier.

| Provider | Configs | Adapter facts |
|---|---|---|
| OpenAI direct | 5.5, Sol, Terra, Luna | `service_tier=flex`; `reasoning.effort=high`; `max_tokens=131072`; provider-default sampling |
| Gemini direct | 3.7 Flash | `serviceTier:"flex"`; `thinkingConfig.thinkingLevel` for effort; uncapped output |
| Anthropic **batch** | Opus 5.0 | `AnthropicBatchClient` / `run_anthropic_batch_config`; adaptive thinking + `output_config.effort`; `display:summarized`; **billed** `thinking_tokens`; budget 128000; ~24h SLA; temperature unset |
| DeepSeek direct | V4 Pro, V4 Flash | native `reasoning_effort`; `max_tokens=131072`; temperature unset under reasoning |

Server-side refusal fallback: **not used** (Fable dropped). `answering_model`
still persisted per row for audit.

---

## 6. Cost tracking & guardrails
- Per-config spend ledger updated after each stage; hard stop at the plan
  ceiling (A: $500, B: $260) — the runner should refuse to start a stage that
  would breach it given the probe-measured $/call.
- Report **list** prices in all artifacts; record `requested_service_tier` and
  `response_service_tier_used` per row so the flex/batch downgrade is auditable.
- Batch (Opus) runs asynchronously — submit early, poll; don't block the cheap
  synchronous configs on it.

---

## 7. Analysis pipeline (post-collection)
1. `build_report_tables.py` → `build_paper_tables_tex.py` → `build_serving_cards.py`
   (regenerate the board, tables, serving cards, snapshot macros).
2. `ch6_bootstrap.py` — CH6 CIs + board-reproduction parity gate.
3. Corrected depth-null on the **event** field (preregistration §4) — the
   rationing hypothesis test, now with a valid observable for all families.
4. v1 endpoints: **excess-horizon** (CH6 − pass@1-null), the beta-binomial
   instance-heterogeneity test on the n=20 subset, and the **equivalence test**
   with the pre-declared margin (replaces "one tier, not an order").
5. Regenerate the evidence capsule; `rebuild.py` must print REBUILD OK.
6. `make check` (inputs/bib/vendor/claims/pdf) green.

---

## 8. Decision gates (see preregistration §8 for the full 9-gate table)
- **G1 excess-horizon > 0** with CI excluding 0 on ≥1 family → consistency is a
  distinct property (the claim v0 could not support).
- **G2 rank order** resolves under the equivalence test → publish an order;
  else publish tiers with the margin stated.
- **G3 rationing**: event-depth front-loading survives BH on the powered data →
  mechanism claim; else it stays a null result (as in v0).
- **G4 trap-at-frontier**: n=20 subset shows heterogeneity beyond the i.i.d.
  null → the trap generalizes; else scope to small models.
- Stop-add rule: after Stage 2, add separation seeds only at adjacent pairs
  whose equivalence test is inconclusive (targeted, not uniform).

---

## 9. A-new vs B-new — side by side

| | A-new | B-new |
|---|---|---|
| Spend | ~$430 | ~$170–210 |
| Wall-clock | ~2–4 days (Opus batch SLA dominates) | ~3–6 days (extra bracketing freeze + 2-stage) |
| Methods section | clean, uniform support | "tiered support, pre-registered brackets" caveat |
| Rank separation | no (unaffordable either way) | no |
| Four-family CH6 | full depth, all 8 | ranked set |
| Risk | higher $ | bracketing rule mis-identifies a crossing on a noisy 3×6 |
| **Verdict** | **recommended** | only if confirmed prices push A > ~$500 |

---

## 10. Risks & contingencies
- **Checkpoint drift** (the whole reason DeepSeek is being recollected): pin the
  exact checkpoint id per run; abort if the served checkpoint changes mid-campaign.
- **Batch latency** (Opus): ~24h; submit in Stage 0/1, not at the end.
- **Availability**: a config that refuses or caps at long rungs gets bound rows
  + the two-axis availability report — do not silently drop it.
- **Price change mid-campaign**: re-freeze `pricing.py` with dates; report list
  regardless, so a price move doesn't retro-change published numbers.
- **Underpower persists**: 6 instances still can't resolve the top three;
  budget the targeted separation seeds (G-stop rule) as a contingency line.

---

## 11. Executable checklist
- [ ] Confirm 4 ⚠️ prices; update `pricing.py` + dates
- [ ] Purge old DeepSeek V4 Pro/Flash run dirs → `EXCLUDED_RUN_DIRS`; regen board; parity gate green
- [ ] Land `event_trace.tsv` generator + scorer `first_divergent_event`; regression-anchor on v0 meter
- [ ] Commit pre-registration freezes (configs, seeds, brackets rule, scoring, adjudication, endpoint)
- [ ] Stage 0 probe (~$5) — all rows score + price sane
- [ ] Stage 1 founding 3×6 (six new configs); freeze brackets (B)
- [ ] Stage 2 depth (A: full 6×6 / B: bracketing top-up + payroll L25)
- [ ] Stage 3 n=20 replication subset (optional, ~$212)
- [ ] Analysis pipeline + capsule REBUILD OK + `make check`
- [ ] Evaluate gates G1–G4; decide order-vs-tiers; add separation seeds if needed
