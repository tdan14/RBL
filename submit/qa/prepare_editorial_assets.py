"""Prepare submission summaries from the immutable collected analysis tables."""
import csv
import json
from pathlib import Path
import re

SUBMIT = Path(__file__).resolve().parents[1]
PROJECT = SUBMIT / 'project'

contexts = {
    'LIT-001': 'Evaluation context: the paper implements a randomized LLC on Rocket-Chip, with Spike/FPGA checks and SPEC CPU2006 evaluation. Sections V-VI and Figures 13 and 16-18 describe its implementation and evaluation. The measured objective is security protection with implementation overhead, not a direct-mapped sensor-cache speedup.',
    'LIT-002': 'Evaluation context: ChampSim experiments include an eight-core baseline with a 16-MiB, 16-way LLC and 64-byte lines, using SPEC CPU2017 and GAP. Sections III and V and Tables V-X describe design and comparison conditions. The separated tag/data budget differs from Q10\'s equal-data-capacity constraint.',
    'LIT-003': 'Evaluation context: Section 8 includes gem5 and trace-based experiments. A reported gem5 configuration has a 1-MiB, 16-way L2 with 64-byte lines. Workloads include MiBench, lmbench, scimark2, GAP, and SPEC2017 evaluation. Sections 4-6 describe the security mechanism. Its protection objective permits hit-rate costs.',
    'LIT-004': 'Evaluation context: the study evaluates robotic processing rather than a synthetic weighing application. Sections III-A, VII, and VIII-D and Figure 5 distinguish application workloads and FCP. Component-level evaluation is separated from the full processor, which contains additional acceleration and prefetching mechanisms.',
    'LIT-005': 'Evaluation context: Section VI-A and Tables I-II describe Scarab experiments with a processor model close to AMD Zen 3 and eleven data-center applications. Figures 8-9 distinguish policy results. The comparison includes an offline reference and a practical profile-guided policy; neither is the submitted data-cache index.',
    'LIT-006': 'Evaluation context: Sections 5-6 describe full-system gem5 evaluation with server workloads and an instruction-cache baseline. These processor-level experiments measure consequences beyond instruction-line miss frequency. Article number 62 and the DOI identify the publication despite differences in pagination across distributed versions.',
    'LIT-007': 'Evaluation context: ChampSim configurations cover four, eight, and sixteen cores, with SPEC2006/2017 and GAP workloads. Sections IV-VII describe the framework and evaluation; Table III reports management overhead. Its multi-mechanism, multicore comparison differs from the single-level static-index experiment.',
    'LIT-008': 'Evaluation context: ChampSim/CRC2 experiments use 27 SPEC2006/2017 programs. Sections 3-4, Table 1, and Figures 7-8 describe predictors, resource budget, and baselines. Section 4.2.1 distinguishes LRU without prefetching from LRU with SPP, so their reported improvement percentages are not interchangeable.',
    'LIT-009': 'Evaluation context: Sections 3-4 describe C++ implementation with the Caffeine simulator. Table 3 compares software caches of 1K, 10K, and 100K items with frames ten times the cache size and policy combinations including LRU. Item count is not interpreted as processor-cache byte capacity.'
}
path = PROJECT / 'Tong_hop_9_bai_bao_tham_khao_Q10.md'
text = path.read_text(encoding='utf-8')
for ident, context in contexts.items():
    pattern = rf'(^## {ident} - .*?\n)(.*?)(?=^## |\Z)'
    match = re.search(pattern, text, re.S | re.M)
    assert match
    if context not in match[2]:
        body = match[2].replace('### Contribution and critical appraisal\n', '### Contribution and critical appraisal\n\n' + context + '\n', 1)
        text = text[:match.start(2)] + body + text[match.end(2):]
path.write_text(text, encoding='utf-8')
counts = {}
for match in re.finditer(r'^## (LIT-\d+) - (.*?)\n(.*?)(?=^## |\Z)', text, re.S | re.M):
    prose = match[3].split('### Contribution and critical appraisal\n', 1)[1]
    counts[match[1]] = dict(title=match[2], prose_words=len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b", prose)))
assert len(counts) == 9 and all(v['prose_words'] >= 800 for v in counts.values())
(SUBMIT / 'qa/literature_word_counts.json').write_text(json.dumps(counts, indent=2), encoding='utf-8')
with (PROJECT / 'results/BATCH01/scenario_summary.csv').open(encoding='utf-8-sig', newline='') as stream:
    rows = list(csv.DictReader(stream))
scenarios = list(dict.fromkeys(row['scenario'] for row in rows))
lines = ['# BATCH01 Results Summary', '', 'The collected matrix contains 24 synthetic traces evaluated under four designs: 96 successful runs and zero failures. Each run has 10,000 warmup and 100,000 measured accesses. Total measured accesses are 9,600,000. The runs form 24 matched trace groups, not 96 independent application samples.', '', 'The table reports miss counts out of 100,000 measured accesses. W4-random reports the mean over all ten seeds; each seed has zero misses for every design. All other rows are single deterministic cases.', '', '| Scenario | D0 misses | D1 misses | D2 misses | DAI-v1 misses | D0 / DAI traffic (bytes) |', '|---|---:|---:|---:|---:|---:|']
for scenario in scenarios:
    group = {r['design']: r for r in rows if r['scenario'] == scenario}
    counts_row = ' | '.join(f"{float(group[d]['miss_rate_mean'])*100000:,.0f}" for d in ['D0', 'D1', 'D2', 'DAI-v1'])
    lines.append(f"| {scenario} | {counts_row} | {float(group['D0']['traffic_bytes_mean']):,.0f} / {float(group['DAI-v1']['traffic_bytes_mean']):,.0f} |")
lines += ['', 'DAI-v1 matches the conventional designs in W1-W4 and improves over D0 only in the declared W5 conflict stress. D1 also removes W5 misses for two competing blocks; D2 does so for two and four. W5 benefits depend on the chosen placement pattern.', '', 'Memory traffic counts 32-byte fills and dirty writebacks in measurement, without a final flush. AMAT values in the separate sensitivity table use assumed lookup and extra miss-penalty cycles; they are not hardware measurements. Insufficient time and financial resources prevented hardware implementation and validation.', '', 'The original CSV tables are retained unchanged. This submission summary is a regenerated presentation of those tables; the historical release is preserved separately in the original evidence archive.']
(PROJECT / 'results/BATCH01/Ket_qua_thi_nghiem.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print('Prepared nine objective appraisals (all >=800 prose words) and count-based results summary.')
