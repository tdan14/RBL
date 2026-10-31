# Q10 Cache Mapping Experiment

This artifact implements a single-level trace-driven cache model. The frozen organizations are D0 (128 sets, one way, conventional index), D1 (64 sets, two ways, conventional index), D2 (32 sets, four ways, conventional index), and DAI-v1 (64 sets, two ways, XOR index).

All organizations contain 4,096 data bytes with 32-byte lines, write-back, write-allocate, and exact LRU. Prefetching, bypassing, coherence, payload computation, CPU timing, and automatic final dirty-line flushing are absent. Packed logical metadata estimates are 352, 376, 416, and 376 bytes respectively, rather than Python memory usage or synthesized area.

## Collected results

BATCH01 contains 24 synthetic traces and 96 successful runs with no failures. Each run uses 10,000 warmup accesses followed by 100,000 measured accesses. Cache state survives warmup; counters reset at the measurement boundary. Four designs consume the same input for each trace.

DAI-v1 matches the conventional caches in measured miss rate in W1-W4. It eliminates measured misses in the constructed W5 stress cases after warmup, whereas D0 misses on every measured W5 access. Conventional associativity also eliminates W5 misses when the competing group fits in its ways. These findings are conditional on the frozen address layouts and order.

Trương Tô Dân (QE210127) is the designated operator and authorizing member. Codex/Python performed direct execution. Inputs are synthetic, not physical weighing-station measurements. Insufficient time and financial resources prevented hardware implementation and validation.

## Reproduction

The simulator and generator use Python 3.11 and the standard library; the original environment used Python 3.11.9. Plot regeneration also uses Matplotlib and NumPy. Commands run from this directory:

```text
python -B -m unittest discover -s tests -v
python -B tools/reproduce_run.py --run-id RUN-000040 --output reproduction/new_RUN-000040.json
```

The expected outcomes are 28 passing tests and `MATCH` respectively. Replay verifies trace and simulator identity and refuses existing output. Replays verify the same experiment; they are not additional independent samples. `REPRODUCE.md` specifies complete audit and analysis regeneration.

| Location | Role |
|---|---|
| `src/`, `configs/`, `tests/` | Frozen simulator, generator, four configurations, tests, and full-block reference model |
| `traces/` | Five debug inputs, 24 official inputs, specifications, and hashes |
| `runs/BATCH01/` | 96 original result/configuration/trace-reference/log records and batch manifest |
| `results/BATCH01/` | 96 per-run rows, 60 scenario/design summaries, 864 AMAT rows, and plots |
| `validation/` | Historical pre-benchmark automated checks and recorded authorization |
| `ai/` | Original prompts, responses, session records, input snapshots, and design freeze |
| `audit/`, `evidence/` | Historical provenance, source snapshot, environment, and integrity records |

The frozen protocol, workload specification, analysis plan, design freeze, and AI input copies are historical records. Their planning language describes the pre-experiment stage. The original evidence archive is retained separately in the submission. Its checksum manifest applies to that original release; the submission manifest covers revised explanatory documents.

Every access is uppercase R/W, an aligned unsigned 32-bit byte address, and size 4. Invalid input produces a failure with a line number. Trace length must equal the requested warmup plus measurement count. Every miss fills a complete line. Measured traffic is `32 * (line_fills + dirty_writebacks)` bytes; warmup traffic and final flushing are excluded. Dirty lines carried into measurement can cause measured writebacks. Zero measured misses does not imply zero compulsory misses over the entire trace.

AMAT is an assumed lookup time plus miss rate times an additional miss penalty. It excludes writeback stalls and is not measured hardware latency. Python wall-clock duration records execution only.
