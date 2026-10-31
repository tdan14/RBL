# Chốt official traces Q10 v1.0

**Trạng thái: ĐÃ CHỐT INPUT TRƯỚC OFFICIAL BENCHMARK.**

Thời điểm: 2026-10-31T16:00:53+07:00. Người phụ trách/xác nhận cho chạy: Trương Tô Dân — QE210127. Công cụ: Codex/Python.

24 trace × 110.000 access; cùng 10.000 warmup + 100.000 đo cho bốn design, dự kiến 96 run. Bố trí, thao tác, seed và giới hạn theo `workload_spec.md`. Không chọn layout theo kết quả cache.

Manifest SHA-256: `b82833a27b13ddb6519f6109fb4e2261f2a8be036c74221a3fef495ee1a2f263`.

Source fingerprint: `e8f6f82a4531d9b59e9ccd63b8291d3be43a9f4002b16674cfdceb195a3d2c86`.

Analysis plan SHA-256: `7b1c8baed879e737e9607f771869be893bdda4daec6d7508039a50f75edf4a2f`.

Tất cả trace pass validator theo số thứ tự access, range/alignment, R/W, số dòng, W5 collision và replay hash. W3 có thể kết thúc giữa chu kỳ; ring lịch sử trong memory được giả định tồn tại trước t=0. W4 dùng buffer liền nhau đúng 4 KiB tổng cộng. W5 là stress có cấu trúc. Không đổi các quyết định này sau khi xem official results.
