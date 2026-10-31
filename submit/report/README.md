# English Research Report - LaTeX Source

The report presents the Q10 experiment for CEA201, class AI21B, with the three confirmed group members. It contains an abstract, introduction, literature review, methodology, results, discussion, conclusion, nine scholarly references, and technical appendices. The supplied section-length ranges are checked in `word_counts.json`.

## Compilation

From this directory, with XeLaTeX and BibTeX available:

```text
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
```

Alternatively, Tectonic manages the bibliography and repeat passes:

```text
tectonic -X compile main.tex --outdir build --keep-logs
```

UTF-8 input and TeX Gyre font files preserve Vietnamese author names. Tables and the scientific figure are included. Python is unnecessary for ordinary compilation. Asset regeneration uses `python prepare_assets.py` with Matplotlib and NumPy; the included CSV files are byte-identical copies of the collected analysis tables.

The bibliography uses publication metadata and DOI links. There are no machine-local bibliographic citations. Hardware implementation and validation were infeasible because time and financial resources were insufficient; simulated counters and assumed-latency estimates remain explicitly distinguished from hardware measurements.

The portable compiler, font cache, temporary build files, and page-rendering images are excluded from the submission. Compilation and PDF checks are documented under the submission-level `qa/` directory.
