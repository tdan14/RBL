# CEA201 Research-Based Learning Submission

**Class:** AI21B  
**Topic:** Question 10 - AI-Assisted Cache Mapping for Continuous Data Streams  
**Submission edition:** 1 November 2026

| Group member | Student ID |
|---|---|
| Trương Tô Dân | QE210127 |
| Trần Châu Hoàng Nam | QE210145 |
| Dương Quốc Thịnh | QE210121 |

The report evaluates a static two-way XOR-indexed cache against direct-mapped, conventional two-way, and conventional four-way caches. All designs contain 4 KiB of data with 32-byte lines. BATCH01 contains 24 synthetic traces and 96 successful runs: 24 matched trace groups across four designs. Each run contains 10,000 warmup accesses and 100,000 measured accesses.

DAI-v1 matches all conventional designs in measured miss rate in W1-W4. Its advantage is confined to the constructed W5 conflict stress cases. The study establishes neither a general speedup nor verified energy savings. Hardware implementation and validation were not feasible because time and financial resources were insufficient.

| Location | Contents |
|---|---|
| `Q10_AI21B_Report.pdf` | Final English research report |
| `report/` | LaTeX source, bibliography, numerical inputs, tables, and figure |
| `project/` | Simulator, configurations, tests, traces, original results/logs, AI records, and analysis |
| `original_evidence/` | Unmodified original BATCH01 evidence archive and original receipt |
| `qa/` | Audit findings, verification logs, editorial change ledger, and package checks |
| `SUBMISSION_CHECKSUMS.json` | SHA-256 submission hashes, excluding the manifest itself |

The report is the primary narrative. `project/REPRODUCE.md` specifies reproduction commands. `qa/QA_REVIEW.md` records corrections and remaining scientific limitations.

The simulator, configurations, frozen protocol, workload specification, traces, original results/logs, and AI prompts/responses retain their collected bytes. Historical AI exchanges retain their conversational wording as evidence. The historical checksum manifest identifies the original archive; the submission manifest identifies this edition. Editorial changes to non-frozen documents are recorded separately in `qa/EDITORIAL_CHANGES.json`.

Design approval and execution authorization are attributed to Trương Tô Dân. Direct execution and automated verification are attributed to Codex/Python. Submission QA is an AI-assisted review, not an independent teacher's assessment, independent human review, or hardware validation.
