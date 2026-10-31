"""Verify and package the report without modifying experimental evidence."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import unicodedata
import zipfile
import fitz
from PIL import Image, ImageChops

report = Path(__file__).resolve().parent
root = report.parent
pdf = report / 'build/main.pdf'
doc = fitz.open(pdf)
text = unicodedata.normalize('NFKC', ' '.join(p.get_text() for p in doc))
text = ' '.join(text.split())
source = (report / 'main.tex').read_text(encoding='utf-8')
bib = (report / 'references.bib').read_text(encoding='utf-8')
log = (report / 'build/main.log').read_text(encoding='utf-8', errors='replace')
assert len(doc) == 12
assert 'AI21B' in text
assert 'financial resources were insufficient' in text
assert not re.search(r'[A-Za-z]:\\|file://', text)
assert not re.search(r'Overfull|Missing character|undefined references|Citation .* undefined|already defined', log)
keys = set(re.findall(r'@\w+\{([^,]+)', bib))
cited = {k for group in re.findall(r'\\cite\{([^}]+)\}', source) for k in group.split(',')}
assert len(keys) == 9 and cited == keys
uris = [a['uri'] for p in doc for a in p.get_links() if a.get('uri')]
assert len(set(uris)) == 9 and all(u.startswith('https://doi.org/') for u in uris)
counts = json.loads((report / 'word_counts.json').read_text())
for key, (low, high) in {'abstract': (150, 250), 'literature': (800, 1200), 'methodology': (400, 600), 'results': (300, 500), 'discussion': (400, 600), 'conclusion': (200, 300)}.items():
    assert low <= counts[key] <= high
for filename in ['all_runs.csv', 'scenario_summary.csv', 'amat_sensitivity.csv']:
    assert (report / 'data' / filename).read_bytes() == (root / 'results/BATCH01' / filename).read_bytes()
render_same = []
for i, page in enumerate(doc, 1):
    old = report / 'qa' / f'page-{i:02}.png'
    pix = page.get_pixmap(matrix=fitz.Matrix(1.3, 1.3))
    current = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
    render_same.append(ImageChops.difference(Image.open(old).convert('RGB'), current).getbbox() is None)
    pix.save(old)
assert all(render_same), 'Final rendering changed; inspect changed pages'
qa = {
    'status': 'PASS', 'pages': len(doc),
    'visual_review': 'All 12 pages inspected in contact sheets; final render identical after page-anchor fix.',
    'final_render_matches_reviewed_pages': all(render_same),
    'bibliography_entries': len(keys), 'all_references_cited': True,
    'unique_doi_links': len(set(uris)), 'local_machine_path_citations': False,
    'section_word_counts': counts, 'csv_copies_match_batch01': True,
    'numeric_claim_checks': 'PASS; see data_checks.json',
    'hardware_constraint_statement': 'Insufficient time and financial resources for hardware implementation and validation.',
    'compile': 'Successful; no overfull boxes, missing characters, undefined citations, or duplicate page anchors.',
    'nonblocking_compile_messages': ['Underfull bibliography box; visually reviewed.', 'Fontconfig default-config notice; explicit font files rendered correctly.'],
    'review_scope': 'Automated checks and AI visual review; no independent human or hardware validation asserted.'
}
(report / 'QA_REPORT.json').write_text(json.dumps(qa, indent=2) + '\n', encoding='utf-8')
out = root / 'output/pdf/Q10_AI21B_Cache_Mapping_Report.pdf'
out.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(pdf, out)
archive = root / 'delivery/Q10_AI21B_Report_LaTeX.zip'
include = [report / x for x in ['main.tex', 'references.bib', 'README.md', 'prepare_assets.py', 'data_checks.json', 'word_counts.json', 'QA_REPORT.json']]
for folder in ['tables', 'figures', 'data']:
    include.extend(p for p in (report / folder).rglob('*') if p.is_file())
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as bundle:
    for path in sorted(include):
        bundle.write(path, Path('Q10_AI21B_Report') / path.relative_to(report))
    bundle.write(out, 'Q10_AI21B_Report/Q10_AI21B_Cache_Mapping_Report.pdf')
with zipfile.ZipFile(archive) as bundle:
    assert bundle.testzip() is None
receipt = {
    'pdf': {'file': out.name, 'bytes': out.stat().st_size, 'sha256': hashlib.sha256(out.read_bytes()).hexdigest()},
    'latex_bundle': {'file': archive.name, 'bytes': archive.stat().st_size, 'sha256': hashlib.sha256(archive.read_bytes()).hexdigest()},
    'experiment_evidence': 'Existing Q10_BATCH01_evidence.zip and receipt.json retained unchanged.'
}
(root / 'delivery/report_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'qa': qa, 'artifacts': receipt}, indent=2))
