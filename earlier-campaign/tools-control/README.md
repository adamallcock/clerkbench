# Tool-availability control (paper Appendix A.5)

Raw run logs for every arm of the paper's tool-availability table, copied
byte-for-byte from the development repository's
`results/relbench/pilot/runs/`. This control ran in the earlier campaign,
on earlier task content, with a calculator and a keyed state store offered
under voluntary function calling. Arms: *neutral* = the unmodified task
prompt with tools attached; *informed* = a developer message saying the
tools exist and may help; *directed* = a developer message instructing the
model to track all state and arithmetic through the tools. The no-tools
baseline is gpt-5.4-nano's twenty-attempt calibration bank on the same cells.

| Config | Arm | L | Correct | File |
|---|---|---|---|---|
| gpt-5.4-nano / xhigh | neutral | 50 | 18/22 | `nano-tools-pilot-20260718/nano-tools-l50-neutral-recovered22of30.jsonl` |
| gpt-5.4-nano / xhigh | informed | 50 | 9/12 | `tools-arms-20260718/tools-gpt-5-4-nano-xhigh-informed-ladder-l50-6.jsonl` |
| gpt-5.4-nano / xhigh | directed | 50 | 3/12 | `tools-arms-20260718/nano-tools-pilot-gpt-5-4-nano-xhigh-tools.jsonl` |
| gpt-5.4-nano / xhigh | neutral | 400 | 0/15 | `nano-tools-pilot-20260718/nano-tools-pilot-gpt-5-4-nano-xhigh-tools.jsonl` |
| gpt-5.6-luna / high | neutral | 50 | 4/12 | `tools-arms-20260718/nano-tools-pilot-gpt-5-6-luna-xhigh-tools.jsonl` |

The neutral L=50 file holds the earliest-completing 22 of 30 attempts: the
other 8 rows were lost to a file collision during collection and no record of
them exists. Score each row with `../../scorers/clerkbench_scorer.py`.
