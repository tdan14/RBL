"""Derive tables, sensitivity figures and evidence from immutable official runs."""

import csv
import json
from pathlib import Path
import statistics
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
from src.simulator.runner import sha256
from prepare_experiments import audit, now, write_json, OPERATOR

DESIGNS = ("D0", "D1", "D2", "DAI-v1")


def relative_reduction(baseline, candidate):
    return None if baseline == 0 else (baseline - candidate) / baseline * 100


def describe(values):
    return dict(mean=statistics.mean(values), sample_stddev=statistics.stdev(values) if len(values) > 1 else None,
                minimum=min(values), maximum=max(values), n=len(values))


def csv_write(path, rows):
    with path.open("x", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)


def main():
    batch = ROOT / "runs/BATCH01"
    with (batch / "RUN_MANIFEST.csv").open(encoding="utf-8", newline="") as f: manifest = list(csv.DictReader(f))
    if len(manifest) != 96 or any(m["status"] != "SUCCESS" for m in manifest):
        raise RuntimeError("Need exactly 96 successful planned runs; failures retained, analysis blocked")
    trace_manifest = json.loads((ROOT / "traces/manifests/manifest.json").read_text(encoding="utf-8"))
    expected_pairs = {(t["trace_id"], d) for t in trace_manifest["traces"] for d in DESIGNS}
    if {(m["trace_id"], m["design_id"]) for m in manifest} != expected_pairs:
        raise RuntimeError("Run matrix differs from frozen plan")
    frozen = json.loads((ROOT / "evidence/PRE_RUN_MANIFEST.json").read_text(encoding="utf-8"))
    for rel, expected in frozen["files"].items():
        if sha256(ROOT / rel) != expected: raise RuntimeError(f"Pre-run evidence changed: {rel}")
    results = []
    for m in manifest:
        path = ROOT / m["result_path"]
        if sha256(path) != m["result_sha256"]: raise RuntimeError("Raw result modified")
        r = json.loads(path.read_text(encoding="utf-8"))
        if r["mode"] != "official" or r["status"] != "SUCCESS" or not r["metrics_validated"]:
            raise RuntimeError("Invalid result in analysis")
        if r["counters"]["accesses"] != 100000 or r["observed"]["warmup_accesses"] != 10000:
            raise RuntimeError("Measurement periods differ")
        results.append(r)
    out = ROOT / "results/BATCH01"; out.mkdir(parents=True, exist_ok=False)
    figures = out / "figures"; figures.mkdir()
    audit("ANALYSIS_STARTED", batch_id="BATCH01", status="STARTED")
    base = {r["trace"]["trace_id"]: r for r in results if r["design_id"] == "D0"}
    rows = []
    for r in results:
        mr = r["metrics"]["miss_rate"]; baseline = base[r["trace"]["trace_id"]]["metrics"]["miss_rate"]
        rows.append(dict(run_id=r["run_id"], family=r["workload_family"], scenario=r["scenario_id"],
                         trace_id=r["trace"]["trace_id"], seed=r["trace"]["seed"], design=r["design_id"],
                         **r["counters"], miss_rate=mr, memory_traffic_bytes=r["metrics"]["memory_traffic_bytes"],
                         miss_rate_delta_pp=(baseline-mr)*100, relative_miss_reduction_pct=relative_reduction(baseline,mr)))
    csv_write(out / "all_runs.csv", rows)
    scenarios = list(dict.fromkeys(r["scenario_id"] for r in results))
    summaries = []
    for scenario in scenarios:
        for design in DESIGNS:
            group = [r for r in results if r["scenario_id"] == scenario and r["design_id"] == design]
            stat = describe([r["metrics"]["miss_rate"] for r in group])
            summaries.append(dict(scenario=scenario, design=design, n=stat["n"], miss_rate_mean=stat["mean"],
                                  miss_rate_sample_stddev=stat["sample_stddev"], miss_rate_min=stat["minimum"],
                                  miss_rate_max=stat["maximum"],
                                  traffic_bytes_mean=statistics.mean(r["metrics"]["memory_traffic_bytes"] for r in group),
                                  runs=";".join(r["run_id"] for r in group)))
    csv_write(out / "scenario_summary.csv", summaries)
    plan = json.loads((ROOT / "analysis_plan.json").read_text(encoding="utf-8"))
    amat = []
    for row in rows:
        baseline_mr = base[row["trace_id"]]["metrics"]["miss_rate"]
        for assumption, times in plan["hit_time_scenarios_cycles"].items():
            for penalty in plan["miss_penalties_cycles"]:
                value = times[row["design"]] + row["miss_rate"] * penalty
                baseline_value = times["D0"] + baseline_mr * penalty
                amat.append(dict(run_id=row["run_id"], trace_id=row["trace_id"], scenario=row["scenario"],
                                 design=row["design"], assumption=assumption, miss_penalty_cycles=penalty,
                                 assumed_hit_cycles=times[row["design"]], estimated_amat_cycles=value,
                                 D0_estimated_amat_cycles=baseline_value,
                                 estimated_amat_reduction_pct=relative_reduction(baseline_value,value)))
    csv_write(out / "amat_sensitivity.csv", amat)
    # Standard standalone scientific plots, labels in English for font portability.
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    colors = ["#64748b", "#2563eb", "#16a34a", "#dc2626"]
    for filename, field, ylabel in [("miss_rate", "miss_rate_mean", "Measured miss rate (%)"),
                                    ("memory_traffic", "traffic_bytes_mean", "Memory traffic (MiB)")]:
        fig, ax = plt.subplots(figsize=(15, 5.5))
        x = np.arange(len(scenarios)); width = .19
        for j, design in enumerate(DESIGNS):
            series = [next(r for r in summaries if r["scenario"] == s and r["design"] == design) for s in scenarios]
            scale = 100 if field == "miss_rate_mean" else 1/1048576
            y = [r[field]*scale for r in series]
            errors = [(r["miss_rate_sample_stddev"] or 0)*100 for r in series] if field == "miss_rate_mean" else None
            ax.bar(x+(j-1.5)*width, y, width, label=design, color=colors[j], yerr=errors, capsize=2)
        ax.set_xticks(x, scenarios, rotation=45, ha="right"); ax.set_ylabel(ylabel)
        ax.set_title("Q10 / BATCH01 / 100,000 measured accesses per trace; W4-random = 10 seeds")
        ax.legend(ncol=4); ax.grid(axis="y", alpha=.2); ax.set_axisbelow(True); fig.tight_layout()
        fig.savefig(figures / (filename + ".png"), dpi=180); fig.savefig(figures / (filename + ".pdf")); plt.close(fig)
    lines = ["# Kết quả official benchmark Q10 — BATCH01", "",
             f"Người phụ trách/xác nhận chạy: **{OPERATOR}**. Công cụ trực tiếp: Codex/Python. Thời điểm tổng hợp: {now()}.", "",
             "Đã thu đủ 96/96 run SUCCESS, 24 trace tổng hợp × 4 design. Mỗi run giữ nguyên 10.000 warmup + 100.000 access đo. Không dùng dữ liệu đo trạm cân thật.", "",
             "## Bảng kết quả theo scenario", "",
             "Miss rate tính theo %. W4-random là trung bình 10 seed; độ lệch chuẩn mẫu và từng seed có trong CSV. Các trường hợp deterministic không có mẫu lặp độc lập.", "",
             "| Scenario | D0 (%) | D1 (%) | D2 (%) | DAI (%) | DAI − D0 (điểm %) | Traffic D0 / DAI (B) |", "|---|---:|---:|---:|---:|---:|---:|"]
    for s in scenarios:
        group = {r["design"]: r for r in summaries if r["scenario"] == s}
        rates = [group[d]["miss_rate_mean"]*100 for d in DESIGNS]
        lines.append(f"| {s} | " + " | ".join(f"{v:.5f}" for v in rates) +
                     f" | {rates[3]-rates[0]:+.5f} | {group['D0']['traffic_bytes_mean']:.0f} / {group['DAI-v1']['traffic_bytes_mean']:.0f} |")
    lines += ["", "## Nhận xét rút từ dữ liệu", ""]
    for s in scenarios:
        group = {r["design"]: r for r in summaries if r["scenario"] == s}
        d0, dai, d1 = (group[d]["miss_rate_mean"] for d in ("D0", "DAI-v1", "D1"))
        outcome = "giảm" if dai < d0 else "tăng" if dai > d0 else "bằng"
        rel = relative_reduction(d0,dai)
        lines.append(f"- **{s}:** miss rate DAI {outcome} so D0; D0={d0*100:.5f}%, DAI={dai*100:.5f}%, D1={d1*100:.5f}%. " +
                     ("Relative reduction N/A vì D0=0." if rel is None else f"Mức giảm tương đối so D0={rel:.5f}%."))
    lines += ["", "## Giới hạn và kết luận", "",
              "Đây là kết quả mô phỏng của các trace đã chốt, không chứng minh hiệu năng/điện năng phần cứng hoặc tính tối ưu phổ quát. W5 là stress phù hợp cấu trúc XOR; không suy rộng lợi ích ở đây cho dữ liệu cân thực. W4 dùng bốn buffer liền nhau, tổng vừa cache; giữ nguyên layout và kết quả ngay cả khi không phân biệt thiết kế.", "",
              "So DAI–D1 giúp tách tác động của hash ở cùng 2-way; so DAI–D0 khác cả associativity và mapping. Không dùng một điểm thắng để kết luận DAI thắng mọi workload. AMAT chỉ là ước tính theo ba miss penalty và ba giả định hit-time đã lưu trước benchmark, không gồm writeback stalls.", "",
              "## File kết quả và evidence", "",
              "- `all_runs.csv`: 96 dòng đầy đủ counter và phép so paired với D0; ô relative reduction trống nghĩa là N/A.",
              "- `scenario_summary.csv`: thống kê theo scenario/design; W4-random có mean/sample std/min/max và danh sách run IDs.",
              "- `amat_sensitivity.csv`: 864 dòng sensitivity theo giả định đã chốt.",
              "- `figures/`: PNG và PDF của miss rate và traffic, sinh từ raw results bằng script.",
              "- `runs/BATCH01/`: raw JSON, config, trace reference, run.log, batch.log và RUN_MANIFEST.csv.",
              "- `audit/AUDIT_LOG.jsonl`: mốc prepare/freeze/run/analysis với operator/executor và trạng thái.",
              "- `evidence/PRE_RUN_MANIFEST.json`: checksum và Git state trước run; `source_snapshot_before_runs.zip`: bản nguồn trước benchmark.",
              "- `traces/manifests/manifest.json`: 24 trace với tham số, seed và SHA-256.", ""]
    (out / "Ket_qua_thi_nghiem.md").write_text("\n".join(lines), encoding="utf-8")
    write_json(out / "analysis_summary.json", dict(status="SUCCESS", operator=OPERATOR, executor="Codex/Python",
               analyzed_runs=len(rows), scenarios=len(scenarios), summary_rows=len(summaries), amat_rows=len(amat), recorded_at=now()))
    audit("ANALYSIS_FINISHED", batch_id="BATCH01", status="SUCCESS", analyzed_runs=96, output="results/BATCH01")
    print("ANALYSIS SUCCESS", out)


if __name__ == "__main__": main()
