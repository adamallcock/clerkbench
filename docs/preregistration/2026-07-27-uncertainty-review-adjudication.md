# Adjudication of the external uncertainty review (2026-07-27)

Verdict quality: highest of the three reviews. Every factual claim we
could check against the repo verified (bib placeholder note; dual
cost formulas under one label; stale caps-count-as-failures line in
released tables.md; the n=5 all-correct fallback promoted to
protocol-6; release per-instance CSV at exactly their counted 527
four-family rows vs 783 canonical). Adam's rule for this phase: no
significant spend until jointly reviewed. Buckets below.

## Bucket 1 — objectively broken; fix on Adam's word (zero cost, zero controversy)
- references.bib "exact citation to be resolved before submission"
  note (line ~127) → resolve the citation; extend the claims gate to
  scan bib notes.
- Released tables.md legacy preamble line contradicting the
  availability doctrine → regenerate.
- Cost label collision: Table 2 "Est. $ per reliable" vs Table 4
  "$ / correct ... incl. retries" are different formulas → rename per
  ruling 18 pending the metric decision.
- Release per-instance_counts.csv stale (527 vs 783 rows) →
  regenerate; fold into the evidence-capsule work (ruling 17).
- Wording fixes: "single run stops being trustworthy" (pass^6=0.5 is
  per-attempt 0.891, not 0.5); "0.46" described as agreement not
  p-value; DeepSeek "mechanism unclassified"; "cannot have leaked" →
  "unlikely to have appeared verbatim"; remove the "at any price"
  cost claim.

## Bucket 2 — accept, implement free (analysis/prose, no API spend)
- R1 served-configuration framing sentence; R2 leave-payroll-out
  sensitivity (analysis only); R5 bootstrap caveat wording + LOSO +
  beta-binomial secondary + joint-seed resampling; R7 crossing-
  convention sensitivity appendix (isotonic comparison; Opus 59→~61,
  order unchanged); R8 multiplicity-families statement; R10 post-data
  decision disclosure sentence; R15 abstract cut (rationing out of
  the abstract; 250-300 words) — flag to Adam as editorial taste;
  R18 metric relabel + primary-cost-axis switch (regeneration).

## Bucket 3 — accept in principle; v1 protocol design (writes docs now, spends later)
- R3 service-envelope doctrine (valid-outcome vs invalid-experiment
  partition; slot replacement; completion-conditional secondary
  estimand).
- R6 kill 5-as-6; require six valid outcomes (9 instance slots need
  replacement attempts — small spend, deferred).
- R9 slot/UUID/lineage protocol for v1; their audit: 90 dup keys, 91
  extra rows, 24 disagreeing groups; counting-all does not change the
  current board (reassuring).
- R11 uniform semantic serving policy (native route, provider-default
  sampling, non-binding budgets, fixed retry/deadline, pinned tier).
- R12 universal L=25 rung (supersedes our selective rule).
- R13 v1 cells at 6x6 minimum, shared seeds, paired inference,
  sequential instance addition, tied tiers when unmet. NOTE: this
  roughly doubles the +4 campaign; new planning envelope ~$550-800
  all-in (was $215-375) including R14 sentinel controls and R20.
- R14 bounded matched-context sentinel arm per model (24 calls/model).

## Bucket 4 — decisions Adam owns
- R4 Fable back on the ranked board, availability-inclusive with a
  partial rank ~4-6 and completion-conditional beside it; drop the
  "refusal-censored" term (they are observed failures, not missing
  data). My recommendation: ACCEPT — it is more consistent with our
  own doctrine than unranking was; reverses an earlier call of yours,
  hence your decision.
- R15 abstract: cut anticipatory rationing as a named finding. My
  recommendation: ACCEPT (voice guide bias-to-cut; it is the most
  conditional finding), keep it prominent in §6.
- R16 ObviousBench: create the versioned GitHub release + tag that
  CITATION.cff already promises, archive with a DOI (Zenodo key is in
  the keychain), cite the immutable artifact. Adam action.
- R17 frozen retired-v0 evidence capsule (scored tasks, golds, raw
  outputs, scores, usage, manifests, scripts, hashes, one-command
  rebuild; generators and v1 seeds stay private). My recommendation:
  ACCEPT — v0 seeds retire at v1 anyway; this makes the
  reproducibility story genuinely strong. Policy call is yours.
- R19/R20 compute-vs-emission control ($200 cap, 216-324 calls,
  probe-first): the strongest new criticism; without it the causal
  language narrows to "artifact-delivery horizon". My recommendation:
  RUN IT before v1 ships; it is the one experiment that changes what
  the paper is allowed to claim. Awaiting your go (spend).

## Not accepted as-is (nuances to raise in review)
- R13's ordering-probability targets (0.90 at 23-52 instances) would
  price rank-separation beyond any sane budget; propose shipping v1
  at 6x6 with tied-tier presentation and treating >=0.80 separation
  as aspirational, per their own "publish tied tiers" clause.
- R7 pre-registered isotonic estimator for v1: accept, but keep the
  first-bracket convention for v0 continuity with the sensitivity
  appendix, rather than re-estimating v0 numbers.
