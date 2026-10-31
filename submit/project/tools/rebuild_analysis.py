"""Regenerate analysis in an isolated copy without editing collected files."""

import argparse
import csv
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        parser.error('Output already exists; an unused destination is required')
    with tempfile.TemporaryDirectory(prefix='q10_analysis_') as temporary:
        workspace = Path(temporary) / 'project'
        shutil.copytree(ROOT, workspace, ignore=shutil.ignore_patterns('__pycache__', 'results'))
        reference = ROOT / 'results/BATCH01'
        process = subprocess.run([sys.executable, '-B', str(workspace / 'tools/analyze_experiments.py')], cwd=workspace, capture_output=True, text=True, encoding='utf-8', errors='replace')
        if process.returncode:
            raise RuntimeError(process.stdout + process.stderr)
        regenerated = workspace / 'results/BATCH01'
        for filename in ['all_runs.csv', 'scenario_summary.csv', 'amat_sensitivity.csv']:
            if read_csv(regenerated / filename) != read_csv(reference / filename):
                raise RuntimeError('Analysis differs from collected table: ' + filename)
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(regenerated, output)
        (output / 'regeneration.log').write_text(process.stdout + process.stderr, encoding='utf-8')
    print('MATCH: 96 per-run, 60 summary, and 864 AMAT rows regenerated.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
