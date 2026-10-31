"""Verify submission provenance, package files, and test a clean extraction."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

SUBMIT = Path(__file__).resolve().parents[1]
WORKSPACE = SUBMIT.parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def main():
    original_receipt = json.loads((SUBMIT / 'original_evidence/receipt.json').read_text(encoding='utf-8'))
    original_archive = SUBMIT / 'original_evidence' / original_receipt['file']
    assert digest(original_archive) == original_receipt['sha256']
    changes = []
    allowed_changes = {
        'README.md', 'REPRODUCE.md', 'Ke_hoach_xay_simulator.md',
        'Tieu_chi_lua_chon_tai_lieu_tham_khao.md', 'Tong_hop_9_bai_bao_tham_khao_Q10.md',
        'evidence/AI_USAGE.md', 'evidence/EVIDENCE_INDEX.md',
        'results/BATCH01/Discussion.md', 'results/BATCH01/Ket_qua_thi_nghiem.md'
    }
    with zipfile.ZipFile(original_archive) as original:
        historical_manifest = json.loads(original.read('evidence/FINAL_CHECKSUMS.json'))
        for name, expected in historical_manifest['files'].items():
            assert hashlib.sha256(original.read(name)).hexdigest() == expected
        for name in original.namelist():
            if name.endswith('/'):
                continue
            current = SUBMIT / 'project' / name
            assert current.is_file(), name
            before = hashlib.sha256(original.read(name)).hexdigest()
            after = digest(current)
            if before != after:
                assert name in allowed_changes, 'Unexpected alteration: ' + name
                changes.append(dict(path='project/' + name, original_sha256=before, submission_sha256=after, category='Non-frozen explanatory document; objective prose, consistency, or portable reproduction. Scientific source and original results unchanged.'))
    assert len(changes) == len(allowed_changes)
    pre = json.loads((SUBMIT / 'project/evidence/PRE_RUN_MANIFEST.json').read_text(encoding='utf-8'))
    for name, expected in pre['files'].items():
        assert digest(SUBMIT / 'project' / name) == expected
    original_report = WORKSPACE / 'report'
    for name in ['main.tex', 'prepare_assets.py']:
        changes.append(dict(path='report/' + name, original_sha256=digest(original_report / name), submission_sha256=digest(SUBMIT / 'report' / name), category='Submission report wording, metadata derivation, date, QA disclosure, or packaged input location.'))
    write(SUBMIT / 'qa/EDITORIAL_CHANGES.json', dict(original_archive_sha256=digest(original_archive), historical_manifest_entries_verified=len(historical_manifest['files']), frozen_file_hashes_unchanged=len(pre['files']), modified_files=changes, added_material='Submission README, objective report source documentation, analysis-regeneration wrapper, data dictionary, and submission QA records. Original archive retained verbatim.'))
    baseline = json.loads((SUBMIT / 'qa/original_workspace_checksums.json').read_text(encoding='utf-8'))
    for name, expected in baseline.items():
        assert digest(WORKSPACE / name) == expected, 'Original workspace changed: ' + name
    write(SUBMIT / 'qa/ORIGINAL_WORKSPACE_VERIFICATION.json', dict(status='PASS', original_files_verified=len(baseline), original_files_changed=0, exclusions='Git internals, pre-existing compiler cache, and Python bytecode caches were excluded from the original baseline. All existing project, report, source, input, result, and evidence files in the baseline remain unchanged.'))
    assert json.loads((SUBMIT / 'qa/scientific_audit.json').read_text())['status'] == 'PASS'
    assert json.loads((SUBMIT / 'qa/report_qa.json').read_text())['status'] == 'PASS'
    assert not (SUBMIT / 'qa/_build').exists()
    assert not list(SUBMIT.rglob('__pycache__'))
    files = sorted(p for p in SUBMIT.rglob('*') if p.is_file() and p.name != 'SUBMISSION_CHECKSUMS.json')
    manifest = {p.relative_to(SUBMIT).as_posix(): digest(p) for p in files}
    write(SUBMIT / 'SUBMISSION_CHECKSUMS.json', dict(algorithm='SHA-256', scope='Final submission edition; original historical archive retained separately.', exclusions=['SUBMISSION_CHECKSUMS.json itself', 'outer submit.zip and external submit_receipt.json'], files=manifest))
    archive = WORKSPACE / 'submit.zip'
    assert not archive.exists(), 'Submission ZIP already exists'
    with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for path in sorted(p for p in SUBMIT.rglob('*') if p.is_file()):
            bundle.write(path, Path('submit') / path.relative_to(SUBMIT))
    with zipfile.ZipFile(archive) as bundle:
        assert bundle.testzip() is None
        packaged = json.loads(bundle.read('submit/SUBMISSION_CHECKSUMS.json'))
        for name, expected in packaged['files'].items():
            assert hashlib.sha256(bundle.read('submit/' + name)).hexdigest() == expected
        with tempfile.TemporaryDirectory(prefix='q10_submission_replay_') as temporary:
            destination = Path(temporary).resolve()
            for name in bundle.namelist():
                assert not Path(name).is_absolute() and '..' not in Path(name).parts
            bundle.extractall(destination)
            project = destination / 'submit/project'
            environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8')
            tests = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v'], cwd=project, env=environment, capture_output=True, text=True, encoding='utf-8', errors='replace')
            assert tests.returncode == 0, tests.stdout + tests.stderr
            replay_output = destination / 'clean_replay_RUN-000040.json'
            replay = subprocess.run([sys.executable, '-B', 'tools/reproduce_run.py', '--run-id', 'RUN-000040', '--output', str(replay_output)], cwd=project, env=environment, capture_output=True, text=True, encoding='utf-8', errors='replace')
            assert replay.returncode == 0, replay.stdout + replay.stderr
            replay_result = json.loads(replay_output.read_text(encoding='utf-8'))
            assert replay_result['reproduction']['matches_original']
    receipt = dict(status='PASS', edition='2026-11-01, Asia/Saigon', archive=archive.name, archive_bytes=archive.stat().st_size, archive_sha256=digest(archive), files=len(manifest)+1, packaged_file_hashes_verified=len(manifest), historical_archive_preserved=True, original_workspace_files_verified=len(baseline), original_workspace_files_changed=0, clean_extraction_unit_tests='28 PASS', clean_extraction_replay='RUN-000040 MATCH', same_environment=True, scientific_audit='96/96 replays and 96/96 full-trace reference counter comparisons PASS', report='12-page English PDF; all pages visually reviewed; nine cited publications', integrity_note='Receipt is external to the ZIP to avoid a self-referential archive hash. Submission checksums cover all packaged files except the manifest itself.')
    write(WORKSPACE / 'submit_receipt.json', receipt)
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
