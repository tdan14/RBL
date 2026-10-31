# Simulator Architecture and Implementation Record

The implemented simulator follows the frozen DAI-v1 design and common cache protocol. The original prospective implementation plan is preserved in the original evidence archive. This submission edition describes the completed implementation.

| Component | Implemented responsibility |
|---|---|
| `src/simulator/models.py` | Frozen configuration validation, line state, counters, access validation, and packed metadata estimates |
| `src/simulator/mapping.py` | Conventional/XOR set selection, tag identification, and inverse block recovery |
| `src/simulator/cache.py` | Hit/miss handling, invalid-way preference, exact LRU, dirty writebacks, and invariants |
| `src/simulator/trace.py` | Input parsing with line-numbered failures |
| `src/simulator/runner.py` | Warmup/measurement transition, source identity, JSON results, and optional event logs |
| `src/workloads.py` | Frozen synthetic generation and access-number-based trace validation |
| `tests/` | 28 tests, hand-derived sequences, and a separate full-block-ID reference representation |

The common engine holds data capacity, line size, write policy, allocation, and replacement semantics constant. D0 uses one way, D1 and DAI-v1 use two ways, and D2 uses four. DAI-v1 uses a static XOR index; it is not a skewed two-bank design or a runtime learning policy.

Each run begins empty. Warmup updates resident lines, dirty flags, and replacement state while excluding its counters. Measurement resets counters and retains state. Each miss fills one line; each dirty valid victim writes one line back to its recovered address. No final flush is performed. Invalid operations, sizes, alignment, and address ranges fail before cache-state mutation.

Validation before the official matrix comprised 28 tests and 20 small trace/configuration comparisons. The source snapshot, hashes, and sign-off record preceded the 24-input freeze and 96-run batch. Submission QA additionally replays all 96 original results and compares their measured counters with the reference model. These checks are AI-assisted implementation evidence, not independent human or hardware validation.

The simulator omits payload values, filter arithmetic, timing, coherence, prefetching, and bypassing. It therefore evaluates declared address streams rather than the numerical accuracy or real-time behavior of a weighing application. Insufficient time and financial resources prevented implementing and validating a hardware prototype.
