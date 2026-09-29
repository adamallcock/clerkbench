# ClerkBench generated tables

Source rows: 7676 ladder attempts across 47 configs. Regenerate: `uv run python scripts/research/build_report_tables.py`

## Table 1 — pass@1 by length (attempts; Wilson CIs in CSV)

*Attempts that stop at an output limit are excluded from these cells as unmeasurable, never scored as zeros. The pipeline cannot yet separate a harness cap from a provider maximum; provider-max stops are scored as availability failures with an annotation once it can. †n counts any limit-stopped attempt that survived the exclusion — a pipeline sentinel that should read zero. Refusals are scored as failed artifacts. Per-cell mechanism counts ship in `failure_decomposition.csv` and `refusal_counts.csv`.* *No L=800 cell was collected in this campaign; the rung is excluded from crossing estimates because it mixes length with state width. Entity-pool sizes per family and rung are in the paper's pool-schedule table. In-flight runs appear as partial attempt counts.*

### banded_meter_billing

| Config | L=50 | L=100 | L=200 | L=400 | L=800 | 50% crossing |
|---|---|---|---|---|---|---|
| 5.4-mini/none | 0/6 (0.00) | 0/6 (0.00) | 0/6 (0.00) | 0/6 (0.00) | — | <50 |
| 5.4-nano/none | 0/6 (0.00) | 0/6 (0.00) | 0/6 (0.00) | 0/6 (0.00) | — | <50 |
| gemma-4-26b-a4b-it/none | 0/6 (0.00) | — | — | — | — | <50 |
| gemma-4-31b-it/none | 0/6 (0.00) | — | — | — | — | <50 |
| openrouter/qwen/qwen3.6-35b-a3b/none | 0/6 (0.00) | — | — | — | — | <50 |
| anthropic/opus-4-8/low | 5/6 (0.83) | 5/6 (0.83) | 1/6 (0.17) | 0/6 (0.00) | — | 141 |
| opus-4.8/low | 1/1 (1.00) | — | — | — | — | >50 |
| gemini/gemini-3-flash-preview/medium | 5/6 (0.83) | 0/6 (0.00) | — | — | — | 66 |
| gemini/gemini-3.1-flash-lite/medium | 0/6 (0.00) | — | — | — | — | <50 |
| gemini/gemini-3.7-flash/medium | 17/18 (0.94) | 27/36 (0.75) | 6/36 (0.17) | 0/18 (0.00) | — | 135 |
| gpt-5-mini/medium | 2/6 (0.33) | 0/6 (0.00) | — | — | — | <50 |
| gpt-5-nano/medium | 0/6 (0.00) | — | — | — | — | <50 |
| 5.4-mini/medium | 1/6 (0.17) | 0/6 (0.00) | 0/6 (0.00) | 0/6 (0.00) | — | <50 |
| 5.4-nano/medium | 3/6 (0.50) | 2/6 (0.33) | 0/6 (0.00) | 0/6 (0.00) | — | 50 |
| gpt-5.6-sol/medium | 5/6 (0.83) | 6/6 (1.00) | 2/6 (0.33) | 0/6 (0.00) | — | 164 |
| openrouter/openai/gpt-oss-120b/medium | 0/18 (0.00) | — | — | — | — | <50 |
| openrouter/openai/gpt-oss-20b/medium | 0/6 (0.00) | — | — | — | — | <50 |
| openrouter/tencent/hy3/medium | 4/6 (0.67) | 0/6 (0.00) | — | — | — | 59 |
| anthropic/fable-5/high | 6/18 (0.33) | 5/18 (0.28) | 4/18 (0.22) | 10/23 (0.43) | — | <50 |
| anthropic/opus-4-8/high | 17/18 (0.94) | 15/18 (0.83) | 14/18 (0.78) | 8/18 (0.44) | — | 356 |
| anthropic/opus-5/high | 26/36 (0.72) | 33/36 (0.92) | 14/18 (0.78) | 13/18 (0.72) | — | >400 |
| anthropic/opus-5-5/high | 18/18 (1.00) | 18/18 (1.00) | 34/36 (0.94) | 29/36 (0.81) | — | >400 |
| gemini/gemini-3.1-pro-preview/high | 16/18 (0.89) | 16/18 (0.89) | 9/18 (0.50) | 11/21 (0.52) | — | >400 |
| gemini/gemini-3.5-flash/high | 8/18 (0.44) | 7/18 (0.39) | 1/8 (0.12) †1 | — | — | <50 |
| gemini/gemini-3.7-flash/high | 18/18 (1.00) | 15/18 (0.83) | 5/9 (0.56) †8 | 3/9 (0.33) †8 | — | 238 |
| gpt-5.5/high | 17/18 (0.94) | 35/36 (0.97) | 23/36 (0.64) | 5/36 (0.14) | — | 242 |
| gpt-5.6-luna/high | 4/18 (0.22) | 1/18 (0.06) | 0/18 (0.00) | 0/18 (0.00) | — | <50 |
| gpt-5.6-sol/high | 16/18 (0.89) | 36/36 (1.00) | 29/36 (0.81) | 9/36 (0.25) | — | 293 |
| gpt-5.6-terra/high | 7/18 (0.39) | 5/18 (0.28) | 0/18 (0.00) | 0/18 (0.00) | — | <50 |
| gpt-6-astra/high | 18/18 (1.00) | 18/18 (1.00) | 36/36 (1.00) | 34/36 (0.94) | — | >400 |
| gpt-6-luna/high | 1/18 (0.06) | 0/18 (0.00) | 0/18 (0.00) | 0/18 (0.00) | — | <50 |
| gpt-6-sol/high | 17/18 (0.94) | 32/36 (0.89) | 26/36 (0.72) | 3/36 (0.08) | — | 255 |
| fable-5/high | 0/1 (0.00) | — | — | — | — | <50 |
| opus-4.7/high | 1/1 (1.00) | — | — | — | — | >50 |
| opus-4.8/high | 17/18 (0.94) | 10/18 (0.56) | 10/18 (0.56) | 10/19 (0.53) | — | >400 |
| gemini-3.5-flash/high | 1/1 (1.00) | — | — | — | — | >50 |
| anthropic/fable-5/high+fallback | 15/18 (0.83) | 15/18 (0.83) | 9/18 (0.50) | 9/17 (0.53) | — | >400 |
| 5.4-mini/xhigh | 4/6 (0.67) | 3/6 (0.50) | 0/6 (0.00) | 0/5 (0.00) | — | 100 |
| 5.4-nano/xhigh | 49/60 (0.82) | 47/60 (0.78) | — | — | — | >100 |
| deepseek/deepseek-flash/default | 17/18 (0.94) | 33/36 (0.92) | 28/36 (0.78) | 14/36 (0.39) | — | 328 |
| deepseek/deepseek-v4-flash/default | 26/36 (0.72) | 31/36 (0.86) | 18/36 (0.50) | 3/36 (0.08) | — | 200 |
| deepseek/deepseek-v4-pro/default | 36/36 (1.00) | 31/36 (0.86) | 32/36 (0.89) | 10/36 (0.28) | — | 309 |
| openrouter/deepseek/deepseek-v4-flash/T0 | — | — | — | — | — | — |
| openrouter/deepseek/deepseek-v4-flash/T0.6 | 1/2 (0.50) | — | — | — | — | >50 |
| openrouter/qwen/qwen3.6-27b/T0.6 | 1/1 (1.00) | 0/1 (0.00) | — | — | — | 71 |
| openrouter/qwen/qwen3.6-27b/T0.9 | — | 0/1 (0.00) | — | — | — | <100 |
| openrouter/qwen/qwen3.6-35b-a3b/T0.6 | 0/2 (0.00) | — | — | — | — | <50 |

### fee_ledger_dropzero

| Config | L=50 | L=100 | L=200 | L=400 | L=800 | 50% crossing |
|---|---|---|---|---|---|---|
| 5.4-mini/none | 0/6 (0.00) | 0/6 (0.00) | 0/6 (0.00) | 0/6 (0.00) | — | <50 |
| 5.4-nano/none | 0/6 (0.00) | 0/6 (0.00) | 0/6 (0.00) | 0/6 (0.00) | — | <50 |
| gemma-4-26b-a4b-it/none | 0/6 (0.00) | — | — | — | — | <50 |
| gemma-4-31b-it/none | 0/6 (0.00) | — | — | — | — | <50 |
| openrouter/qwen/qwen3.6-35b-a3b/none | 0/6 (0.00) | — | — | — | — | <50 |
| anthropic/opus-4-8/low | 2/6 (0.33) | 4/6 (0.67) | 1/6 (0.17) | 0/18 (0.00) | — | 100 |
| opus-4.8/low | — | — | — | — | — | — |
| gemini/gemini-3-flash-preview/medium | 5/6 (0.83) | 0/6 (0.00) | — | — | — | 66 |
| gemini/gemini-3.1-flash-lite/medium | 0/6 (0.00) | — | — | — | — | <50 |
| gemini/gemini-3.7-flash/medium | 36/36 (1.00) | 29/36 (0.81) | 13/36 (0.36) | 0/18 (0.00) | — | 161 |
| gpt-5-mini/medium | 1/6 (0.17) | 0/6 (0.00) | — | — | — | <50 |
| gpt-5-nano/medium | 0/6 (0.00) | — | — | — | — | <50 |
| 5.4-mini/medium | 0/6 (0.00) | 0/6 (0.00) | 0/6 (0.00) | 0/6 (0.00) | — | <50 |
| 5.4-nano/medium | 2/6 (0.33) | 0/6 (0.00) | 0/6 (0.00) | 0/6 (0.00) | — | <50 |
| gpt-5.6-sol/medium | 5/6 (0.83) | 2/6 (0.33) | 0/6 (0.00) | 0/6 (0.00) | — | 79 |
| openrouter/openai/gpt-oss-120b/medium | 0/18 (0.00) | — | — | — | — | <50 |
| openrouter/openai/gpt-oss-20b/medium | 0/6 (0.00) | — | — | — | — | <50 |
| openrouter/tencent/hy3/medium | 0/6 (0.00) | — | — | — | — | <50 |
| anthropic/fable-5/high | 14/18 (0.78) | 18/18 (1.00) | 14/18 (0.78) | 24/28 (0.86) | — | >400 |
| anthropic/opus-4-8/high | 17/18 (0.94) | 12/18 (0.67) | 4/18 (0.22) | 2/23 (0.09) | — | 130 |
| anthropic/opus-5/high | 17/18 (0.94) | 33/36 (0.92) | 29/36 (0.81) | 21/36 (0.58) | — | >400 |
| anthropic/opus-5-5/high | 18/18 (1.00) | 17/18 (0.94) | 17/18 (0.94) | 16/18 (0.89) | — | >400 |
| gemini/gemini-3.1-pro-preview/high | 18/18 (1.00) | 18/18 (1.00) | 10/18 (0.56) | 0/22 (0.00) | — | 214 |
| gemini/gemini-3.5-flash/high | 15/18 (0.83) | 12/18 (0.67) | 2/14 (0.14) | — | — | 125 |
| gemini/gemini-3.7-flash/high | 18/18 (1.00) | 17/18 (0.94) | 8/11 (0.73) †4 | 0/9 (0.00) †6 | — | 248 |
| gpt-5.5/high | 18/18 (1.00) | 34/36 (0.94) | 26/36 (0.72) | 9/36 (0.25) | — | 277 |
| gpt-5.6-luna/high | 6/18 (0.33) | 6/18 (0.33) | 0/18 (0.00) | 0/18 (0.00) | — | <50 |
| gpt-5.6-sol/high | 31/36 (0.86) | 22/36 (0.61) | 12/36 (0.33) | 1/18 (0.06) | — | 132 |
| gpt-5.6-terra/high | 23/36 (0.64) | 8/36 (0.22) | 0/18 (0.00) | 0/18 (0.00) | — | 63 |
| gpt-6-astra/high | 18/18 (1.00) | 18/18 (1.00) | 18/18 (1.00) | 18/18 (1.00) | — | >400 |
| gpt-6-luna/high | 13/36 (0.36) | 2/36 (0.06) | 0/18 (0.00) | 0/18 (0.00) | — | <50 |
| gpt-6-sol/high | 30/36 (0.83) | 13/36 (0.36) | 8/36 (0.22) | 1/18 (0.06) | — | 82 |
| fable-5/high | — | — | — | — | — | — |
| opus-4.7/high | — | — | — | — | — | — |
| opus-4.8/high | 17/18 (0.94) | 13/18 (0.72) | 7/18 (0.39) | — | — | 159 |
| gemini-3.5-flash/high | — | — | — | — | — | — |
| anthropic/fable-5/high+fallback | 10/18 (0.56) | 18/18 (1.00) | 16/18 (0.89) | 15/18 (0.83) | — | >400 |
| 5.4-mini/xhigh | 4/6 (0.67) | 4/6 (0.67) | 0/3 (0.00) | 0/1 (0.00) | — | 119 |
| 5.4-nano/xhigh | 40/60 (0.67) | 49/60 (0.82) | — | — | — | >100 |
| deepseek/deepseek-flash/default | 17/18 (0.94) | 35/36 (0.97) | 26/36 (0.72) | 9/36 (0.25) | — | 277 |
| deepseek/deepseek-v4-flash/default | 36/36 (1.00) | 34/36 (0.94) | 22/36 (0.61) | 2/36 (0.06) | — | 230 |
| deepseek/deepseek-v4-pro/default | 35/36 (0.97) | 30/36 (0.83) | 20/36 (0.56) | 1/18 (0.06) | — | 216 |
| openrouter/deepseek/deepseek-v4-flash/T0 | — | 0/1 (0.00) | — | — | — | <100 |
| openrouter/deepseek/deepseek-v4-flash/T0.6 | 0/3 (0.00) | 0/1 (0.00) | — | — | — | <50 |
| openrouter/qwen/qwen3.6-27b/T0.6 | 0/1 (0.00) | 0/1 (0.00) | — | — | — | <50 |
| openrouter/qwen/qwen3.6-27b/T0.9 | — | 0/1 (0.00) | — | — | — | <100 |
| openrouter/qwen/qwen3.6-35b-a3b/T0.6 | 0/1 (0.00) | — | — | — | — | <50 |

### payroll_overtime_ledger

| Config | L=50 | L=100 | L=200 | L=400 | L=800 | 50% crossing |
|---|---|---|---|---|---|---|
| 5.4-mini/none | — | — | — | — | — | — |
| 5.4-nano/none | — | — | — | — | — | — |
| gemma-4-26b-a4b-it/none | — | — | — | — | — | — |
| gemma-4-31b-it/none | — | — | — | — | — | — |
| openrouter/qwen/qwen3.6-35b-a3b/none | — | — | — | — | — | — |
| anthropic/opus-4-8/low | — | — | — | — | — | — |
| opus-4.8/low | — | — | — | — | — | — |
| gemini/gemini-3-flash-preview/medium | — | — | — | — | — | — |
| gemini/gemini-3.1-flash-lite/medium | — | — | — | — | — | — |
| gemini/gemini-3.7-flash/medium | 18/18 (1.00) | 14/18 (0.78) | 10/18 (0.56) | 0/18 (0.00) | — | 214 |
| gpt-5-mini/medium | — | — | — | — | — | — |
| gpt-5-nano/medium | — | — | — | — | — | — |
| 5.4-mini/medium | — | — | — | — | — | — |
| 5.4-nano/medium | 2/6 (0.33) | 1/6 (0.17) | 1/6 (0.17) | 0/6 (0.00) | — | <50 |
| gpt-5.6-sol/medium | — | — | — | — | — | — |
| openrouter/openai/gpt-oss-120b/medium | — | — | — | — | — | — |
| openrouter/openai/gpt-oss-20b/medium | — | — | — | — | — | — |
| openrouter/tencent/hy3/medium | — | — | — | — | — | — |
| anthropic/fable-5/high | — | — | — | — | — | — |
| anthropic/opus-4-8/high | — | — | — | — | — | — |
| anthropic/opus-5/high | 18/18 (1.00) | 15/18 (0.83) | 17/18 (0.94) | 7/18 (0.39) | — | 343 |
| anthropic/opus-5-5/high | 16/18 (0.89) | 18/18 (1.00) | 16/18 (0.89) | 14/18 (0.78) | — | >400 |
| gemini/gemini-3.1-pro-preview/high | — | — | — | — | — | — |
| gemini/gemini-3.5-flash/high | — | — | — | — | — | — |
| gemini/gemini-3.7-flash/high | 17/18 (0.94) | 18/18 (1.00) | 5/10 (0.50) †5 | 4/11 (0.36) †10 | — | 200 |
| gpt-5.5/high | 18/18 (1.00) | 14/18 (0.78) | 13/18 (0.72) | 6/18 (0.33) | — | 297 |
| gpt-5.6-luna/high | 9/18 (0.50) | 3/18 (0.17) | 0/18 (0.00) | 0/18 (0.00) | — | 50 |
| gpt-5.6-sol/high | 18/18 (1.00) | 18/18 (1.00) | 17/18 (0.94) | 14/18 (0.78) | — | >400 |
| gpt-5.6-terra/high | 7/18 (0.39) | 9/18 (0.50) | 0/18 (0.00) | 0/18 (0.00) | — | 45 |
| gpt-6-astra/high | 18/18 (1.00) | 18/18 (1.00) | 18/18 (1.00) | 18/18 (1.00) | — | >400 |
| gpt-6-luna/high | 9/18 (0.50) | 3/18 (0.17) | 1/18 (0.06) | 0/18 (0.00) | — | 50 |
| gpt-6-sol/high | 17/18 (0.94) | 18/18 (1.00) | 14/18 (0.78) | 9/18 (0.50) | — | >400 |
| fable-5/high | — | — | — | — | — | — |
| opus-4.7/high | — | — | — | — | — | — |
| opus-4.8/high | — | — | — | — | — | — |
| gemini-3.5-flash/high | — | — | — | — | — | — |
| anthropic/fable-5/high+fallback | — | — | — | — | — | — |
| 5.4-mini/xhigh | — | — | — | — | — | — |
| 5.4-nano/xhigh | 58/60 (0.97) | 46/58 (0.79) | — | — | — | >100 |
| deepseek/deepseek-flash/default | 17/18 (0.94) | 18/18 (1.00) | 14/18 (0.78) | 9/18 (0.50) | — | >400 |
| deepseek/deepseek-v4-flash/default | 15/18 (0.83) | 16/18 (0.89) | 6/18 (0.33) | 2/18 (0.11) | — | 161 |
| deepseek/deepseek-v4-pro/default | 18/18 (1.00) | 17/18 (0.94) | 12/18 (0.67) | 6/18 (0.33) | — | 283 |
| openrouter/deepseek/deepseek-v4-flash/T0 | — | — | — | — | — | — |
| openrouter/deepseek/deepseek-v4-flash/T0.6 | — | — | — | — | — | — |
| openrouter/qwen/qwen3.6-27b/T0.6 | — | — | — | — | — | — |
| openrouter/qwen/qwen3.6-27b/T0.9 | — | — | — | — | — | — |
| openrouter/qwen/qwen3.6-35b-a3b/T0.6 | — | — | — | — | — | — |

### spent_tracking_gateway

| Config | L=50 | L=100 | L=200 | L=400 | L=800 | 50% crossing |
|---|---|---|---|---|---|---|
| 5.4-mini/none | 0/6 (0.00) | — | — | — | — | <50 |
| 5.4-nano/none | 0/6 (0.00) | — | — | — | — | <50 |
| gemma-4-26b-a4b-it/none | — | — | — | — | — | — |
| gemma-4-31b-it/none | — | — | — | — | — | — |
| openrouter/qwen/qwen3.6-35b-a3b/none | — | — | — | — | — | — |
| anthropic/opus-4-8/low | 2/6 (0.33) | 2/6 (0.33) | 0/6 (0.00) | — | — | <50 |
| opus-4.8/low | — | — | — | — | — | — |
| gemini/gemini-3-flash-preview/medium | 6/6 (1.00) | 4/6 (0.67) | 0/6 (0.00) | — | — | 119 |
| gemini/gemini-3.1-flash-lite/medium | — | — | — | — | — | — |
| gemini/gemini-3.7-flash/medium | 18/18 (1.00) | 17/18 (0.94) | 12/18 (0.67) | 5/18 (0.28) | — | 269 |
| gpt-5-mini/medium | 6/6 (1.00) | 2/6 (0.33) | 1/6 (0.17) | 0/6 (0.00) | — | 84 |
| gpt-5-nano/medium | — | — | — | — | — | — |
| 5.4-mini/medium | 0/6 (0.00) | — | — | — | — | <50 |
| 5.4-nano/medium | 6/6 (1.00) | 2/6 (0.33) | 0/6 (0.00) | — | — | 84 |
| gpt-5.6-sol/medium | 4/6 (0.67) | 4/6 (0.67) | 2/6 (0.33) | 0/6 (0.00) | — | 141 |
| openrouter/openai/gpt-oss-120b/medium | — | — | — | — | — | — |
| openrouter/openai/gpt-oss-20b/medium | — | — | — | — | — | — |
| openrouter/tencent/hy3/medium | 4/6 (0.67) | 1/6 (0.17) | 0/6 (0.00) | — | — | 63 |
| anthropic/fable-5/high | 0/6 (0.00) | — | — | — | — | <50 |
| anthropic/opus-4-8/high | — | — | — | 4/18 (0.22) | — | <400 |
| anthropic/opus-5/high | 18/18 (1.00) | 0/18 (0.00) | 5/18 (0.28) | 4/18 (0.22) | — | 76 |
| anthropic/opus-5-5/high | 11/18 (0.61) | 8/18 (0.44) | 3/18 (0.17) | 2/18 (0.11) | — | 79 |
| gemini/gemini-3.1-pro-preview/high | 6/6 (1.00) | 5/6 (0.83) | 3/6 (0.50) | 0/6 (0.00) | — | 200 |
| gemini/gemini-3.5-flash/high | 5/6 (0.83) | 2/6 (0.33) | 1/10 (0.10) | — | — | 79 |
| gemini/gemini-3.7-flash/high | 18/18 (1.00) | 17/18 (0.94) | 15/18 (0.83) †3 | 6/11 (0.55) †11 | — | >400 |
| gpt-5.5/high | 18/18 (1.00) | 17/18 (0.94) | 13/18 (0.72) | 7/18 (0.39) | — | 317 |
| gpt-5.6-luna/high | 5/18 (0.28) | 2/18 (0.11) | 0/18 (0.00) | 0/18 (0.00) | — | <50 |
| gpt-5.6-sol/high | 15/18 (0.83) | 14/18 (0.78) | 12/18 (0.67) | 0/18 (0.00) | — | 238 |
| gpt-5.6-terra/high | 14/18 (0.78) | 10/18 (0.56) | 0/18 (0.00) | 0/18 (0.00) | — | 107 |
| gpt-6-astra/high | 18/18 (1.00) | 18/18 (1.00) | 18/18 (1.00) | 18/18 (1.00) | — | >400 |
| gpt-6-luna/high | 5/18 (0.28) | 0/18 (0.00) | 0/18 (0.00) | 0/18 (0.00) | — | <50 |
| gpt-6-sol/high | 15/18 (0.83) | 8/18 (0.44) | 4/18 (0.22) | 1/18 (0.06) | — | 91 |
| fable-5/high | — | — | — | — | — | — |
| opus-4.7/high | — | — | — | — | — | — |
| opus-4.8/high | 5/6 (0.83) | 5/6 (0.83) | 3/6 (0.50) | 0/2 (0.00) | — | 200 |
| gemini-3.5-flash/high | — | — | — | — | — | — |
| anthropic/fable-5/high+fallback | 5/6 (0.83) | 5/6 (0.83) | 4/6 (0.67) | 1/6 (0.17) | — | 252 |
| 5.4-mini/xhigh | 5/6 (0.83) | 2/6 (0.33) | 0/6 (0.00) | — | — | 79 |
| 5.4-nano/xhigh | 59/60 (0.98) | 56/60 (0.93) | 4/6 (0.67) | 1/6 (0.17) | — | 252 |
| deepseek/deepseek-flash/default | 17/18 (0.94) | 12/18 (0.67) | 11/18 (0.61) | 1/18 (0.06) | — | 230 |
| deepseek/deepseek-v4-flash/default | 18/18 (1.00) | 16/18 (0.89) | 14/18 (0.78) | 2/18 (0.11) | — | 267 |
| deepseek/deepseek-v4-pro/default | 17/18 (0.94) | 17/18 (0.94) | 15/18 (0.83) | 10/18 (0.56) | — | >400 |
| openrouter/deepseek/deepseek-v4-flash/T0 | — | — | — | — | — | — |
| openrouter/deepseek/deepseek-v4-flash/T0.6 | — | — | — | — | — | — |
| openrouter/qwen/qwen3.6-27b/T0.6 | — | — | — | — | — | — |
| openrouter/qwen/qwen3.6-27b/T0.9 | — | — | — | — | — | — |
| openrouter/qwen/qwen3.6-35b-a3b/T0.6 | — | — | — | — | — | — |

## Table 2 — horizons and efficiency

*The cost column here is meter-family only, normalized from the rung nearest the capability horizon to 100 events, with a fixed 2x retry factor (the expected attempts at a 50% per-attempt success rate). It is a different formula from Table 4's cost columns and is not comparable with them.*

| Config | Capability horizon (meter / dropzero) | pass^k=50% length (meter / dropzero) | Tokens per reliable event | Meter-only horizon-normalized $ per 100 events (2x retry) |
|---|---|---|---|---|
| gemini/gemini-3.7-flash/medium | 135 / 161 | 100 / 84 | 280 | $0.15 |
| anthropic/opus-5/high | >400 / >400 | <50 / 200 | 230 | $0.62 |
| anthropic/opus-5-5/high | >400 / >400 | 252 / >400 | 169 | $0.38 |
| gemini/gemini-3.7-flash/high | 238 / 248 | 84 / 119 | 721 | $0.33 |
| gpt-5.5/high | 242 / 277 | 135 / 159 | 158 | $0.61 |
| gpt-5.6-luna/high | <50 / <50 | <50 / <50 | 298 | $0.04 |
| gpt-5.6-sol/high | 293 / 132 | 141 / 63 | 92 | $0.44 |
| gpt-5.6-terra/high | <50 / 63 | <50 / <50 | 154 | $0.20 |
| gpt-6-astra/high | >400 / >400 | >400 / >400 | 87 | $0.50 |
| gpt-6-luna/high | <50 / <50 | <50 / <50 | 208 | $0.01 |
| gpt-6-sol/high | 255 / 82 | 100 / 63 | 80 | $0.12 |
| deepseek/deepseek-flash/default | 328 / 277 | 126 / 152 | 406 | $0.04 |
| deepseek/deepseek-v4-flash/default | 200 / 230 | <50 / 119 | 525 | $0.07 |
| deepseek/deepseek-v4-pro/default | 309 / 216 | 84 / 79 | 435 | $0.14 |

## Table 3 — first-divergence depth, meter bills.tsv (median [min–max] per config × L)

| Config | L=50 | L=100 | L=200 | L=400 | L=800 |
|---|---|---|---|---|---|
| gemini/gemini-3.7-flash/medium | — | — | — | — | — |
| anthropic/opus-5/high | — | — | — | — | — |
| anthropic/opus-5-5/high | — | — | — | — | — |
| gemini/gemini-3.7-flash/high | — | — | — | — | — |
| gpt-5.5/high | — | — | — | — | — |
| gpt-5.6-luna/high | — | — | — | — | — |
| gpt-5.6-sol/high | — | — | — | — | — |
| gpt-5.6-terra/high | — | — | — | — | — |
| gpt-6-astra/high | — | — | — | — | — |
| gpt-6-luna/high | — | — | — | — | — |
| gpt-6-sol/high | — | — | — | — | — |
| deepseek/deepseek-flash/default | — | — | — | — | — |
| deepseek/deepseek-v4-flash/default | — | — | — | — | — |
| deepseek/deepseek-v4-pro/default | — | — | — | — | — |

## Table 4 — Leaderboard (ClerkBench-CH6, v1 roster, founding families)

Headline score: consistency horizon — the workload length (events) at which the probability of a model producing a fully correct artifact on EVERY one of 6 attempts falls to 50%; geometric mean across families, L=800 rung excluded. ≥/≤ mark scores censored at the measured range. (p) = provisional (run in flight).

Ordinal ranks go to ranked rows only. An *availability-dominated* row sits in the ranked block at its bound position and carries a partial rank (an interval) instead of an ordinal, because a ≤ bound cannot support a forced ordering — its failures are observed failures (mostly API-level refusals), not missing outcomes. `—` in the # column marks a row the leaderboard does not rank at all: *route comparison* (a second collection of a configuration already on the board, kept for the route contrast), *unranked (one slot short)* (six-attempt protocol, but at least one instance has five assessable attempts after cap/transport exclusions — replace the slot to restore the rank), and *unranked (pass^k bound)* (screening tier, k<6 attempts per instance). Every bound row bounds the horizon from above without locating it.

Cost columns (R18): the primary axis is the mean list-price cost of ONE L=100 attempt, both founding families pooled — a measured quantity. The secondary column is the oracle-verified statistical cost per success (campaign dollars per observed success at L=100); reading it as a retry price assumes a free perfect verifier that tells you which retry succeeded. It is a pooled ratio, so it understates configs with uneven family difficulty; the family macro-average ships beside it in `leaderboard.csv`.

| # | Config | ClerkBench-CH6 (events) | Capability horizon | $ / L=100 attempt | Oracle-verified $ / success |
|---|---|---|---|---|---|
| 1 | gpt-6-astra/high | ≥400 | ≥400 | $0.31 | $0.31 |
| 2 | anthropic/opus-5-5/high | ≥317 | ≥400 | $0.18 | $0.18 |
| 3 | gpt-5.5/high | 147 | 259 | $0.37 | $0.38 |
| 4 | deepseek/deepseek-flash/default | 138 | 301 | $0.03 | $0.04 |
| 5 | anthropic/opus-5/high | ≤100 | ≥400 | $0.28 | $0.31 |
| 6 | gpt-5.6-sol/high | 94 | 197 | $0.27 | $0.34 |
| 7 | gemini/gemini-3.7-flash/medium | 92 | 147 | $0.07 | $0.09 |
| 8 | deepseek/deepseek-v4-pro/default | 81 | 258 | $0.13 | $0.15 |
| 9 | gpt-6-sol/high | 79 | 145 | $0.06 | $0.10 |
| 10 | deepseek/deepseek-v4-flash/default | ≤77 | 214 | $0.06 | $0.07 |
| 11 | gpt-5.6-luna/high | ≤50 | ≤50 | $0.02 | $0.09 |
| 12 | gpt-5.6-terra/high | ≤50 | ≤56 | $0.10 | $0.40 |
| 13 | gpt-6-luna/high | ≤50 | ≤50 | $0.01 | $0.19 |
| — | gemini/gemini-3.7-flash/high | unranked (pass^1 bound ≤100) | 243 | $0.17 | $0.19 |

*Frontier eligibility: only configs whose CH6 reaches the 100-event reference workload are priced on the frontier chart. Configs below it are not comparable on price: they can still deliver the reference artifact given enough retries, they just do not hold it across six attempts at even odds, which is what the score prices. The frontier covers TESTED configs only — absent models are absent, not dominated.*

## Table 5 — Four-family leaderboard (ClerkBench-CH6-4fam v1)

CH6 computed across all four families (`banded_meter_billing`, `fee_ledger_dropzero`, `payroll_overtime_ledger`, `spent_tracking_gateway`). A config qualifies only when measured at ≥6 attempts per instance on ALL four families; two-attempt screening rows never enter a CH6 computation, so screening-tier data cannot produce a four-family score. The founding-family board in Table 4 remains the headline (three seed instances per cell, six at both rungs of every in-range CH6 bracket; per-cell depth in seed_depth.csv); this table is the four-family variant at three instances per cell on the newer families.

*≥/≤ mark censored crossings and ~ marks mixed censoring across families.*

| Config | ClerkBench-CH6-4fam (events) |
|---|---|
| gpt-6-astra/high | ≥400 |
| anthropic/opus-5-5/high | ~167 |
| gpt-5.5/high | 157 |
| deepseek/deepseek-flash/default | 116 |
| anthropic/opus-5/high | ≤114 |
| gpt-5.6-sol/high | 112 |
| gemini/gemini-3.7-flash/medium | 100 |
| deepseek/deepseek-v4-pro/default | 98 |
| gpt-6-sol/high | ≤84 |
| deepseek/deepseek-v4-flash/default | ≤74 |
| gpt-5.6-luna/high | ≤42 |
| gpt-5.6-terra/high | ≤42 |
| gpt-6-luna/high | ≤42 |

## Figures

- `curves_banded_meter_billing.svg`, `curves_fee_ledger_dropzero.svg` — pass@1 vs length per config.
