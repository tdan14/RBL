"""Audit preserved records and replay all BATCH01 scientific results."""
from pathlib import Path
import csv
import hashlib
import io
import json
import statistics
import sys
import time
import unittest

SUBMIT = Path(__file__).resolve().parents[1]
ROOT = SUBMIT / 'project'
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
from src.simulator.models import Config
from src.simulator.runner import run_trace, sha256, source_identity
from src.simulator.trace import read_trace
from src.workloads import encoded_trace, validate_trace
from tests.reference import ReferenceCache


def rows(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def close(actual, expected):
    if expected is None:
        assert actual == ''
    else:
        assert abs(float(actual) - expected) < 1e-10, (actual, expected)


def main():
    began = time.perf_counter()
    pre = json.loads((ROOT / 'evidence/PRE_RUN_MANIFEST.json').read_text(encoding='utf-8'))
    for path, digest in pre['files'].items():
        assert sha256(ROOT / path) == digest, path
    manifest = json.loads((ROOT / 'traces/manifests/manifest.json').read_text(encoding='utf-8'))
    for spec in manifest['traces']:
        assert sha256(ROOT / spec['path']) == spec['sha256']
        digest = hashlib.sha256()
        for line in encoded_trace(spec):
            digest.update(line)
        assert digest.hexdigest() == spec['sha256']
        stats = validate_trace(spec, read_trace(ROOT / spec['path']))
        assert all(stats[key] == spec[key] for key in stats)
    print('PASS: frozen files, 24 trace hashes, regeneration and access-level specifications.', flush=True)
    suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'), top_level_dir=str(ROOT))
    stream = io.StringIO()
    test_result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    (SUBMIT / 'qa/unit_tests.log').write_text(stream.getvalue(), encoding='utf-8')
    assert test_result.wasSuccessful()
    print(f'PASS: {test_result.testsRun} unit tests.', flush=True)
    entries = rows(ROOT / 'runs/BATCH01/RUN_MANIFEST.csv')
    assert len(entries) == 96 and len({r['run_id'] for r in entries}) == 96
    assert {(r['trace_id'], r['design_id']) for r in entries} == {(t['trace_id'], d) for t in manifest['traces'] for d in ['D0', 'D1', 'D2', 'DAI-v1']}
    fingerprint = source_identity()['source_sha256']
    originals = {}
    replay_rows = []
    for entry in entries:
        ident = entry['run_id']
        original = json.loads((ROOT / entry['result_path']).read_text(encoding='utf-8'))
        assert sha256(ROOT / entry['result_path']) == entry['result_sha256']
        assert original['status'] == 'SUCCESS' and original['metrics_validated']
        assert original['simulator']['source_sha256'] == fingerprint
        cfg = Config.load(ROOT / f"configs/{entry['design_id']}.json")
        spec = next(t for t in manifest['traces'] if t['trace_id'] == entry['trace_id'])
        replay = run_trace(cfg, ROOT / spec['path'], mode='debug', run_id='SUBMISSION-QA-' + ident, trace_id=spec['trace_id'], seed=spec['seed'])
        assert replay['status'] == 'SUCCESS'
        for field in ['counters', 'metrics', 'config', 'observed', 'requested']:
            assert replay[field] == original[field], (ident, field)
        assert replay['trace']['sha256'] == original['trace']['sha256']
        oracle = ReferenceCache(cfg)
        counts = dict(accesses=0, hits=0, misses=0, read_misses=0, write_misses=0, evictions=0, dirty_writebacks=0, line_fills=0)
        for i, access in enumerate(read_trace(ROOT / spec['path'])):
            hit, victim, wb = oracle.access(access.operation, access.address)
            if i >= 10000:
                counts['accesses'] += 1
                counts['hits'] += int(hit)
                counts['misses'] += int(not hit)
                counts['read_misses'] += int(not hit and access.operation == 'R')
                counts['write_misses'] += int(not hit and access.operation == 'W')
                counts['evictions'] += int(victim is not None)
                counts['dirty_writebacks'] += int(wb is not None)
                counts['line_fills'] += int(not hit)
        assert counts == original['counters'], ident
        originals[ident] = original
        replay_rows.append(dict(run_id=ident, trace_id=entry['trace_id'], design=entry['design_id'], replay_match=True, full_trace_reference_match=True, counters=counts, original_sha256=entry['result_sha256']))
        print(f'PASS {len(replay_rows)}/96 {ident}: replay and full-block reference counters match.', flush=True)
    raw = rows(ROOT / 'results/BATCH01/all_runs.csv')
    summary = rows(ROOT / 'results/BATCH01/scenario_summary.csv')
    amat = rows(ROOT / 'results/BATCH01/amat_sensitivity.csv')
    assert (len(raw), len(summary), len(amat)) == (96, 60, 864)
    baselines = {r['trace']['trace_id']: r for r in originals.values() if r['design_id'] == 'D0'}
    for row in raw:
        original = originals[row['run_id']]
        assert row['design'] == original['design_id'] and row['trace_id'] == original['trace']['trace_id']
        for key, value in original['counters'].items():
            assert int(row[key]) == value
        mr = original['counters']['misses'] / 100000
        baseline = baselines[row['trace_id']]['metrics']['miss_rate']
        close(row['miss_rate'], mr)
        close(row['miss_rate_delta_pp'], 100 * (baseline - mr))
        close(row['relative_miss_reduction_pct'], 100 * (baseline - mr) / baseline if baseline else None)
        assert int(row['memory_traffic_bytes']) == 32 * (original['counters']['line_fills'] + original['counters']['dirty_writebacks'])
    for row in summary:
        group = [r for r in originals.values() if r['scenario_id'] == row['scenario'] and r['design_id'] == row['design']]
        rates = [r['metrics']['miss_rate'] for r in group]
        assert int(row['n']) == len(group)
        for key, value in dict(miss_rate_mean=statistics.mean(rates), miss_rate_sample_stddev=statistics.stdev(rates) if len(rates) > 1 else None, miss_rate_min=min(rates), miss_rate_max=max(rates), traffic_bytes_mean=statistics.mean(r['metrics']['memory_traffic_bytes'] for r in group)).items():
            close(row[key], value)
        assert row['runs'].split(';') == [r['run_id'] for r in group]
    plan = json.loads((ROOT / 'analysis_plan.json').read_text(encoding='utf-8'))
    for row in amat:
        original = originals[row['run_id']]
        times = plan['hit_time_scenarios_cycles'][row['assumption']]
        penalty = int(row['miss_penalty_cycles'])
        assert penalty in plan['miss_penalties_cycles']
        value = times[row['design']] + original['metrics']['miss_rate'] * penalty
        base = times['D0'] + baselines[row['trace_id']]['metrics']['miss_rate'] * penalty
        close(row['estimated_amat_cycles'], value)
        close(row['D0_estimated_amat_cycles'], base)
        close(row['assumed_hit_cycles'], times[row['design']])
        close(row['estimated_amat_reduction_pct'], 100 * (base - value) / base)
    report = dict(status='PASS', frozen_file_hashes_verified=len(pre['files']), traces_verified=24, generator_regenerations=24, trace_specifications_verified=24, unit_tests=test_result.testsRun, full_replays=96, full_trace_reference_comparisons=96, measured_accesses=9600000, csv_rows=dict(all_runs=96, scenario_summary=60, amat_sensitivity=864), scientific_fields_unchanged=True, elapsed_seconds=round(time.perf_counter()-began, 3), scope='Submission QA on the same installed environment; these checks are not additional independent samples, hardware validation, or independent human review.', runs=replay_rows)
    (SUBMIT / 'qa/scientific_audit.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print('PASS: all 96/60/864 derived CSV rows recomputed from original records.', flush=True)


if __name__ == '__main__':
    main()
