---
title: ClerkBench Uncertainty Review Rulings
date: 2026-07-27
type: review
status: final
---

# ClerkBench Uncertainty Review Rulings

## Overall Judgment

ClerkBench has a strong core contribution: a length-indexed, repeated-attempt
measure of exact end-to-end artifact reliability. I would not ship the current
paper and release unchanged, however. The largest problems are not the basic
idea; they are an inconsistent availability estimand, invalid tolerance for
five-attempt cells, weakly identified rank uncertainty, stale released
per-instance counts, and causal language that does not yet separate computation
from artifact emission.

The score should survive these changes. The exact ordering and several claims
should not be treated as fixed until they are made.

## Evidence Reviewed

- `paper-clerkbench/main.pdf` and its LaTeX sources
- `release/clerkbench-v0-preprint/aggregates/`
- Relevant scripts under `scripts/research/`
- Public release documentation under `release/clerkbench-v0-preprint/`
- Fresh recomputation from the canonical local run set, without changing it
- Visual rendering of all 33 PDF pages

The rendered PDF is visually clean: I found no clipping, overlap, broken table,
or unreadable glyph. The serious issues are methodological, editorial, and
release-integrity issues.

## Decision Standard

Each item receives one of three verdicts:

- **Agree:** keep the current choice, with any clarifying disclosure stated.
- **Change:** replace the choice before shipping.
- **Needs work:** retain the underlying direction only after a specified
  analysis, rule, or presentation change.

The final review will distinguish construct validity, operational usefulness,
statistical identification, and reproducibility rather than treating them as
interchangeable.

## Rulings

### 1. What CH6 measures

**Verdict: change.**

Keep CH6, but define it as the **operational consistency horizon of a dated
served configuration**. It is not an intrinsic cognitive property of model
weights: route, refusal policy, sampling policy, input length, and output
envelope demonstrably affect it. Mechanism heterogeneity does not require
inventing additive workload-linked and context-linked CH6 components; the
current controls do not identify additive shares. Publish the mechanism profile
beside the score as a diagnostic.

Also remove the claim that CH6 directly marks where "a single unsupervised run"
becomes untrustworthy. That is the pass@1 horizon. Under homogeneous iid
attempts, pass^6 = 0.5 corresponds to per-attempt success
\(2^{-1/6}=0.891\), not 0.5. A precise replacement is:

> CH6 is the batch length at which six independent executions all succeed with
> even odds, for a specified route, sampling policy, and deployment envelope.

### 2. Payroll's length-flat hazard

**Verdict: agree.**

Keep payroll in the operational aggregate. A model that fails one-third of
short payroll runs has a real clerical-trust problem even if the failure hazard
does not rise with length. Removing the family would optimize the score toward
a pure slope construct that the paper says it is not measuring.

Do not describe its contribution as evidence of length-linked degradation.
Treat it as a left-censored reliability floor, and add common lower payroll
rungs for every ranked configuration. Start with L=25; add L=12 if L=25
remains below the pass^6 threshold. This must be family-wide, not selectively
added only to configurations near the observed boundary.

### 3. Availability doctrine

**Verdict: change.**

The clean partition is based on whether the event belongs to the predeclared
measurement envelope:

1. **Evaluator-invalid:** local crash, exhausted research credit, accidental
   client deadline, or harness cap below the declared target envelope. Void the
   slot and replace it under the frozen configuration; otherwise leave the cell
   incomplete.
2. **Service outcome inside the envelope:** refusal, provider maximum,
   provider-side terminal error, or expiry of a declared deployment SLA. Score
   it as an availability failure.
3. **Completed outcome:** grade the artifact.

A 2,400-second timeout is therefore invalid only when it was an accidental
research guardrail. If 2,400 seconds is the promised service deadline, it
scores. Record fields such as `limit_owner`, `configured_limit`,
`provider_max`, `deadline_owner`, and retry lineage so the distinction is
executable rather than interpretive.

The current pipeline cannot implement the stated three-way doctrine.
`build_report_tables.py` excludes every `length` or `max_tokens` row without
recording who owns the limit. The released `tables.md` simultaneously says
60K cap hits count as failures, while the paper and builder exclude cap hits.
Resolve this contradiction from historical row-level manifests before
shipping.

### 4. Fable 5

**Verdict: change.**

Unranking Fable specifically because refusals dominate is inconsistent with
the chosen end-to-end estimand. If a refusal is a failure because the operator
receives no artifact, Fable's refusal-inclusive score belongs in the same score
table. Call it **availability-limited**, not "refusal-censored": the refusals
are observed failures, not missing outcomes.

Its \(\leq84\) bound does not support a forced ordinal rank because it overlaps
Opus 59 and lower censored rows. Give Fable an ordinal interval or leave the
rank number unresolved for the mathematically correct reason: overlapping
bounds. Add separate availability and completion-conditional execution
columns. The disclosed meter completion rates
0.86/0.83/0.80/0.57 are useful diagnosis, not an alternative primary score.

### 5. Hierarchical bootstrap with three instances

**Verdict: needs work.**

The bootstrap is meaningful as a **finite-design sensitivity analysis**, not
as a calibrated population 95% confidence interval. With three seed instances,
the empirical cluster distribution has only three support points. The second
stage treats each observed \(c/n\) as the true attempt probability, so 0/6 and
6/6 instances contribute no within-instance uncertainty. A Bayesian hierarchy
cannot manufacture the missing seed information; with three groups, its
between-instance variance will be prior-sensitive.

Keep the current bootstrap, but:

- label its intervals as empirical design-sensitivity intervals;
- add leave-one-seed-out ranges;
- add a beta-binomial or hierarchical Bayesian sensitivity with at least two
  defensible priors;
- resample shared seeds jointly across models for pairwise comparisons rather
  than bootstrapping configurations independently; and
- report the top configurations as one tier.

Suggested paper caveat:

> These intervals resample three observed seeds per cell and attempts within
> them. They quantify sensitivity to this finite seed set, not calibrated 95%
> coverage over the generator population; unseen instance modes are not
> represented and the intervals may be anti-conservative.

### 6. Five clean attempts counted as protocol-6

**Verdict: change.**

Remove the tolerance. The unbiased estimator
\(\binom{c}{6}/\binom{n}{6}\) does not exist at \(n=5\). The implementation's
fallback is an all-correct indicator, which estimates pass^5, not pass^6; the
brief's description of it as a plug-in pass^6 estimate does not match the code.

Require six assessable attempts for every scored instance. Re-run invalid
slots under the frozen serving configuration or make the configuration
unrankable. In the current canonical rows, nine full-tier instance slots have
only five clean attempts; this affects the ranked Gemini 3.1 Pro and direct
Opus rows as well as Fable and the Opus route comparison. This is small,
bounded recollection and should be completed rather than modeled away.

### 7. Crossing interpolation

**Verdict: needs work.**

Disclosure alone is insufficient for a headline ranking, but this does not
need a large new study. Add a systematic sensitivity table comparing the
current first-downward-bracket rule with a monotone fit on log length and a
conservative crossing range. On current canonical data, an equal-weight
isotonic refit changes direct Opus from CH6 59 to 61 and leaves the ordering
unchanged; that is exactly the robustness result the appendix should show.

For v1, pre-register a monotone estimator and refit it inside every bootstrap
replicate. If the intended population curve is not assumed monotone, then a
single "horizon" is not well-defined and the paper must report all crossings or
a threshold-exceedance set instead.

### 8. Multiplicity

**Verdict: needs work.**

Do not apply one global BH correction to every p-value in the paper. The tests
do not form one coherent discovery family, and the primary CH6 estimates are
not null-hypothesis tests. Instead, define families prospectively:

- BH across the 61 exploratory depth cells;
- BH across the roughly 35 homogeneity screens;
- Holm or an exact predeclared contrast family within each matched-control
  experiment; and
- unadjusted descriptive p-values elsewhere, clearly labeled as descriptive.

Honest wording:

> We do not claim paper-wide family-wise error control. Multiplicity is
> controlled within each named exploratory or confirmatory test family;
> leaderboard estimates and intervals are descriptive, and all other p-values
> are labeled unadjusted.

### 9. Deduplication

**Verdict: change.**

Neither "always dedupe by attempt index" nor "count every row" is correct.
`attempt_index` is a protocol slot, not a globally unique sample identity.
Counting every separately run row would over-weight selectively remediated
models and instances; silently keeping one can outcome-select among genuine
repeats.

The current local set has 90 duplicate keys and 91 extra rows; 24 duplicate
keys disagree in outcome or status. Counting all rows happens not to change
the present Table 4 scores, which is reassuring, but it does not validate the
rule. The current "else first" preference also depends on unsorted file
discovery for equally eligible rows, so it is not fully deterministic.

For v1, give every request a UUID and every intended observation a protocol
slot. Record `parent_retry`, `supersedes`, and a score-blind reason. Exactly one
valid outcome fills a slot; independent replication campaigns receive new
slots and are analyzed separately. Freeze that canonical manifest before
looking at scores, then publish count-all and alternate-canonicalization
sensitivities for v0.

### 10. Canonical direct Opus row

**Verdict: agree.**

The direct row is the right canonical target because the aggregator collection
violated the intended serving protocol through a silent 64K cap and T=0. The
direct result is not the more flattering one: CH6 is 59 direct versus 65 on
the aggregator route, and the bootstrap route comparison is near even.

Add one chronology sentence. If the direct-route canonicality rule was not
timestamped before seeing the direct outcomes, call it a post-data but
score-independent protocol correction. Also call the comparison a
**multi-factor serving-envelope sensitivity**, not a pure route effect:
route, temperature, and output budget all changed.

### 11. Sampling policy

**Verdict: needs work.**

Require a uniform **selection rule**, not a uniform numeric temperature. T=0
is not representative of ordinary deployment, is not deterministic in
practice, and is unavailable on adaptive-thinking routes. Provider defaults
are heterogeneous, but that is acceptable once the estimand is explicitly a
served configuration.

For v1, pre-register: native provider route where available; provider-recommended
sampling with no caller override; temperature unset where adaptive reasoning
requires it; a non-binding or provider-maximum output envelope; and an exact
request manifest, route, and snapshot date. T=0 and temperature sweeps belong
in secondary within-model controls, not the primary cross-provider ranking.

### 12. Selective extra rungs

**Verdict: change.**

The bias is real when the same noisy observations both select support and
estimate the crossing. Use a two-stage adaptive design:

1. Run universal anchor rungs.
2. Use separate placement instances to choose refinement rungs.
3. Lock the support map using a model-agnostic rule, such as adding L=25 when
   the placement interval at L=50 overlaps 0.5 or puts the crossing in a
   predeclared 25-75 window.
4. Estimate the ranked curve on fresh confirmatory instances.

Payroll already justifies a universal L=25 rung, so no config-specific
selection is needed there. If placement data are reused in the final estimate,
the bootstrap must replay the adaptive rule; conditioning on the selected
support is not enough.

### 13. v1 instances versus attempts

**Verdict: change.**

Choose **6 instances x 6 attempts** as the minimum v1 design. Reject 9 x 4 for
CH6: it can estimate an H4 score, but that is a different metric and cannot be
placed on the CH6 leaderboard without a prior-dependent model.

Six instances will improve stability but will not reliably separate 20-30
event gaps. The present GPT-5.5-over-Sol bootstrap probability is 0.623,
equivalent to only about \(z=0.31\). Under the optimistic assumption that
uncertainty falls as \(1/\sqrt{m}\), moving from three to six instances raises
the correct-order probability only to roughly 0.67, nowhere near a
confirmatory threshold. For a true 30-event gap, the same rough calculation
needs about 10, 22, and 37 instances per rung for 0.80, 0.90, and 0.95
correct-order probability respectively; nonlinear crossings and censoring
make those figures optimistic.

Use the same seed instances for every model and paired inference. Start at
6 x 6, add six-attempt instances only under a predeclared sequential precision
rule at the bracketing cells, and publish tied tiers unless the separation
criterion is met.

### 14. Standing matched-context control

**Verdict: agree.**

Add it as a standing diagnostic, not a score component. Mechanism
heterogeneity is now an empirical result, so omitting the control for future
models would make the causal interpretation depend on which model happened to
receive the arm.

A bounded design is six shared instances, two attempts in each added condition
(standalone prefix and full-context/process-prefix), across two fixed anchor
families, reusing main-run survival. That is 48 extra calls per model. Report
paired classifications such as context-linked, workload-linked, or no detected
contrast. Complete DeepSeek's missing control.

### 15. Abstract

**Verdict: change.**

At roughly 407 words, the abstract is too dense for a first read. It asks the
reader to retain two horizons, four findings, several ratios, three
model-specific mechanisms, a null model, and the dice/trap taxonomy.

Cut anticipatory rationing as a named abstract finding; it is the most
mechanism-dependent and least necessary to understand the benchmark. Preserve
only one sentence:

> Matched controls show that long-run degradation can be workload-linked,
> input-length-linked, or absent, so CH6 is an operational rather than
> mechanistic score.

Keep the consistency gap and a one-sentence trap/slip result because they
directly justify repeated measurement. Target 200-250 words. Also replace the
unsupported "two orders of magnitude" claim: the released 50-400 ladder
establishes "from below 50 to beyond 400 events," not a measured 100-fold
range.

### 16. ObviousBench citation

**Verdict: change.**

The lack of an arXiv preprint is not a material weakness if ObviousBench is
cited as software/data provenance rather than scientific support. The current
citation is mutable and over-explains its non-archival status. Archive a
versioned release, preferably with a DOI, and cite that release or an immutable
commit. Remove ObviousBench as support for the pass^k method; ClerkBench's
estimator and CH6 rationale must stand on their own. Mention the sibling only
where the shared release policy is relevant.

There is also a live metadata mismatch to resolve before using "archived
release" language: the official
[CITATION.cff](https://github.com/adamallcock/obviousbench/blob/main/CITATION.cff)
declares v0.2.0 and asks users to cite an archived release, while the official
[tags page](https://github.com/adamallcock/obviousbench/tags) does not expose a
matching v0.2.0 tag as of 2026-07-27.

### 17. Withheld generators and reproducibility

**Verdict: needs work.**

The release supports some numeric regeneration, not independent experimental
reproduction. The public scorer self-test passes all 16 demo instances, but
scored prompts, expected artifacts, outputs, manifests, and generators are not
released, and the public bundle omits analysis scripts that the paper says are
released.

More urgently, the current `per_instance_counts.csv` is stale. A fresh
comparison against the canonical loader found 783 current ladder records
versus 429 released records: 364 current records are missing, 10 stale records
are extra, and 44 overlapping records have different counts. Most of direct
Opus-high is absent, and several Gemini and Fable rows predate the current
cap-exclusion doctrine. The released aggregates are therefore not presently
self-sufficient.

The strongest addition is an immutable **frozen-v0 evidence capsule**:
scored task records and gold artifacts, raw outputs and usage, manifests,
adjudication overlays, analysis scripts, environment lock, and checksums, with
a one-command rebuild. Retire those exact v0 instances from future headline
evaluation and use fresh v1 seeds. Generators can remain private or escrowed,
but the paper should say "aggregate arithmetic regeneration" rather than
"experimental reproducibility" until the capsule exists.

### 18. Cost per correct artifact

**Verdict: change.**

Keep L=100 as a fixed reference and keep undiscounted list prices. Change the
aggregation and the label. The current pooled ratio estimates total campaign
dollars per observed success. It does not generally estimate the expected cost
of retrying a particular artifact, because
\(E[c_i]/E[p_i] \neq E[c_i/p_i]\) when instance and family difficulty vary.
That distinction matters most in a benchmark whose central result is stable
instance-level blind spots.

At minimum, publish family-specific values and macro-average them. The current
pooled versus family-macro figures are:

- GPT-5.5: $0.386 versus $0.386;
- Sol: $0.340 versus $0.364;
- direct Opus: $0.576 versus $0.583; and
- Fable: $0.877 versus $1.306, a 49% understatement from pooling.

For the claimed retry interpretation, specify a retry policy and estimate
per-instance delivery probability and spend with a beta-binomial model or
bounded-retry sensitivity; report uncertainty. Otherwise rename the current
quantity "observed list-price dollars per successful L=100 output."

Also remove or rename generated Table 2's different meter-only,
horizon-normalized formula, which currently carries the same label but
produces different values. Delete the statement that CH6<100 models cannot
produce a reference artifact "at any price"; they can succeed with retries,
just not meet the stated repeat-reliability threshold.

### 19. Strongest unasked criticism

**Verdict: needs work.**

The strongest missing criticism is that workload length jointly increases:

1. state transitions and arithmetic;
2. input length; and
3. exact output bytes and rows.

The matched-context arm isolates some input-length effects, but nothing
separates clerical computation from artifact emission. With any nonzero
serialization or transcription hazard, byte-exact success must fall as the
artifact grows even for a perfect calculator. CH6 may therefore be partly a
generic **artifact-emission horizon**, and "workload-linked" does not yet mean
"computation-linked."

I would reject the causal/mechanistic interpretation without either a control
or a narrower claim. Add:

- an emission-only control that supplies correct per-event values and requires
  an identical-length artifact; and
- a compressed-output control that requires the full computation but only a
  fixed-size final/checkpoint summary.

Without those controls, explicitly frame CH6 as an end-to-end operational
artifact horizon.

### 20. One additional experiment for $200

**Verdict: needs work.**

Commission a matched **compute x emission control**, because it addresses the
most general unidentified mechanism rather than one model's ranking.

Use GPT-5.5 and Gemini 3.1 Pro, meter and ledger at L=400, three shared seeds,
and six paired attempts in three arms:

1. normal computation and full artifact;
2. normal computation and fixed-size summary; and
3. supplied correct event values and full artifact transcription.

That is 216 calls for a fresh three-arm block; probe the largest/most expensive
cell first and stop or reduce to one family if the paid-cost projection exceeds
$200. The paired contrasts identify output-emission cost
(full versus compressed output) and computation cost (normal versus supplied
values) while controlling input and artifact format. This resolves a
paper-wide construct question that another modest rank-expansion wave cannot;
the power sketch indicates $200 is unlikely to establish adjacent rank order.

## Additional Release-Integrity Findings

These were not among the 20 judgment calls and should be treated as
pre-submission blockers:

- `per_instance_counts.csv` is a July 12-era artifact and does not reproduce
  the current July 26-27 score pipeline.
- The generated cap note and the builder implement contradictory scoring
  rules.
- The paper's "two orders of magnitude" claim is unsupported by the released
  50-400 scored ladder.
- The bibliography still renders placeholder corporate/key authors such as
  "Beyond pass at 1," "Beta-binomial pass at k," and "ReliabilityBench";
  `references.bib` also contains an explicit "exact citation to be resolved
  before submission" note. The bibliography checker did not catch this.
- The release README and paper say analysis/runner surfaces are released that
  are not present in the public bundle.

## Ranked Pre-Ship Actions

1. **Freeze and audit one canonical attempt manifest.** Implement the
   availability partition, remove the n=5 promotion, replace missing protocol
   slots, resolve duplicate lineage, and regenerate every aggregate from that
   manifest.
2. **Repair the public evidence surface.** Regenerate
   `per_instance_counts.csv`, resolve cap-note and cost-table contradictions,
   ship the frozen-v0 evidence capsule, and run a byte-level release audit.
3. **Align the estimand and leaderboard.** Call CH6 a served-configuration
   operational horizon, score Fable consistently, use partial ranks for
   overlapping bounds, and separate availability from conditional execution.
4. **Lock the v1 statistical design.** Use shared 6 x 6 cells, paired
   inference, universal lower payroll support, predeclared adaptive refinement,
   empirical-sensitivity intervals, and tied rank tiers.
5. **Close the paper's claim surface.** Run the compute/emission control or
   narrow the mechanism claims; then cut the abstract, fix the unsupported
   range statement, archive the ObviousBench citation, and replace all
   placeholder bibliography entries.
