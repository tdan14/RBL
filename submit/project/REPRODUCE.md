# Reproducibility Procedure

Original BATCH01 records are reference results. Replays use new output locations. Commands run from `project` using a host Python 3.11 installation; the collected environment used Python 3.11.9. No machine-specific interpreter path is required.

## Tests and single-record replay

```text
python -B -m unittest discover -s tests -v
python -B tools/reproduce_run.py --run-id RUN-000040 --output reproduction/new_RUN-000040.json
```

Expected outcomes: 28 passing tests; `MATCH` and `reproduction.matches_original=true`. The replay validates trace hash and simulator/configuration fingerprint. The output destination must be unused. RUN-000001 through RUN-000096 are supported. Scientific fields are compared because timestamps and execution locations differ between runs.

## Complete submission audit

From the parent `submit` directory:

```text
python -B qa/run_scientific_audit.py
```

The audit verifies all frozen files, regenerates 24 trace hashes in memory, checks every input access against its specification, runs 28 tests, replays 96 records, and recomputes their measured counters with a full-block reference model. It also recomputes the numerical fields of the 96/60/864 analysis tables. Outputs are written under `qa/`; original records remain unchanged. These are AI-assisted checks in the same environment, not independent samples, independent human review, or hardware validation.

## Analysis regeneration

```text
python -B tools/rebuild_analysis.py --output ../qa/rebuilt_analysis
```

Matplotlib and NumPy are required for figures. The command runs the original frozen analysis script in an isolated temporary copy. The output destination must not exist. All values in the 96 per-run, 60 summary, and 864 AMAT rows are compared to the collected CSV tables. Plot bytes may differ with software versions or PDF metadata. The original analysis script refuses to overwrite collected results.

## LaTeX compilation

From the submission's `report` directory:

```text
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
```

Tectonic is an alternative. XeLaTeX-compatible UTF-8 fonts preserve Vietnamese author names. Tables and the figure are included; ordinary compilation does not require Python. `python prepare_assets.py` regenerates report assets from the included CSV copies with Matplotlib and NumPy.

## Historical integrity and scope

`evidence/PRE_RUN_MANIFEST.json` identifies frozen scientific inputs. `evidence/FINAL_CHECKSUMS.json` identifies the historical release preserved in the submission's `original_evidence/Q10_BATCH01_evidence.zip`. Non-frozen explanatory documents have submission-stage editorial revisions, recorded separately in the submission manifest and change ledger.

Raw JSON retains original execution locations as historical environment fields. These are not bibliographic citations and are not used for portable input lookup. Relative trace references locate the packaged input.

AI evidence consists of original prompts, responses, session records, and design freeze, rather than a complete chat export. No exact model identifier is inferred. Physical sensor measurements, hardware timing or energy, independent machine provisioning, and independent human review are absent.
