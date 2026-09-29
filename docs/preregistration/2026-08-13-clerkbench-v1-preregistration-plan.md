---
title: ClerkBench v1 Preregistration Plan
date: 2026-08-13
status: draft — awaiting Adam's go/no-go per gate (§8)
type: preregistration
---

# ClerkBench v1 Preregistration Plan

## 0. Why this document exists, and what it is not

The v0 preprint (`paper-clerkbench/`) survived two adversarial reviews
(`docs/research/2026-07-19-red-team-report.md`,
`docs/research/2026-07-27-uncertainty-review-rulings.md`) and a length cut
(`docs/research/2026-08-12-length-cut-plan.md`). Both reviews independently
verified the measurement substrate — task construction, grading, raw-log
provenance — as sound, and both independently rejected the STRONG claims the
v0 board tried to support: a resolved ranking, a panel-wide causal mechanism
("anticipatory rationing"), and a "one tier, not an order" verdict asserted
rather than tested. The paper has already been reframed once (abstract now
reads "substantially shorter," not "2–5×"; the leaderboard already ships
hierarchical-bootstrap intervals; the leading three configs are already
described as overlapping). That reframe is necessary but not sufficient: it
turns overclaims into hedges. It does not turn the underlying board into a
**powered** instrument capable of resolving what the hedges concede it cannot
currently resolve.

This document is the plan for the data collection and analysis that would
close that gap. It is written preregistration-style: every estimand is
defined before any new data is collected, every test is named with its null,
its family, and its decision rule, and §8 is a gate a reviewer (or Adam) can
check off against without re-deriving anything. It touches no other file in
this repository and commits nothing on its own.

**What v0 already earned**, and what this plan explicitly builds on rather
than re-litigates:
- A generator-based, simulator-graded, no-tools measurement instrument with
  clean provenance (raw JSONL per attempt, immutable, traceable —
  `results/relbench/pilot/runs/`).
- An unbiased pass^k estimator (`scripts/research/regime_analysis.py:78`,
  the all-*k* complement of Chen et al. 2021's pass@*k*), a hierarchical
  bootstrap over instances and attempts (`scripts/research/ch6_bootstrap.py`),
  and a first attempt at a corrected divergence-depth null
  (`scripts/research/depth_null_analysis.py`).
- A documented, if incomplete, availability doctrine (refusal vs. cap vs.
  transport failure) and a failure-mode decomposition per cell
  (`docs/paper/generated/failure_decomposition.csv`).
- A costed, partially-adopted v1 protocol
  (`docs/research/2026-07-27-v1-protocol-and-budget.md`,
  `docs/research/2026-07-27-uncertainty-review-adjudication.md`) that this
  plan inherits rather than restates: native routes, valid-outcome vs.
  invalid-experiment slot ledger, 6×6 minimum cells, universal L=25 payroll
  rung, isotonic crossing sensitivity.

**What v0 has not earned**, which is the actual subject of this document:
a primary endpoint that isolates the genuinely empirical content of "CH6 is
shorter than capability" from its mechanical component (§1); enough seeds to
resolve the crossings the current board cannot (§2); an instrumentation fix
for a divergence-depth measure that is provably wrong for two of the four
families (§3); a powered, preregistered test of "anticipatory rationing"
instead of a descriptive one (§4); a real equivalence test behind "one tier,
not an order" (§5); and a grading/adjudication protocol decided before the
data that decides it (§6).

---

## 1. Primary endpoint: excess consistency loss

### 1.1 The claim under scrutiny, made precise

`paper-clerkbench/sections/06_results.tex` opens §6 with: "the consistency
horizon runs 2–4× shorter than the capability horizon." `sections/05_metrics.tex`
defines the two horizons: the capability horizon is the length $L^\*$ at which
pooled pass@1, $\bar p(L)$, crosses $0.5$; CH6 is the length at which
$\mathrm{pass}^6(L)$ — the probability that all six independent attempts on an
instance succeed, averaged over instances — crosses $0.5$.

Two facts about this comparison need to be separated, and the v0 text
conflates them.

**Fact A (trivial, assumption-free).** For any single instance and any $L$,
"all 6 of 6 attempts succeed" is a subset of the event "attempt 1 succeeds,"
so $\mathrm{pass}^6(L) \le \bar p(L)$ pointwise, for *any* model, *any* data,
*any* correlation structure between attempts. CH6 $\le$ capability horizon
follows immediately for any pointwise-decreasing curve. This costs nothing to
state and proves nothing about *how much* shorter.

**Fact B (the tautology the task brief flags).** Define the **homogeneous
i.i.d. null**: assume every instance in the cell shares one true per-attempt
success probability, $p_i \equiv \bar p(L)$ for all $i$. Under that
assumption alone, $\mathrm{pass}^6(L) = \bar p(L)^6$, so the *null* CH6 is
the length $\mathrm{CH6}_{\mathrm{null}}$ solving $\bar p(L)^6 = 0.5$, i.e.
$\bar p(\mathrm{CH6}_{\mathrm{null}}) = 2^{-1/6} = 0.8909\ldots$, against
$\bar p(L^\*) = 0.5$ for the capability horizon. Because $\bar p$ is
decreasing and $0.891 > 0.5$, $\mathrm{CH6}_{\mathrm{null}} \le L^\*$
**always**, for the same reason as Fact A — and the *entire* v0-reported
"2–4×" gap can, in principle, be reproduced from the pass@1 curve alone,
with zero attempts beyond $k=1$, zero claim about repeated-attempt behavior,
and zero instance heterogeneity. This is what "mechanical" means in the task
brief: at per-attempt $p=0.891$ vs. $p=0.5$, the SE quoted for the crossing
in the review material (`docs/research/2026-07-19-red-team-report.md` C2,
$\mathrm{SE}\approx 0.289$ at $m=3$ instances) is a statement about how
*precisely* $\mathrm{CH6}_{\mathrm{null}}$ or $\mathrm{CH6}_{\mathrm{obs}}$
can be *located*, not about whether the located value carries information
beyond $\bar p(L)$.

**Fact C (new to this plan; the reason the reframe is not just "add a
caveat").** $p \mapsto p^k$ is convex on $[0,1]$ for $k \ge 1$
($\frac{d^2}{dp^2}p^k = k(k-1)p^{k-2}\ge 0$), so by Jensen's inequality, for
*any* distribution of true per-instance probabilities $p_i$ with mean
$\bar p(L)$,
$$
\mathrm{E}_i[p_i^{\,6}] \;\ge\; \big(\mathrm{E}_i[p_i]\big)^{6} = \bar p(L)^6,
$$
with equality iff every instance has the same true $p_i$. This holds
regardless of *why* instances differ — genuine blind spots, ordinary
difficulty spread, anything. Consequently, real instance heterogeneity can
only push observed $\mathrm{pass}^6(L)$ **up** relative to the homogeneous
null at fixed $L$, which — since $\mathrm{pass}^6$ is decreasing in $L$ —
can only push the observed crossing **later**, i.e.
$$
\mathrm{CH6}_{\mathrm{null}} \;\le\; \mathrm{CH6}_{\mathrm{obs}} \;\le\; L^\*
\qquad\text{always.}
$$
$\mathrm{CH6}_{\mathrm{null}}$ is therefore not a curiosity but the
**theoretical floor** of the gap the paper reports, and any real
non-i.i.d. structure in how models fail can only *narrow* the "consistency
is way below capability" gap relative to that floor, never widen it. The
paper's framing, taken at face value, is not merely under-evidenced — it
sits on the side of the sandwich where genuine empirical content would
*shrink* the headline number, so reporting the raw gap without locating
$\mathrm{CH6}_{\mathrm{null}}$ risks overstating exactly the claim it is
making.

### 1.2 Two nulls, not one

The i.i.d. null ($\S1.1$, Fact B) is the strict floor: zero free parameters
beyond $\bar p(L)$, and it does not distinguish "ordinary" difficulty
variation across instances (e.g. two ledgers that differ slightly in how
close balances sit to their minimums) from a genuine trap (an account-ID
collision one model reliably mishandles). A cell can beat the i.i.d. null
just from mundane heterogeneity, which is not the phenomenon v0's "instance
trap" language claims.

Define the **instance-conditioned (beta-binomial) null**: $p_i
\stackrel{\text{iid}}{\sim} \mathrm{Beta}(\alpha_0,\beta_0)$ across
instances in the cell, with $\alpha_0/(\alpha_0+\beta_0) = \bar p(L)$
(mean-matched to the *observed* pooled pass@1 for that cell) and
concentration $\kappa_0 = \alpha_0+\beta_0$ **fixed ex ante, not fit per
cell**. Fitting $\kappa_0$ to the very cell being tested would make the null
absorb the heterogeneity it is meant to test for (a cell with a real trap
would simply widen the fitted Beta until the trap looked like ordinary
dispersion) — this is the failure mode `ch6_bootstrap.py`'s
`moment_match_beta()` already flags as "PRIOR-SENSITIVE" for degenerate
cells (`scripts/research/ch6_bootstrap.py:481`), used there for a
*different* purpose (a secondary CI on CH6 itself). For the null, $\kappa_0$
must instead be calibrated from an *independent* reference: the **meter
family**, which the existing evidence (`paper-clerkbench/tables/heterogeneity.tex`;
"meter tracks its null at every length") already establishes as the
stochastic-slip regime — i.e. as the family where instance-to-instance
variation is closest to whatever "ordinary" dispersion looks like for this
generator family. Pool meter's per-instance success fractions across
configs and rungs, moment-match one $\kappa_0$, and hold it fixed for every
other family's beta-binomial null. Under a Beta-mixed binomial, the exact
moment is
$$
\mathrm{E}_{p\sim\mathrm{Beta}(\alpha_0,\beta_0)}[p^{6}]
= \prod_{j=0}^{5}\frac{\alpha_0+j}{\alpha_0+\beta_0+j},
$$
giving $\mathrm{CH6}_{\beta_0}$, the length at which this quantity crosses
$0.5$. By construction $\kappa_0<\infty \Rightarrow
\mathrm{CH6}_{\mathrm{null}} \le \mathrm{CH6}_{\beta_0} \le
\mathrm{CH6}_{\mathrm{obs}}$: the beta-binomial null absorbs ordinary
dispersion and leaves only genuine trap-like clustering as "excess."

### 1.3 The primary estimand

For every ranked (config, family) at every measured $L$:
$$
\Delta_{\mathrm{iid}}(L) = \widehat{\mathrm{E}}[p_i^{\,6}](L) - \hat{\bar p}(L)^6,
\qquad
\Delta_{\beta_0}(L) = \widehat{\mathrm{E}}[p_i^{\,6}](L) - \mathrm{E}_{\beta_0}[p^6],
$$
where $\widehat{\mathrm{E}}[p_i^{\,6}](L) = \frac{1}{m}\sum_i
\binom{c_i}{6}/\binom{n_i}{6}$ is the existing unbiased estimator
(`scripts/research/regime_analysis.py:78`, `unbiased_passk`), already
computed today for the nano/20-attempt calibration and (as `null_k3`/`ratio`)
for $k=3$ in `docs/paper/generated/regime_frontier.csv`. **This is the
primary endpoint of v1**, reported per cell with a bootstrap CI (reusing the
hierarchical instance-and-attempt resample already implemented in
`ch6_bootstrap.py`), and at the horizon level as
$$
\mathrm{ExcessHorizon}_{\mathrm{iid}} = \mathrm{CH6}_{\mathrm{obs}} - \mathrm{CH6}_{\mathrm{null}},
\qquad
\mathrm{ExcessHorizon}_{\beta_0} = \mathrm{CH6}_{\mathrm{obs}} - \mathrm{CH6}_{\beta_0}.
$$
Both are $\ge 0$ by construction (§1.1 Fact C); reporting them, rather than
the raw CH6-vs-capability gap, is what makes "the consistency horizon is
shorter than capability" a measurement rather than an algebra exercise:
$\mathrm{ExcessHorizon} \approx 0$ says the gap is fully explained by the
pass@1 curve's own shape (no new information in the 6-attempt board beyond
what a pass@1 sweep already gave); $\mathrm{ExcessHorizon} \gg 0$ says the
6-attempt board is finding something a pass@1 sweep could not — most likely
sticky, capability-gated blind spots on specific instances (the trap
regime), which is the actually interesting failure mode this benchmark is
built to surface.

### 1.4 Leaderboard consequence: rank stability under normalization

Compute a second ranking of the same configs by $\mathrm{ExcessHorizon}$
rather than raw CH6, and report the two side by side. Three outcomes are
distinguishable and each is reportable as a finding, not a failure mode:
1. **Stable** — the two rankings agree (Kendall's $\tau$ close to 1,
   computed via the existing pairwise bootstrap machinery on both metrics).
   Raw CH6, despite being partly mechanical, is tracking the genuine signal
   because the panel's pass@1 curves are similar enough in shape that the
   mechanical component is roughly constant across configs and cancels in
   the ranking.
2. **Compressed** — Excess-CH6 separates configs raw CH6 cannot (adjacent
   pairs that are indistinguishable in $\mathrm{CH6}_{\mathrm{obs}}$
   because they have near-identical pass@1 shapes turn out to have very
   different trap structure).
3. **Reordered** — the rankings genuinely disagree, meaning a config's raw
   CH6 rank is partly an artifact of its pass@1 curve's steepness rather
   than of anything specific to its repeated-attempt behavior. This would be
   the single most important v1 finding if it occurs, since it would mean
   the v0 board has been ranking curve shape, not consistency.

### 1.5 What already exists vs. what v1 must add

Already implemented and reusable with no new code: the unbiased pass^*k*
estimator, the hierarchical bootstrap resample, the meter-family
"stochastic-slip" reference regime as an empirical fact. New for v1: (a) the
beta-binomial null with an *externally* calibrated $\kappa_0$ (today's
`moment_match_beta` fits per cell — a different, valid use for a different
purpose, but not this one); (b) computing $\Delta_{\mathrm{iid}}$ and
$\Delta_{\beta_0}$ as first-class, published per-cell quantities rather than
an ad hoc regime classification (`docs/paper/generated/regime_frontier.md`
§1) run only where convenient; (c) the Excess-CH6 leaderboard and the
rank-stability comparison of §1.4. None of this requires new API spend
beyond what §2 collects for other reasons — it is an analysis-layer
addition over the existing and planned board.

---

## 2. Power and seed design

### 2.1 Why three instances fails, quantified on the current board

`scripts/research/ch6_bootstrap.py` already reports what three seed
instances per cell buys. From the current bootstrap output
(`docs/paper/generated/ch6_bootstrap.csv`), the top three ranked configs'
95% CIs are GPT-5.5 $[100,238]$, Sol $[100,183]$, Gemini 3.1 Pro
$[84,168]$ — fully overlapping — and the adjacent-pair separation
probabilities among them (the `pair` rows) are all in the noise band the
review flagged (e.g. Sol vs. Gemini 3.1 Pro: $P[\text{Sol}>\text{Gemini}]
\approx 0.62$–$0.73$ depending on pairing scheme). But not every adjacent
pair is unresolved: direct Opus (CH6 $59.0$) vs. `5.4-nano/xhigh` (CH6
$\le 50.0$) — ranks 6 and 7, the bottom of the ranked block — separates at
$P[\text{Opus}>\text{nano}] = 0.9525$ (independent resample) / $0.9435$
(joint-seed paired resample), both from the `pair`/`pair_joint` rows keyed
`anthropic/opus-4-8/high,5.4-nano/xhigh` in `ch6_bootstrap.csv`. The board
already demonstrates both failure modes side by side at $m=3$: it separates
a genuinely large gap (Opus vs. a config it beats by more than the width of
its own bootstrap interval) and fails to separate three genuinely close
configs whose true order — if one even exists at this resolution — is
unknown. Three instances is not "too few in general"; it is precisely
enough to resolve gaps of roughly a full CH6 rung and not enough to resolve
the 20–30-event gaps that separate the leading tier
(`docs/research/2026-07-27-uncertainty-review-rulings.md` ruling 13).

At the crossing itself, each cell's per-instance pass^6 indicator is
Bernoulli-like with variance $q(1-q)$ at true $q=0.5$, so the cell-mean
estimator over $m$ instances has $\mathrm{SE}(\hat q) = 0.5/\sqrt m$: $0.289$
at $m=3$, $0.204$ at $m=6$, $0.158$ at $m=10$, $0.107$ at $m=22$, $0.082$ at
$m=37$ — the last three matching ruling 13's own sketch
(`docs/research/2026-07-27-uncertainty-review-rulings.md`: "10, 22, and 37
instances... for 0.80, 0.90, and 0.95 correct-order probability" on a
30-event gap, under an optimistic $1/\sqrt m$ scaling from the observed
$m=3$ baseline). This plan adopts that arithmetic rather than re-deriving
a different one, and extends it with the delta-method step needed to state
it in event units.

### 2.2 Converting probability precision to event precision

$\mathrm{SE}(\hat q)$ is a statement about the crossing *probability*; the
quantity that matters for rank separation is the crossing *location* $L$.
By the delta method, at a crossing bracketed by rungs $(L_1,q_1)$,
$(L_2,q_2)$ with the pipeline's log-linear interpolation
(`scripts/research/build_report_tables.py:481`, `crossing()`), the local
slope in $\log L$ is $s = (q_1-q_2)/\log(L_2/L_1)$, so
$$
\mathrm{SE}(\hat L) \;\approx\; \frac{\mathrm{SE}(\hat q)}{s}\cdot L.
$$
Steeper brackets (larger $s$) buy more location precision per unit of
probability precision for free; this is the quantitative reason payroll's
L=25 universal rung and any future bracket-tightening rungs are worth more
per dollar near a crossing than adding instances at rungs where the curve is
flat (near 0 or 1) — consistent with Plan B's bracketing-first design
(`docs/research/2026-07-27-v1-protocol-and-budget.md`).

### 2.3 Instance count decision

**Decision: 6 instances × 6 attempts is the v1 floor for every cell that
feeds a ranked crossing** (adopting ruling 13's verdict), with **sequential
addition at the bracketing rungs only** — not uniformly — up to a budget
cap, per Plan B's bracketing-first allocation
(`docs/research/2026-07-27-v1-protocol-and-budget.md`). This buys
$\mathrm{SE}(\hat q)=0.204$ at every crossing (down from $0.289$), which by
$\S2.2$ roughly halves event-location SE at typical observed brackets, but
by ruling 13's own honest arithmetic **does not** reliably separate the
leading tier: moving 3→6 raises the correct-order probability for the
current GPT-5.5-vs-Sol gap only to about $0.67$, far short of a
confirmatory threshold. **v1 does not promise to resolve the leading tier's
order.** It promises: (a) every ranked crossing computed from six
*assessable* instances, not three (closing R6's 5-as-6 hole,
`docs/research/2026-07-27-uncertainty-review-rulings.md` ruling 6); (b)
sequential, predeclared instance addition at bracketing cells specifically,
funded up to the budget in §7, with the acceptance criterion of §5
(equivalence, not ordering) as the actual output for ties; (c) explicit,
published power numbers (below) so a reader knows what gap size the board
*can* and *cannot* resolve, rather than inferring it from silence.

| target correct-order probability (30-event gap, 1/√m scaling from the $m=3$ baseline) | instances/cell |
|---|---|
| 0.67 (current 6×6 floor) | 6 |
| 0.80 | ~10 |
| 0.90 | ~22 |
| 0.95 | ~37 |

The 0.90/0.95 tiers are unaffordable at full-panel scope (Bucket 3's own
costing puts the *6×6 minimum* alone at ~$550–800 all-in across four
families and five to seven configs,
`docs/research/2026-07-27-uncertainty-review-adjudication.md`); this plan
does not fund them panel-wide. It funds them **narrowly, only where a
specific pairwise comparison is load-bearing for a stated v1 claim** — e.g.
if v1's abstract wants to say config A beats config B rather than "A and B
are tied," that specific pair gets sequential instance addition toward the
0.80 tier at its bracketing cells before the claim ships, per the
sequential-precision rule already adopted in Plan B/ruling 13. Otherwise,
ties are published as tiers (§5).

### 2.4 Higher-repeat frontier subset: does the trap replicate off nano?

The nano trap (`paper-clerkbench/sections/06_results.tex` §6.6: dropzero at
$L{=}50$, one instance failed 16/20 times, a model×content interaction, "34
of 34 failures across the two windows carry the identical signature") is
the single strongest piece of evidence in the entire preprint for real
instance heterogeneity — and it exists **only** at $n=20$ attempts on a
small model. `docs/paper/generated/regime_frontier.csv`/`.md` and
`paper-clerkbench/tables/heterogeneity.tex` show it clearly: dropzero
observed pass^3 exceeds the i.i.d. null by $0.340/0.088 = 3.86\times$ at
$L{=}50$ (matching the abstract's "up to $3.9\times$"). The frontier board
runs at $n=6$, which cannot detect a 16/20-style trap at all — a config
that fails an instance 3 or 4 times in 6 is statistically indistinguishable
from ordinary variance at that $n$, and §1's excess-loss estimand is
underpowered exactly where the trap phenomenon is strongest and most
interesting. **This is the single largest unresolved empirical question the
current board leaves open**: is instance-trap heterogeneity a
small/non-reasoning-model phenomenon, invisible at the frontier because
frontier models genuinely do not have blind spots at this task's
difficulty — or is it present at the frontier too, just masked by $n=6$'s
resolution?

**Design.** Reuse the existing nano protocol
(`paper-clerkbench/sections/06_results.tex` §6.6: 20 attempts/instance,
$\approx\$5$ total at nano's ~\$0.03/call) at frontier prices. Target the
family and rungs where the trap actually appeared — dropzero, $L\in\{25,
50\}$ — on the same shared seed instances already used by the standard
board (so results are directly comparable to the $n=6$ board and can be
downsampled to check what an $n=6$ subsample of the $n=20$ data would have
found, which independently validates the "does not replicate at $n=6$"
claim on the very data collected for it). Sample of configs: the cheapest
and priciest ends of the ranked panel, so a null result cannot be blamed on
picking a config too weak to have blind spots — `5.4-nano/xhigh` (already
have this; re-run for the shared-seed alignment), `deepseek-v4-flash`
(cheapest frontier-adjacent config, ~\$0.06/call), and two genuine frontier
configs, `gpt-5.5/high` and `gemini-3.1-pro/high` (the two configs whose
depth-null cells are already flagged front-loaded in
`docs/paper/generated/depth_null.csv`, making them the most likely
frontier configs to show trap structure if it exists there at all).

| item | value |
|---|---|
| configs | gpt-5.5/high, gemini-3.1-pro/high, deepseek-v4-flash/default, 5.4-nano/xhigh (4) |
| family × rungs | dropzero × {25, 50} (2) |
| instances | 6 shared board seeds |
| attempts/instance | 20 |
| total calls | $4 \times 2 \times 6 \times 20 = 960$ |
| cost basis (`docs/research/2026-07-27-v1-protocol-and-budget.md`) | 5.5 ~\$0.25, 3.1 Pro ~\$0.45, DS-flash ≈ DS-Pro ~\$0.06 (cheaper route), nano ~\$0.03 |
| est. cost | $6\times20\times2\times(0.25+0.45+0.06+0.03) \approx \$212$ |

Probe-first: run one (config, $L$) cell first, confirm cost matches the
per-call basis before committing to the full $960$-call block, per the
"probe the largest/most expensive cell first" discipline already used for
the emission control (ruling 20).

### 2.5 Power for the excess-loss estimand

$\Delta_{\mathrm{iid}}$'s bootstrap CI width scales with the same
$1/\sqrt m$ instance-count logic as CH6's (it is a difference of two
functions of the same per-instance pass^6 estimates), so §2.3's 6×6 floor
applies to it directly with no separate derivation. What genuinely needs
$n=20$, not more instances, is not $\Delta_{\mathrm{iid}}$'s *location* but
its **existence at the per-instance level**: distinguishing "this instance
has true $p_i=0.3$" (ordinary difficulty) from "this instance has true
$p_i \approx 0$ except this model resolves the collision correctly and gets
$p_i=1$" (a trap) requires enough attempts on individual instances to
estimate $p_i$ itself with useful precision — at $n=6$, $\hat p_i \in
\{0,\frac16,\ldots,1\}$, a 7-point lattice too coarse to separate "low but
nonzero" from "genuinely near-zero." This is exactly what §2.4's $n=20$
subset is for, and it is the correct lever for this question — more
instances at $n=6$ each would sharpen the *cell-average* $\Delta$ estimate
but would not resolve whether any *individual* instance is a true trap, and
therefore would not test the frontier-replication question at all.

---

## 3. Per-event divergence instrumentation

### 3.1 What is broken today, exactly

The paper's divergence-depth measure (`paper-clerkbench/sections/06_results.tex`
Table `tab:depth`, and the byte-offset feeding
`scripts/research/depth_null_analysis.py`/`regime_analysis.py`) is computed
as `first_diff_index / target_length`: the byte position of the first wrong
byte inside the **first alphabetically mismatched file**, as a fraction of
that file's length. This is a direct read of
`scripts/research/copybench_file_output.py:1698-1722`
(`score_file_tree`): the loop `for path in sorted(expected_paths &
observed_paths)` walks files in **alphabetical order**, and `first_mismatch
= mismatched[0]` takes the first one found that way. There is no notion of
"the file that actually reflects event order" in this logic — it is a
byte-exact diff tool, not an event-time instrument, and it was never
supposed to be one.

For the meter family (`banded_meter_billing`), this happens to work: the
per-event output file is `out/bills.tsv`
(`scripts/research/truncation_analysis.py:101`, `LOG_FILE`), one row per
event with an explicit `seq`, and it plausibly sorts early enough
alphabetically among the family's other output files to usually be the
first mismatch. For the ledger family (`fee_ledger_dropzero`), it does not
work, for two independent reasons, both directly visible in
`scripts/research/reliability_abstention_pilot.py`:

- **No per-event log exists to diff against.** `out/rejections.tsv` logs
  only *rejected* transactions (`scripts/research/truncation_analysis.py:40`,
  explicitly commented "the ledger family has no per-event log, so this is
  a labeled necessary-condition PROXY only"), silently skipping every
  accepted event. A model's first divergence on an *accepted* transaction
  is invisible to it entirely.
- **The file most likely to be the alphabetically-first mismatch is not
  event-ordered at all.** `out/checkpoint.tsv` is built by `state_lines()`
  (`reliability_abstention_pilot.py:2513-2518`): one row per **account**,
  in account order, not per event — `"account\tbalance\tstatus\taccepted\trejected"`
  — and it is a single **snapshot**, frozen at one fixed point in the
  stream: `checkpoint_seq = n * 625 // 1000` (`reliability_abstention_pilot.py:3957`,
  i.e. 62.5% of the instance length — at $L{=}50$, `checkpoint_seq = 31`,
  matching the task brief's "frozen after a fixed 31 events" exactly). A
  byte offset inside this file cannot correspond to an event index under
  any interpretation: rows are ordered by account ID, and the entire file
  reflects state as of one proportional checkpoint regardless of how many
  events actually occurred afterward. "First divergent byte in
  `checkpoint.tsv`" measures which **account row** first diverges (a
  function of account-ID sort order and which account's arithmetic the
  model got wrong), not *when in the event stream* the model's execution
  first went off track. Every ledger-family row in `tab:depth` and every
  ledger-family cell in `depth_null.csv` inherits this problem; it cannot
  be fixed by re-deriving a better null (`depth_null_analysis.py` already
  did that, correctly, per its own docstring — it fixed the null, not the
  measure the null is tested against).

The task brief's characterization is precisely borne out by the code:
the instrument computes a **byte offset in whatever file alphabetized
first**, not an **event index**, and for the ledger family that file is a
non-chronological snapshot.

### 3.2 What already works and should not be rebuilt

Two of the four v1 families already have adequate per-event logs, confirmed
directly from their use as the *non-proxy* survival measure in
`scripts/research/truncation_analysis.py:37-39,101-103`:
- **meter** (`banded_meter_billing`): `out/bills.tsv`, one row per billing
  event, `seq`-keyed.
- **gateway** (`spent_tracking_gateway`): `out/request_log.tsv`, used
  directly (not flagged proxy) as the per-event survival measure.

Two do not, by the same evidence:
- **dropzero** (`fee_ledger_dropzero`): rejections-only proxy, no full log.
- **payroll** (`payroll_overtime_ledger`): the same `checkpoint.tsv` +
  rejections-only pattern (`scripts/research/payroll_adjudication_record.py:16`
  lists the same four-file shape — `employees.tsv / checkpoint.tsv /
  adjustments.tsv / rejections.tsv` — with no full event log either). The
  family-expansion plan already flagged this exact class of risk without
  resolving it: "Checkpoint semantics differ per family... keep the same
  'exact table immediately after event k' contract"
  (`docs/research/2026-07-18-family-expansion-plan.md`, Risk 3) — that risk
  is precisely the gap this section closes.

### 3.3 v1 spec: a canonical per-event trace, uniform across all four families

Every v1 family's output contract gains one designated file,
`out/event_trace.tsv`, satisfying:
1. **One row per event in the input stream, in `seq` order, with no
   gaps** — covering *every* event (accepted, rejected, or otherwise
   outcome-bearing), not only a distinguished subset. This is the concrete
   fix for dropzero and payroll; meter's `bills.tsv` and gateway's
   `request_log.tsv` already satisfy it and are simply designated as that
   family's `event_trace.tsv` (no generator change needed there beyond
   the designation itself).
2. **A common minimal schema** across families: `seq\touttcome\t<family
   fields>`, where `outcome` is drawn from a small closed vocabulary
   (`accepted`, `rejected:<reason>`, or the family's existing outcome
   labels) and every field is derivable from the prompt's explicit
   vocabulary — the same token-derivability gate already required of every
   other output file (`docs/research/2026-07-18-family-expansion-plan.md`
   Phase 1, item 4).
3. **A generator self-test asserting full coverage**: for a held-out
   instance, the count of `event_trace.tsv` rows equals $L$ exactly, and
   the file byte-identically reproduces under regeneration with the same
   seed (`docs/research/2026-07-18-family-expansion-plan.md` Phase 1, item
   5's byte-identity discipline, extended to this file specifically).
   `checkpoint.tsv`-style snapshots are **not removed** — they remain a
   useful independent check on final/mid-stream state — the fix adds a
   file, it does not repurpose one.

### 3.4 Grader change: first-divergent-EVENT, not first-mismatched-byte

`scripts/research/copybench_file_output.py`'s `score_file_tree` keeps its
existing alphabetical-first-mismatch logic for general-purpose diffing (it
is shared infrastructure and other consumers depend on its current
behavior) but gains a family-aware wrapper for ClerkBench that:
1. Always evaluates `out/event_trace.tsv`'s row-level diff, regardless of
   alphabetical file order, whenever that file is among the mismatched
   set.
2. Parses the file structurally (split on rows, then on the `seq` column)
   and reports **the `seq` of the first row that differs from gold**, not
   a byte offset — emitted as a new `first_divergent_event: <int | null>`
   field alongside (not replacing) the existing byte-level fields, so
   nothing downstream that reads `first_mismatch`/`first_diff_index` breaks.
3. Falls back to today's byte-offset behavior only when `event_trace.tsv`
   itself is entirely absent from the response (e.g. the model omitted the
   file, or malformed it beyond row-parsing) — a case that is itself
   diagnostic and is reported as a distinct `event_trace_missing` flag
   rather than silently degrading to a less meaningful number.

This is the artifact-level fix that makes §4's per-event hazard test
well-defined for every family, including the two that currently cannot
support it at all.

### 3.5 Validation gates and cost

Pure engineering: generator changes (per family, add or designate the
trace file; for dropzero/payroll, extend the existing per-event simulation
loop — already tracking every transaction's outcome internally,
`simulate_ledger_v3`, `reliability_abstention_pilot.py:2490-2570` — to also
*emit* one row per iteration instead of only accumulating into `rejections`
and the final `state_lines()`) and one grader change
(`copybench_file_output.py`, family-aware wrapper). **No incremental API
spend**: `event_trace.tsv` is generated by the simulator for gold, and
required of the model's own output going forward — it adds to the model's
required output length for dropzero/payroll (roughly the size of
`bills.tsv`/`request_log.tsv` at the same $L$, since it's the same
one-row-per-event shape), which changes those two families' effective
task difficulty slightly and **breaks byte-identical comparability with
v0's dropzero/payroll cells** — this must be treated as a new instance
generation, not a drop-in replacement, and is exactly the kind of change
`docs/research/2026-07-18-family-expansion-plan.md` Phase 1's
"byte-identity check" gate is designed to catch if attempted carelessly.
Required before any v1 dropzero/payroll collection: (a) the generator
change, (b) the self-test gate of §3.3.3, (c) a discrimination pilot
mirroring Phase 2 of the family-expansion plan (2 attempts × 3 instances,
GPT-5.5-high and nano/medium) to confirm the added output requirement does
not itself become the dominant failure mode (a model failing to *format*
the new file correctly is a format failure, not the execution reliability
this benchmark targets, and should be visible as such via the existing
`failure_type` taxonomy in `copybench_file_output.py:1710-1721`).

---

## 4. Rationing as a preregistered hypothesis

### 4.1 Primary confirmatory test

**Hypothesis (preregistered, not descriptive):** For a subset of
configurations, the first-divergent-event position (§3.4) is front-loaded
relative to a per-cell-calibrated truncated-geometric null — i.e. models
allocate reasoning effort in anticipation of total workload, producing
earlier failures on longer instances than a constant per-event hazard would
predict.

**Null model.** Per (config, family, $L$) cell, calibrate a constant
per-event hazard $h$ from that cell's *own* pass@1: $\hat q = c/n$ (with the
same zero-success boundary correction already used,
`scripts/research/depth_null_analysis.py:207-213`, `q_hat`), $h = 1 -
\hat q^{1/L}$. Under constant hazard, the first-divergent-event index $T$
among failing attempts is truncated-geometric on $\{1,\ldots,L\}$; its exact
distribution and Monte-Carlo test statistic are already implemented
(`depth_null_analysis.py:221-256`, `null_median_rel`, `simulate_medians`,
`mc_pvalue`) and are reused **without modification** — the null-model
machinery in v0 was already correct (red-team finding C1's own fix,
verified by the reproduction gate at `depth_null_analysis.py:104-133`).
**What changes for v1 is only the input measure**: $T$ is now
`first_divergent_event` (§3.4, an actual event index) instead of
`first_diff_index / target_length` read off a possibly non-chronological
file. Re-run the existing script's Stage 2 unmodified against the new
per-event trace once §3 ships.

**Motivating evidence for why this matters, not just in principle.** A
preliminary event-time reanalysis restricted to the meter family alone
(where `bills.tsv` already is a genuine per-event log, so no instrumentation
fix was needed to compute it correctly today) found **zero BH-significant
cells** — the front-loading signal the current byte-offset table shows
(e.g. `depth_null.csv`'s `gpt-5.5/high,meter,400` row: 7 failures, raw
$p=0.031$, not BH-significant within the meter-only stratum) does not
survive at meter's own resolution beyond a weak, uncorrected hint at
$L{=}400$ (raw $p\approx 0.009$–$0.03$ on 4–8 failures per cell — too few
failing attempts per cell for that raw $p$ to mean much before correction).
This is the meter-family evidence that the currently-published,
byte-offset-based "four significant cells" result
(`paper-clerkbench/sections/06_results.tex` §6.4) is not yet resting on a
trustworthy per-event measure, and it is the direct motivation for making
§3's instrumentation fix a **precondition** for re-running this test, not
an optional refinement.

**Power.** The limiting factor is failing-attempt count per cell, not
instance count: the depth statistic is computed only from failures, and
`depth_null.csv`'s own data shows most cells carry 1–12 failing attempts.
§2.3's 6×6 floor (36 attempts/cell) at a config with pass@1 $\approx 0.5$
near its crossing yields ~18 failures — enough for the existing Monte-Carlo
test to have reasonable power against a moderate front-loading effect (the
same order as the "real" effects already found and not retracted by the
byte-offset analysis, e.g. GPT-5.5 at $L{=}400$: observed $0.14$ vs. null
$0.41$, a factor-of-3 shift). Cells with pass@1 near 0 or 1 contribute few
or no failures and are structurally underpowered for this test regardless
of instance count — this is a property of the phenomenon, not a design
flaw, and should be disclosed as such rather than papered over with more
seeds.

### 4.2 Multiple-testing plan

Adopts ruling 8 verbatim (`docs/research/2026-07-27-uncertainty-review-rulings.md`):
named, prospective families, not one global correction.
- **Depth-null family**: BH (FDR 0.05) across all pooled (config, $L$)
  cells with $\ge 1$ failure, computed once per family stratum (pooled and
  per-family, as `depth_null_analysis.py` already stratifies at
  lines 374–381) — this family now runs on the event-time measure.
- **Homogeneity-screen family** (§1's trap detection, `chi2_homogeneity_p`
  in `regime_analysis.py:84-100`): BH across the ~35–61 cells with $\ge 6$
  attempts/instance, separately from the depth family.
- **Each matched-control experiment** (truncation, emission, the §2.4
  higher-repeat subset): Holm or an exact predeclared contrast within that
  experiment's own small set of comparisons, never folded into the two
  families above.
- Everything else (single-cell descriptive $p$-values, e.g. the token-slope
  regressions of §4.3) is reported unadjusted and explicitly labeled
  descriptive.

Published wording (reused from ruling 8): "We do not claim paper-wide
family-wise error control. Multiplicity is controlled within each named
exploratory or confirmatory test family; all other $p$-values are labeled
unadjusted."

### 4.3 Token-per-event slope, disentangled from fixed overhead

`paper-clerkbench/sections/06_results.tex` §6.4 already states the
confound precisely: "A fixed per-task reasoning overhead mechanically
lowers this ratio (per-event reasoning is of the form $a/L + b$)." No
script currently fits or removes $a$; the paper reports the raw ratio
$e(L{=}400)/e(L{=}50)$ and flags it as merely suggestive. v1 fits it.

**Model.** For each (config, family) with token usage at $\ge 3$ rungs
(already logged on every attempt — this needs **no new API spend**, only
new analysis over existing and §2's planned collection), regress total
reasoning tokens $T$ against $L$:
$$
T(L) = a + bL + cL\log L \;+\; \varepsilon,
$$
nesting the "fixed overhead + constant marginal cost" model ($c=0$, giving
$e(L)=T(L)/L = a/L+b$, flat once overhead is removed) inside a model where
the marginal cost itself declines with $L$ ($c<0$, the anticipatory
signature). Report $\hat a$ (the fixed-overhead estimate), the
overhead-corrected per-event rate $\hat e_{\mathrm{corr}}(L) =
(T(L)-\hat a)/L$, and a test of $c=0$.

**The disentangling step, concretely.** Today's ratio conflates two
mechanisms that make $e(L)$ decline: (i) a start-up cost $a$ amortized over
more events (mechanical, not rationing), and (ii) a genuinely
length-dependent marginal cost $b(L)$ (the rationing hypothesis). Removing
$\hat a$ and re-plotting $\hat e_{\mathrm{corr}}(L)$ isolates (ii): if
$\hat e_{\mathrm{corr}}(L)$ is flat once $a$ is subtracted, the observed
decline in the raw ratio is fully explained by amortized overhead and the
token evidence for rationing evaporates; if $\hat e_{\mathrm{corr}}(L)$
still declines, that is evidence $b$ itself shrinks with $L$, independent
of the depth-based test in §4.1.

**Power caveat, disclosed rather than hidden.** With rungs at
$\{25,50,100,200,400\}$ (5 points) and a 3-parameter model, per-config
degrees of freedom are thin (2 residual df). Per-config significance for
$c$ is not reliable at this resolution; the primary confirmatory read is a
**pooled/hierarchical fit** — $c$ shared across configs within a lab or
across the whole panel, with config-specific $(a,b)$ — reported as the
population-level curvature estimate, with per-config $(\hat a,
\hat e_{\mathrm{corr}})$ reported descriptively (unadjusted, per §4.2). This
requires no additional rungs beyond what §2's crossing-bracketing campaign
already buys, since every ranked attempt already carries usage data.

### 4.4 Decision rule

Rationing is confirmed for a configuration only if **both** legs hold after
correction: (a) a BH-significant, calibration-robust depth-null deviation
in the "earlier" direction (§4.1, on the event-time measure, robustness
band per `depth_null_analysis.py`'s existing grid check) at $\ge 1$ cell,
**and** (b) a significant negative $c$ in the pooled overhead-corrected
token regression (§4.3) for that same configuration or its lab. Either leg
alone is reported as suggestive, not confirmatory, and is not used to
support a panel-wide claim in the abstract (consistent with ruling 15's
existing decision to demote rationing out of the abstract while keeping it
prominent in §6).

---

## 5. Equivalence testing for "one tier" claims

### 5.1 The gap being filled

`paper-clerkbench/sections/06_results.tex`'s current uncertainty paragraph
asserts "the leading configurations are one tier, not an order" from
overlapping bootstrap CIs and a stated separation-probability range. Failure
to reject "A > B" is not evidence that A and B are equivalent — it is
consistent with "genuinely different but this design cannot tell," which is
a different claim the reader cannot distinguish from the current wording.
This section replaces the assertion with an actual equivalence test.

### 5.2 Predefine the margin, in events, before looking at v1 data

**Margin rule**: two configs' CH6 values are declared **practically
equivalent** if $|\mathrm{CH6}_A - \mathrm{CH6}_B| $ would not exceed
$$
\delta = \max(10\text{ events},\; 0.10 \times \min(\mathrm{CH6}_A, \mathrm{CH6}_B))
$$
— i.e. at least 10 events, or 10% of the smaller of the two horizons,
whichever is larger. At the current board's scale ($\mathrm{CH6}\approx
100$–$130$ for the top three), this gives $\delta\approx 10$–$13$ events, a
substantially tighter and more defensible bar than the $20$–$30$-event gaps
ruling 13 already treats as "the gaps that matter" — so a positive
equivalence finding under this margin is a real claim, not one gerrymandered
to be easy to satisfy. This margin is fixed **before** any v1 seed
expansion (§2) runs against it, per standard TOST practice.

### 5.3 Test procedure

Reuse `ch6_bootstrap.py`'s existing joint-seed paired resample
(`joint_seed_replicates`, §5c in that script's docstring) — already built
to remove the shared-seed nuisance component from pairwise comparisons —
but change its output from a one-sided sign count (`gt`/`tie`/`lt`, the
current `pair_joint` rows) to the **replicate-level difference
distribution** $D = \mathrm{CH6}_A - \mathrm{CH6}_B$ per bootstrap draw.
Two one-sided tests (TOST): declare equivalence if the 90% percentile CI of
$D$ (equivalent to two one-sided $\alpha=0.05$ tests) lies entirely within
$(-\delta,\delta)$. This is a small, additive change to an already-written
function — no new collection is required to compute it on the current
board, though its power to detect equivalence (rather than merely fail to
reject a difference) benefits from §2's instance additions the same way
ordinary separation does.

### 5.4 Reporting convention

Every adjacent ranked pair gets one of three labels, published in the
leaderboard itself rather than left to a prose footnote:
- **Separated**: $D$'s 95% CI excludes 0 (the existing ordering claim).
- **Equivalent**: $D$'s 90% CI $\subset (-\delta,\delta)$ (the TOST
  criterion, §5.3).
- **Indeterminate**: neither — the current design cannot distinguish "close
  but different" from "genuinely tied" for this pair. This is the honest
  label for most of the current leading trio at $n=3$, and the label §2's
  seed additions are meant to move pairs *out of*, in either direction
  (into Separated or into Equivalent), rather than a permanent resting
  state.

---

## 6. Grading and protocol preregistration

### 6.1 Strict-contract and normalized-content, published side by side

`paper-clerkbench/sections/05_metrics.tex` already documents that the
grader normalizes two transport features before content comparison: CRLF
line endings, and a two-bracket `">>` file-block delimiter read as the
intended `">>>`. `scripts/research/rescore_delimiter_slip.py` confirms this
normalization currently changes the scored outcome for exactly one
configuration — DeepSeek V4 Flash, both routes — and that the change is
large: on the affected attempts, the two-bracket slip is present in 166 of
168 attempts (`paper-clerkbench/sections/06_results.tex` §6.2's "cheap
content-strong row" paragraph), moving the config from effectively unscored
under the strict (pre-normalization) contract to its current published
rank-5 CH6 of 84. **Today only the normalized number is published** — the
strict-contract number is not shown anywhere in the paper or the released
aggregates, so a reader cannot see the size of this one grading decision's
effect on the board. v1 publishes both, per config, as two columns (or two
CSV fields) rather than one silently-normalized number: `ch6_strict` (no
transport normalization) and `ch6_normalized` (current pipeline). Where
they diverge by more than the equivalence margin of §5.2, the leaderboard
flags the row as **grading-sensitive** rather than letting the normalized
number stand alone as if it were the only defensible read.

### 6.2 Blinded adjudication policy, predeclared

The current adjudication overlay (`results/relbench/pilot/adjudications/
2026-07-08-dropzero-status-vocab.json`, 51 entries) reverses failures where
a model's output uses a semantically equivalent status label the prompt's
rulebook did not explicitly enumerate — a defensible policy, independently
re-derived and verified exact by the red-team review
(`docs/research/2026-07-19-red-team-report.md`, numbers-audit item
"Adjudication overlay"). But it was written and applied **after** seeing
which model it helped: 38 of the 44 currently-applied reversals accrue to
one config, Gemini 3.1 Pro, moving its CH6 from an unranked $\le 59.6$ to a
ranked $100.1$ (rank 3) — a swing large enough to change whether the config
is ranked at all. The policy itself is sound; the order of operations is
not blinded, and the current paper does not disclose the concentration.

**v1 policy, preregistered before any v1 attempt is scored:**
1. The label-equivalence rule (what counts as a reversible status-vocab
   slip) is written and frozen from the v0 rulebook text alone, before any
   v1 model's outputs are read.
2. Every adjudication decision records, at write time, a `score_blind`
   field: whether the adjudicator could see which config/rank the row
   belonged to when the call was made. The existing slot-ledger lineage
   fields already adopted for v1 (`parent_retry`, `supersedes`,
   `docs/research/2026-07-27-uncertainty-review-rulings.md` ruling 9) are
   extended with this one field at no additional engineering cost, since
   the ledger infrastructure already exists.
3. Per-config reversal counts and their effect on CH6 are published in the
   leaderboard notes, not buried in a provenance file — closing the exact
   inconsistency the red-team review caught between the paper's "all 50,"
   the overlay's 51 entries, 44 applied, and PROVENANCE.md's "14"
   (`docs/research/2026-07-19-red-team-report.md`, M5).

### 6.3 Raw vs. adjudicated boards, both published

Direct consequence of §6.2: v1 ships the leaderboard computed **without**
the overlay alongside the one computed **with** it, for every config the
overlay touches, not only Gemini 3.1 Pro. A reader who trusts the
adjudication policy reads the adjudicated board; a reader who wants the
byte-exact contract with zero researcher judgment reads the raw one. Both
already exist as intermediate pipeline states (`build_report_tables.py`
applies the overlay via `load_adjudicated()`/`(rel, task_id,
attempt_index) in adj` checks that are trivially toggleable) — this is a
reporting change, not a new analysis.

### 6.4 Two-axis availability metric

`docs/paper/generated/failure_decomposition.csv` already decomposes every
cell into `wrong_answer / parse_failed / refusal / other_error /
availability_failures / execution_failures / excluded_budget_capped /
excluded_transport` — the infrastructure for this section already exists
and needs no new collection, only two new headline numbers computed from
columns that are already there. Publish, per config:
- **Intention-to-treat CH6** (ITT): the current doctrine — refusals and
  provider-envelope stops score as failures, researcher-induced caps and
  transport errors void the slot for replacement (§R3's partition,
  `docs/research/2026-07-27-uncertainty-review-rulings.md` ruling 3,
  already adopted into the v1 protocol). This is "how long can you trust a
  batch against this deployed configuration, refusals and all" — the
  number that matters for an operator who cannot control the model's
  refusal policy.
- **Completion-conditional CH6** (CC): computed only over attempts that
  produced an assessable artifact (`execution_failures` in
  `failure_decomposition.csv`'s own terms), i.e. conditioning out refusals
  and availability failures entirely. This is "how reliable is the model's
  execution, given it attempted the task" — the number that isolates
  capability from serving/safety policy.
Both are already partially present in the text (Fable's "completion-
conditional pass rates" are disclosed narratively,
`paper-clerkbench/sections/06_results.tex` §6.2) but not as a systematic,
published pair of columns for every config, which is what makes ruling 4's
"availability-limited, not refusal-censored" resolution auditable rather
than asserted (`docs/research/2026-07-27-uncertainty-review-rulings.md`
ruling 4).

---

## 7. Budget and scope

### 7.1 Cost basis

Reused verbatim from the last approved costing pass
(`docs/research/2026-07-27-v1-protocol-and-budget.md`): GPT-5.5 ~\$0.25,
Sol ~\$0.20, Gemini 3.1 Pro ~\$0.45, direct Opus ~\$0.55, DeepSeek Pro
~\$0.06, nano ~\$0.03 per ladder call at the founding-family rungs. Existing
reusable data: two founding families at 3×6 across four rungs for the
ranked five, plus payroll/gateway screening.

### 7.2 Line items

| item | source | est. cost |
|---|---|---|
| Four-family, 6×6 minimum, bracketing-tiered (Plan B, R13-updated) | `docs/research/2026-07-27-v1-protocol-and-budget.md` Plan B + Bucket 3 doubling for 4-family/6×6 | \$550–800 |
| Higher-repeat frontier subset (§2.4: does the nano trap replicate) | new, this plan | ~\$212 |
| Sentinel matched-context arm, per new model (R14) | `docs/research/2026-07-27-uncertainty-review-adjudication.md` Bucket 3 | ~\$25/model |
| Sequential instance addition for load-bearing pairwise claims (§2.3) | new, this plan; funded only where a specific claim needs it | \$50–150 (contingent) |
| Per-event instrumentation (generator + grader engineering, §3) | new, this plan | \$0 API / engineering time only |
| Compute-vs-emission control | already run (ruling 20; git log `Compute-vs-emission decomposition control`) | \$0 (sunk, ≤\$180 spent) |
| Slot replacements (R6, closing 5-as-6) | already run (git log `Slot replacements integrated`) | \$0 (sunk, ~\$18 spent) |
| **Total incremental** | | **~\$830–1,190** |

This is above Plan B's original \$260–330 (`docs/research/2026-07-27-v1-protocol-and-budget.md`)
because it inherits the post-review Bucket 3 correction that Plan B's
minimum roughly doubles once R13's 6×6-everywhere and the four-family
scope are both applied (`docs/research/2026-07-27-uncertainty-review-adjudication.md`:
"new planning envelope ~\$550-800 all-in"), plus the two genuinely new
items this plan adds (§2.4's replication subset and contingent
sequential-addition spend for load-bearing pairs). It excludes chasing the
0.90+ ordering-probability tiers panel-wide (§2.3), which the review's own
numbers price beyond any defensible budget.

### 7.3 What v0 ships as vs. what v1 earns

| | v0 (current) | v1 (this plan) |
|---|---|---|
| Framing | Instrument note: a validated measurement tool, a descriptive board, hedged uncertainty | Powered comparative claims, where the power exists; honest ties elsewhere |
| Primary endpoint | Raw CH6 vs. capability horizon gap (partly mechanical, §1) | Excess-CH6 beyond the i.i.d. and beta-binomial nulls (§1) |
| Seeds | 3/cell (quantized to $\{0,\tfrac13,\tfrac23,1\}$) | 6/cell floor, sequential addition at load-bearing pairs |
| Instance-trap evidence | Only at nano, $n=20$, off the ranked board | Tested directly at the frontier, $n=20$ subset (§2.4) |
| Divergence depth | Byte offset in the alphabetically-first mismatched file; wrong instrument for 2 of 4 families | Event index from a dense per-event trace, uniform across families (§3) |
| Rationing | Descriptive (token ratio + one corrected-null pass) | Preregistered, two-leg confirmatory test with a decision rule (§4) |
| "One tier" | Asserted from overlapping CIs | TOST equivalence test against a predeclared margin (§5) |
| Grading | One normalized number per config | Strict and normalized side by side; flagged where they diverge (§6.1) |
| Adjudication | Applied, then disclosed after the fact | Frozen before scoring, score-blind flag recorded, raw+adjudicated boards both published (§6.2–6.3) |
| Availability | Availability-dominated flag on one config (Fable) | Two-axis ITT/completion-conditional CH6 for every config (§6.4) |

### 7.4 Sequencing

1. §3 (per-event instrumentation) ships first and is a hard precondition
   for §4's confirmatory rationing test on dropzero/payroll — it is pure
   engineering, zero API spend, and every other line item benefits from
   having it in place before new collection starts (a v1 dropzero/payroll
   cell collected before the instrumentation fix would need to be
   re-collected, not merely re-analyzed).
2. §2.3's four-family 6×6 floor and §2.4's higher-repeat frontier subset
   run in parallel once §3 lands for the families that need it (meter and
   gateway can start immediately; dropzero and payroll wait on §3).
3. §1's excess-loss endpoint, §4's rationing test, and §5's equivalence
   test are analysis passes over the same collection and can be computed
   incrementally as cells complete — none require the full campaign to
   finish before producing a first result.
4. §6's grading/adjudication protocol changes are policy decisions with
   near-zero marginal cost and should be frozen **before** step 2 begins,
   not applied retroactively, since §6.2's entire point is that the
   adjudication rule must be written before v1 outputs are read.

---

## 8. Decision-gate summary

| gate | pass criterion | if failed |
|---|---|---|
| G1 — primary endpoint defined | §1's $\Delta_{\mathrm{iid}}$/$\Delta_{\beta_0}$ computable from existing + planned data, $\kappa_0$ calibrated from meter, published per cell | Do not publish a v1 "consistency << capability" headline without it |
| G2 — seed floor met | Every ranked crossing computed from $\ge 6$ assessable attempts on $\ge 6$ instances (§2.3) | Config is unranked, bound published, not a point estimate |
| G3 — frontier trap question answered | §2.4's 960-call subset run and reported, whichever way it comes out | Do not claim the nano trap "does not replicate" or "replicates" at the frontier without it |
| G4 — per-event instrumentation live | §3's `event_trace.tsv` + grader change shipped and self-test-gated for all four families | No confirmatory rationing claim (§4) for dropzero or payroll |
| G5 — rationing decision rule applied | Both legs of §4.4 checked per config before any config is described as "rationing" | Report as suggestive only, out of the abstract |
| G6 — equivalence tested | Every adjacent ranked pair labeled Separated/Equivalent/Indeterminate per §5.4 | Do not say "one tier, not an order" without the TOST backing it |
| G7 — grading transparency | Strict and normalized CH6 both published; adjudication frozen pre-hoc with raw+adjudicated boards (§6.1–6.3) | Do not publish a single normalized-only number as if it were the only defensible read |
| G8 — availability two-axis | ITT and completion-conditional CH6 published for every config, not only availability-flagged ones (§6.4) | Availability doctrine remains asserted per-config rather than measured panel-wide |
| G9 — budget approved | §7.2's ~\$830–1,190 incremental spend approved by Adam before collection starts | Fall back to Plan C scope (`docs/research/2026-07-27-v1-protocol-and-budget.md`) and narrow §2.3/§2.4 accordingly |

v1 ships only once G1–G8 are met for every claim that appears in its
abstract; a claim without its gate met is demoted to a disclosed limitation,
per the same discipline the v0 reframe already applied once.
