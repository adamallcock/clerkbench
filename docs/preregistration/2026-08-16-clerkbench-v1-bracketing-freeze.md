# ClerkBench v1 — Stage-2 bracketing freeze (founding families)

Pre-registration "commit before spend" artifact (preregistration §2.3). The
two crossing-bracketing rungs per (config, family) are identified from the
frozen Stage-1 3×6 data by the pre-declared rule below, BEFORE any 6-instance
top-up. Computed from the canonical board (`pass1_by_length.csv`, post
DeepSeek-v0 purge + budget-cap exclusion) via `build_report_tables.crossing()`.

**NOTE (2026-08-16):** the 5.5/Sol brackets below use the re-collected v1 data
(on the frozen tasks), not the invalid v0 reuse. This moved both configs
materially: 5.5 meter crossing >400 → 264, Sol meter >400 → 328 (their v0
L400 was ~0.6–0.9; on the frozen tasks it is ~0.17–0.39). Opus 5.0 is now the
only config censored >400 on both families.

## Pre-declared rule

For each (config, family), the **bracketing rungs** are the adjacent ladder
rung pair (L₁, L₂) with strict pass@1 ≥ 0.5 at L₁ and < 0.5 at L₂ (the first
downward crossing of 0.5). If pass@1 < 0.5 at the smallest rung (L=50) the
config is **censored low** (`<50`); if ≥ 0.5 at the largest in-range rung
(L=400) it is **censored high** (`>400`). Censored configs get NO in-range
top-up (a low-censored config would need L=25; a high-censored one L=800, which
is excluded as width-confounded). Budget-unmeasurable cells (Gemini-high L200+)
do not receive top-ups — more attempts would only produce more capped rows.

## Frozen brackets

| Config | Family | pass@1 (50/100/200/400) | crossing | bracket | Stage-2 |
|---|---|---|---|---|---|
| Opus-5.0/high | meter | 0.67 0.94 0.78 0.72 | >400 | — | censored high |
| Opus-5.0/high | ledger | 0.94 1.00 0.67 0.72 | >400 | — | censored high |
| GPT-5.5/high | meter | 0.94 0.94 0.72 0.17 | 264 | {200,400} | top-up 3→6 |
| GPT-5.5/high | ledger | 1.00 0.89 0.67 0.17 | 252 | {200,400} | top-up 3→6 |
| Sol/high | meter | 0.89 1.00 0.78 0.39 | 328 | {200,400} | top-up 3→6 |
| Sol/high | ledger | 1.00 0.72 0.22 0.06 | 136 | {100,200} | top-up 3→6 |
| Terra/high | meter | 0.46 0.29 0.04 0.00 | <50 | — | censored low |
| Terra/high | ledger | 0.67 0.17 0.00 0.00 | 63 | {50,100} | top-up 3→6 |
| Luna/high | meter | 0.25 0.04 0.00 0.00 | <50 | — | censored low |
| Luna/high | ledger | 0.29 0.25 0.00 0.00 | <50 | — | censored low |
| DS-Pro/default | meter | 1.00 0.83 0.78 0.33 | 308 | {200,400} | top-up 3→6 |
| DS-Pro/default | ledger | 1.00 0.89 0.39 0.06 | 171 | {100,200} | top-up 3→6 |
| DS-Flash/default | meter | 0.72 0.72 0.44 0.11 | 174 | {100,200} | already 6×6 |
| DS-Flash/default | ledger | 1.00 0.86 0.67 0.06 | 242 | {200,400} | already 6×6 |
| Gemini-med | meter | 0.94 0.94 0.22 0.00 | 153 | {100,200} | top-up 3→6 |
| Gemini-med | ledger | 1.00 0.67 0.44 0.00 | 168 | {100,200} | top-up 3→6 |
| Gemini-high | meter | 1.00 0.83 (cap) (cap) | — | — | unmeasurable ≥L200 (censored) |
| Gemini-high | ledger | 1.00 0.94 (cap) (cap) | — | — | unmeasurable ≥L200 (censored) |

## Stage-2a top-up plan (founding families — no `event_trace` needed)

Add instances 000004–000006 (from the frozen 6-instance seed set, a superset of
the 3-instance set) × 6 attempts at each **top-up** bracket above. Shared seeds
preserved. Cells:

- GPT-5.5/high ledger {200,400}; Sol/high ledger {100,200}; Terra/high ledger
  {50,100}; DS-Pro/default meter {200,400} + ledger {100,200}; Gemini-med
  meter {100,200} + ledger {100,200}.
- Total ≈ 8 (config,family) × 2 rungs × 3 inst × 6 att ≈ 288 attempts. DS-Flash
  already 6×6; Gemini-high and all censored cells excluded.

## Stage-2b (separate — payroll L25 universal + gateway)

Requires the per-event `event_trace.tsv` instrumentation (preregistration §2.2)
and is NEW-instance collection (v0 payroll/gateway cannot be reused). Tracked
separately from the founding-family board; gates the four-family CH6.
