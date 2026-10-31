"""Validate and freeze official inputs, before any official cache result."""

from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.workloads import encoded_trace, scenarios, validate_trace
from src.simulator.trace import read_trace
from src.simulator.runner import sha256, source_identity

OPERATOR = "Trương Tô Dân — QE210127"


def now():
    return datetime.now(timezone(timedelta(hours=7))).isoformat(timespec="seconds")


def write_json(path, data):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2); f.write("\n")


def audit(action, **fields):
    path = ROOT / "audit/AUDIT_LOG.jsonl"; path.parent.mkdir(exist_ok=True)
    entry = dict(timestamp=now(), operator=OPERATOR, executor="Codex / Python", action=action, **fields)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main():
    if (ROOT / "WORKLOAD_FREEZE.md").exists():
        raise RuntimeError("Freeze already exists; do not overwrite frozen inputs")
    latest = (ROOT / "validation/LATEST.txt").read_text().strip()
    validation = json.loads((ROOT / "validation" / latest / "summary.json").read_text(encoding="utf-8"))
    if validation["status"] != "PASS":
        raise RuntimeError("Validation must pass before freeze")
    if validation["source"]["source_sha256"] != source_identity()["source_sha256"]:
        raise RuntimeError("Validation fingerprint differs from current source")
    audit("PREPARATION_STARTED", validation=latest, status="STARTED")
    manifest = []
    for spec in scenarios():
        path = ROOT / "traces/official" / (spec["trace_id"] + ".trace")
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as f:
            for row in encoded_trace(spec): f.write(row)
        stats = validate_trace(spec, read_trace(path))
        replay = hashlib.sha256()
        for row in encoded_trace(spec): replay.update(row)
        digest = sha256(path)
        if digest != replay.hexdigest(): raise AssertionError("Generator replay hash mismatch")
        item = {**spec, **stats, "path": path.relative_to(ROOT).as_posix(), "sha256": digest, "bytes": path.stat().st_size}
        manifest.append(item)
        audit("TRACE_VALIDATED", trace_id=spec["trace_id"], sha256=digest, status="PASS")
        print("TRACE PASS", spec["trace_id"], flush=True)
    write_json(ROOT / "traces/manifests/manifest.json", {
        "created_at": now(), "operator": OPERATOR, "executor": "Codex / Python",
        "python": platform.python_version(), "count": len(manifest), "traces": manifest,
        "generator_sha256": sha256(ROOT / "src/workloads.py"),
        "simulator": source_identity(), "workload_spec_sha256": sha256(ROOT / "workload_spec.md"),
        "analysis_plan_sha256": sha256(ROOT / "analysis_plan.json"),
        "validation_summary": f"validation/{latest}/summary.json"
    })
    signoff = ("# Xác nhận implementation trước official benchmark\n\n"
               f"Người xác nhận/phụ trách: **{OPERATOR}**.\n\n"
               f"Mốc ghi nhận: {now()}. Người dùng đã xác nhận và ủy quyền bắt đầu chạy trong cuộc trò chuyện. "
               "Đây là ghi nhận xác nhận đó, không tự mô tả một buổi review thủ công mới do AI thực hiện.\n\n"
               f"Validation tự động mới nhất: `{latest}`; {validation['unit_tests']} test và "
               f"{validation['comparison_count']} đối chiếu đạt. Generator/trace được kiểm tra từng dòng và hash sinh lại trước freeze. "
               "Codex/Python là công cụ trực tiếp thực thi. Chưa có official result tại thời điểm chốt input.\n")
    (ROOT / "validation/IMPLEMENTATION_SIGNOFF.md").write_text(signoff, encoding="utf-8")
    freeze = ("# Chốt official traces Q10 v1.0\n\n**Trạng thái: ĐÃ CHỐT INPUT TRƯỚC OFFICIAL BENCHMARK.**\n\n"
              f"Thời điểm: {now()}. Người phụ trách/xác nhận cho chạy: {OPERATOR}. Công cụ: Codex/Python.\n\n"
              "24 trace × 110.000 access; cùng 10.000 warmup + 100.000 đo cho bốn design, dự kiến 96 run. "
              "Bố trí, thao tác, seed và giới hạn theo `workload_spec.md`. Không chọn layout theo kết quả cache.\n\n"
              f"Manifest SHA-256: `{sha256(ROOT / 'traces/manifests/manifest.json')}`.\n\n"
              f"Source fingerprint: `{source_identity()['source_sha256']}`.\n\n"
              f"Analysis plan SHA-256: `{sha256(ROOT / 'analysis_plan.json')}`.\n\n"
              "Tất cả trace pass validator theo số thứ tự access, range/alignment, R/W, số dòng, W5 collision và replay hash. "
              "W3 có thể kết thúc giữa chu kỳ; ring lịch sử trong memory được giả định tồn tại trước t=0. "
              "W4 dùng buffer liền nhau đúng 4 KiB tổng cộng. W5 là stress có cấu trúc. Không đổi các quyết định này sau khi xem official results.\n")
    with (ROOT / "WORKLOAD_FREEZE.md").open("x", encoding="utf-8") as f: f.write(freeze)
    inputs = list((ROOT / "src").rglob("*.py")) + list((ROOT / "tests").glob("*.py")) + list((ROOT / "tools").glob("*.py"))
    inputs += list((ROOT / "configs").glob("*.json"))
    inputs += list((ROOT / "ai").rglob("*.md"))
    inputs += [ROOT / "ai/evidence/SESSION_TIMES.json", ROOT / "ai/evidence/SHA256SUMS.json"]
    inputs += [ROOT / p for p in ["experiment_protocol.md", "ai/inputs/experiment_protocol.md", "ai/AI_DESIGN_FREEZE.md", "workload_spec.md", "analysis_plan.json", "WORKLOAD_FREEZE.md", "traces/manifests/manifest.json", "validation/IMPLEMENTATION_SIGNOFF.md", f"validation/{latest}/summary.json", f"validation/{latest}/test_report.txt"]]
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        git_status = subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True)
    except (OSError, subprocess.CalledProcessError): commit, git_status = None, "unavailable"
    files = {p.relative_to(ROOT).as_posix(): sha256(p) for p in sorted(set(inputs))}
    write_json(ROOT / "evidence/PRE_RUN_MANIFEST.json", dict(created_at=now(), operator=OPERATOR,
               executor="Codex / Python", git_head=commit, git_status=git_status, files=files,
               note="Uncommitted tool/workload changes included in source snapshot and SHA-256, not misrepresented as committed"))
    with zipfile.ZipFile(ROOT / "evidence/source_snapshot_before_runs.zip", "x", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(set(inputs)): z.write(p, p.relative_to(ROOT))
    audit("INPUTS_FROZEN", status="SUCCESS", trace_count=24, planned_runs=96,
          manifest_sha256=sha256(ROOT / "traces/manifests/manifest.json"), pre_run_sha256=sha256(ROOT / "evidence/PRE_RUN_MANIFEST.json"))
    print("FROZEN 24 traces; no official cache runs executed by prepare", flush=True)


if __name__ == "__main__": main()
