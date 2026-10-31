# Evidence Index - Q10 BATCH01

**Designated operator and authorizing member:** Trương Tô Dân, QE210127. **Direct executor:** Codex/Python. Original timestamps use UTC+07:00.

| Evidence | Artifact | Scope |
|---|---|---|
| Frozen protocol | `experiment_protocol.md`, `ai/inputs/experiment_protocol.md` | Common constraints and measurement rules |
| AI design process | `ai/prompts/`, `ai/responses/`, `ai/AI_SESSION_LOG.md` | Three proposals, critique, and selection history |
| Design freeze | `ai/AI_DESIGN_FREEZE.md` | DAI-v1 specification preceding implementation and official runs |
| Pre-run source | `source_snapshot_before_runs.zip`, `PRE_RUN_MANIFEST.json` | Source identity and explicitly recorded uncommitted changes |
| Original validation | `validation/IMPLEMENTATION_SIGNOFF.md` and manifest-referenced validation folder | 28 tests and 20 small trace/configuration comparisons |
| Input specification | `workload_spec.md`, `WORKLOAD_FREEZE.md`, `traces/manifests/manifest.json` | Frozen layouts, access rules, seeds, and trace hashes |
| Original inputs | `traces/official/` | 24 traces of 110,000 accesses each |
| Analysis assumptions | `analysis_plan.json` | Metrics, zero-baseline rule, seed summaries, and assumed latency scenarios |
| Raw runs | `runs/BATCH01/RUN-000001` through `RUN-000096` | Results, logs, configuration snapshots, and trace references |
| Batch provenance | `runs/BATCH01/RUN_MANIFEST.csv`, `batch.log`, `audit/AUDIT_LOG.jsonl` | Run identity, chronology, status, and result hashes |
| Derived tables | `results/BATCH01/` | 96 per-run, 60 summary, and 864 AMAT rows |
| Original sampled replays | `reproduction/summary.json`, `clean_copy_check.json` | Six sampled replays and one clean-copy replay in the same environment |
| Original release integrity | `FINAL_CHECKSUMS.json`, `FINAL_VERIFICATION.json` | Historical archive, not hashes of submission-edited documents |
| Submission verification | Submission-level `qa/` | Complete replays, full-block reference counters, CSV checks, publication review, and PDF QA |

Paths in the table are project-relative except the pre-run source and original integrity filenames, which are relative to this `evidence` directory. They identify packaged artifacts rather than scholarly publications.

| Claim | Original run range | Finding |
|---|---|---|
| W1 | RUN-000001 to RUN-000008 | Every design has a 12.5% measured miss rate; read/write traffic differs |
| W2 | RUN-000009 to RUN-000020 | 1/4-KiB buffers have zero measured misses; 16-KiB buffer has 12.5% |
| W3 | RUN-000021 to RUN-000040 | Corresponding rates match across designs for all five windows |
| W4 | RUN-000041 to RUN-000084 | Round-robin and all ten random seeds have zero measured misses |
| W5 | RUN-000085 to RUN-000096 | D0 has 100% measured misses; DAI-v1 has zero after warmup |

The unmodified original archive and receipt are supplied at submission level under `original_evidence/`. Its SHA-256 remains the original receipt value. The submission manifest and editorial ledger separately identify final presentation files and revised non-frozen documentation. Hashes establish byte identity, not scientific truth or independent review.
