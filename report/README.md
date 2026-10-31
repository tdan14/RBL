# Q10 English research report — LaTeX source

The report follows the supplied CEA201 report structure: Abstract, Introduction, Literature Review, Methodology, Results, Discussion, Conclusion, References, and technical appendices. Class AI21B and the three confirmed member names/IDs are included; no instructor or group number has been invented.

## Build

Main file: `main.tex`. Bibliography: `references.bib`. Compile with XeLaTeX plus BibTeX (or Tectonic, which manages the necessary passes). The source uses UTF-8 to preserve Vietnamese author names and TeX Gyre fonts.

```text
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
```

Alternatively:

```text
tectonic -X compile main.tex --outdir build --keep-logs
```

Compilation is also possible in an online LaTeX editor configured for XeLaTeX. No online upload was performed during preparation.

Tables and the W5 figure are included as generated assets and do not require Python for ordinary compilation. To regenerate them from the included CSV copies, run `python prepare_assets.py` with Matplotlib installed. The numerical checks verify 96 per-run rows, 60 scenario/design summaries, and 864 AMAT sensitivity rows.

## Data and evidence

The CSV copies are derived directly from BATCH01. Their hashes and claim checks are in `data_checks.json`. The report does not alter raw experimental files, layouts, the selected design, or the frozen analysis assumptions. The complete experiment evidence is supplied separately in the Q10 BATCH01 evidence bundle; this report source archive is not a replacement for raw traces and logs.

All nine scholarly references use publication metadata and DOI links, not machine-local file citations. The document distinguishes simulation results, assumed latency calculations, and unverified hardware behavior. It explicitly states that time and financial constraints prevented hardware implementation and validation.

Word counts in `word_counts.json` are approximate prose counts; headings, tables, captions, references, and most mathematics are excluded. The supplied section-length ranges are checked before release.

## Included source files

- `main.tex`, `references.bib`
- `tables/`: generated results, traffic, and environment tables
- `figures/`: W5 scientific figure in PDF/PNG
- `data/`: numerical tables and software version fields used by the report
- `prepare_assets.py`, `data_checks.json`, `word_counts.json`

The portable compiler download, its cache, build intermediates and page-rendering QA images are excluded from the source archive.
