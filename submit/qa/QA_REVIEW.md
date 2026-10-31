# Submission Quality Review

**Review date:** 1 November 2026, Asia/Saigon.  
**Scope:** report, literature appraisal, implementation, frozen inputs, original results, reproduction, and packaging.  
**Review method:** AI-assisted critical review with executed checks. This record does not claim that a teacher or an independent human reviewer performed the assessment.

## Findings and resolutions

| Issue | Assessment and correction |
|---|---|
| Statistical unit | The phrase “96 paired runs” was ambiguous. The report now identifies 96 runs in 24 matched trace groups and explicitly rejects interpretation as 96 independent samples. |
| Hypothesis language | A formal null hypothesis was stated without an inferential test. The introduction now uses descriptive research questions, consistent with the frozen analysis plan. |
| Mechanism attribution | DAI-v1 differs from direct mapping in both associativity and index. The report retains D1 as the closer two-way control and limits attribution accordingly. |
| Resource accounting | The report now derives the 352/376/416/376-byte metadata estimates from tag widths and replacement state. Equal data capacity is not presented as equal area or total implementation cost. |
| Hardware claims | The report explicitly states that insufficient time and financial resources prevented hardware implementation and validation. Lookup latency, area, power, and application speedup remain unmeasured. |
| AMAT interpretation | The estimate remains an assumed lookup cost plus miss rate times additional penalty. Writeback stalls are excluded. Miss reduction is not described as equivalent execution-time reduction. |
| Finite W3 horizon | The 2,048-sample case covers 53 full sampling cycles plus a partial cycle. No steady-state or real-time claim is made. |
| Favorable W5 layout | The declared stress pattern and its compatibility with XOR placement remain explicit. Zero W5 misses is not generalized to arbitrary sensor layouts. |
| Uninformative W4 cases | Zero rates across all ten seeds remain reported. No layout was replaced after results were observed to manufacture a candidate advantage. |
| Literature count | The active selection criteria now specify nine publications, superseding the preliminary six-to-eight target. Original criteria remain archived verbatim. |
| Literature prose | Nine detailed appraisals were rewritten in objective academic prose, each with more than 800 prose words, publication identity, evaluation context, assigned responsibility, and a named conclusion. The synthesis has an overall conclusion. |
| Bibliographic dates | The PAIC journal edition is 2023 despite its DOI substring; the OPODIS 2023 paper was published in 2024. Tartan uses the 2024 proceedings year rather than a later repository cover date. |
| Historical versus final documents | Original prompts, responses, frozen protocol, source snapshot, results, and logs remain verbatim. Historical dialogue and planning language are evidence rather than the final narrative. Non-frozen explanatory documents use objective prose. |
| Portable reproduction | Machine-specific interpreter commands were replaced by host Python commands. Raw execution locations remain only as historical environment fields, not bibliography or portable input lookup. |
| Analysis regeneration | The original analysis refuses existing results. An additional wrapper regenerates analysis in an isolated copy and compares all three CSV tables without changing collected records. Its execution passed. |
| Checksum scope | Historical FINAL_CHECKSUMS applies to the original release. A separate submission manifest and editorial ledger identify the edited edition; historical hashes are not silently reassigned. |
| Date consistency | The submission report is dated 1 November 2026. Original experiment and search timestamps remain 31 October 2026. |

## Executed scientific checks

`scientific_audit.json` and `scientific_audit.log` record the following completed checks:

- 45 frozen file hashes match the pre-run manifest.
- All 24 original trace hashes match; byte generation reproduces all hashes.
- Every access in each official trace matches the access-number-based specification.
- All 28 original unit tests pass; the test output is retained separately.
- All 96 original result hashes match the original run manifest.
- All 96 replays match counters, metrics, configuration, observed/requested periods, and trace hash.
- Measured counters for all 96 full traces match the separate full-block-ID/LRU-list reference representation.
- All numeric fields in the 96 per-run, 60 summary, and 864 AMAT rows were recomputed and matched.
- The original analysis script regenerates CSV tables exactly in an isolated copy.

The reference model is a different representation of the declared semantics, not an optimal policy or independent human assessment. These checks use the same installed environment. Replay does not create new independent experimental samples.

## Report and source checks

The PDF compiles successfully and contains 12 pages. Every rendered page was visually inspected for layout, tables, formulas, author-name glyphs, figure legibility, page numbering, and bibliography. Nine bibliography entries are cited; all nine DOI targets are included as publication links. The report contains no machine-local bibliographic citations or unresolved reference markers. Approximate body counts are recorded in `report/word_counts.json` and satisfy the supplied section ranges.

The compiled document has one nonblocking underfull bibliography-line warning. The affected reference is readable and unclipped. The compiler's Fontconfig default-configuration notice does not prevent the explicitly specified font files from rendering. There are no overfull boxes, missing glyph reports, undefined citations, or duplicate page anchors.

The source review found no assistant-to-user instructions in the simulator's explanatory comments or docstrings. Technical validation rules and historical authorization data remain part of their frozen implementation. The final report, active project overview, reproduction guide, implementation description, literature criteria, literature appraisal, evidence explanation, and results discussion use objective authorial language.

## Publication evidence and access limits

The publication identities and the report's factual descriptions were checked against the saved author/publisher full texts and bibliographic records. Submission review also accessed the following primary sources:

- [Song et al., author full text](https://wsong83.github.io/publication/comparch/tc2024.pdf).
- [Maya, author/institutional full text](https://www.cse.iitb.ac.in/~biswa/ISCA2024.pdf).
- [SassCache, author full text](https://antoonpurnal.github.io/files/pdf/SassCache.pdf).
- [Tartan, institutional full text](https://www.pdl.cmu.edu/PDL-FTP/associated/Tartan-ISCA24.pdf).
- [Micro-operation replacement, author full text](https://www.thu-haslab.org/publication/co-public/2025-from-optimal-to-practical/19_HPCA2025_micro-op_cache.pdf).
- [CHROME, institutional full text](https://cs.iit.edu/~scs/assets/files/lu2024chrome.pdf).
- [PAIC, publisher record](https://jcst.ict.ac.cn/article/doi/10.1007/s11390-022-1573-3) and its linked full text.
- [ALPS, publisher record](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.OPODIS.2023.34) and full text.

The EMISSARY author URL returned HTTP 403 during the submission review and the DOI page was not retrievable through the browser tool. Its previously saved full text and DOI metadata remain the basis for verification. The source register records this limit. The absence of an observed correction or retraction notice is not a guarantee of current publication status, particularly for inaccessible pages. No fabricated successful access is recorded.

## Remaining scientific limits

The results are conditional on synthetic addresses, one data capacity, one line size, a fixed finite prefix, no coherence, no prefetching or bypassing, and no hardware timing model. Random seeds vary sensor selection rather than physical buffer layout. The study contains one selected candidate and does not experimentally compare human-only design against AI-assisted design. It therefore does not establish general AI design effectiveness, universal mapping superiority, hardware speedup, security, or energy savings.

A complete chat export and a verified exact AI model identifier are absent. Existing prompts, responses, session records, and the design specification are retained. Contributions are assignments and recorded authorization; individual manual completion is not inferred. No scientific input or original result was modified to improve the reported outcome.

The final packaging receipt records checksum verification, clean extraction/replay, archive integrity, and preservation of the original workspace. Those checks establish artifact consistency and runnability within the tested environment, not a guarantee of a particular grade or the absence of every possible scientific limitation.
