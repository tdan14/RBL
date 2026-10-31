# Simulator cache cho nghiên cứu Q10

Simulator Python đã triển khai D0, D1, D2 và DAI-v1 (B — XOR 2-way) theo protocol và thiết kế đã chốt. Mô hình một cấp cache dữ liệu, tag/valid/dirty, exact LRU, write-back/write-allocate; không mô phỏng nội dung word, timing CPU, prefetch hoặc bypass.

## Trạng thái

**BATCH01 đã hoàn tất:** 24 trace chính thức × 4 thiết kế = 96 run SUCCESS, 0 FAIL. Dân là người phụ trách/xác nhận theo chỉ định; Codex/Python trực tiếp thực thi. Xem [kết quả](results/BATCH01/Ket_qua_thi_nghiem.md), [evidence index](evidence/EVIDENCE_INDEX.md), [hướng dẫn tái lập](REPRODUCE.md) và [trace freeze](WORKLOAD_FREEZE.md).

- Đã có bốn config, lõi cache dùng chung, parser, runner và xuất JSON/JSONL.
- Bộ validation tự động trước batch có **28 test** (gồm generator và phép tính thống kê) và **20 phép đối chiếu** trên năm trace debug × bốn thiết kế, đều PASS trong lần chạy được ghi tại `validation/LATEST.txt`.
- Mô hình tham chiếu dùng full block ID và danh sách LRU, khác cách lưu tag nén/LRU bit/rank của implementation chính.
- Các kiểm tra tự động được AI hỗ trợ xây và chạy; người dùng đã xác nhận implementation và ủy quyền batch, được ghi trong `validation/IMPLEMENTATION_SIGNOFF.md`. Không gán tự động thành một review con người độc lập hoặc đối chiếu Ripes.
- Đã sinh, kiểm tra từng dòng, xác minh hash sinh lại và chốt 24 trace W1–W5 trước khi chạy. Đã chạy lại sáu result mẫu và một result từ bản sao nguồn giải nén sạch, đều khớp. Đây vẫn là cùng môi trường Python, chưa phải kiểm tra trên máy khác.

## Yêu cầu và cách chạy

Python 3.11 trở lên; không cần cài package ngoài. Chạy từ thư mục `C:\Tai_Lieu_Hoc\CEA201\RBL`.

Trong PowerShell, dùng Python hiện có trên máy:

```powershell
$simPython = 'C:\Users\Thinkpad\AppData\Local\Programs\Python\Python311\python.exe'
```

Chạy một ví dụ nhỏ DAI (chế độ debug, không phải official benchmark):

```powershell
& $simPython -m src.simulator.runner --config configs/DAI-v1.json --trace traces/debug/dirty.trace --warmup 0 --measure 4 --run-id DEBUG-DAI-dirty-demo --output validation/dirty_demo.json --events validation/dirty_demo.events.jsonl
```

Kết quả kỳ vọng: 4 access, 1 hit, 3 miss, 1 eviction, 1 dirty writeback, 3 line fills và traffic 128 B. Event cuối ghi trả base 2048, không phải 2080.

Chạy lại cùng tên output sẽ bị từ chối để không ghi đè kết quả cũ. Chọn tên output/events mới cho lượt khác. Thay config bằng `D0.json`, `D1.json` hoặc `D2.json` để chạy thiết kế khác; dùng cùng trace và cùng số access.

Chạy unit tests:

```powershell
& $simPython -m unittest discover -s tests -v
```

Tạo lại đầy đủ báo cáo validation và kết quả debug:

```powershell
& $simPython tools/validate_simulator.py
```

Mỗi lần validation tạo thư mục riêng trong `validation/`; `LATEST.txt` chỉ tới lần gần nhất. Báo cáo gồm `test_report.txt`, `summary.json`, 20 result JSON, 20 event JSONL và checksum của code/test/input/evidence. Không trộn chúng với kết quả benchmark chính thức.

## Định dạng trace

```text
# Comment và dòng trống được bỏ qua, không tính access.
R 0x00000000 4
W 2048 4
R 32 4  # Được phép comment cuối dòng.
```

OP phải viết hoa R/W; địa chỉ là số thập phân hoặc hex tiền tố `0x`; size phải bằng 4. Địa chỉ nguyên, chia hết cho 4, trong 0..0xFFFFFFFC. Dòng sai gây FAIL với số dòng; không âm thầm bỏ qua. Trace phải có đúng tổng số demand access được yêu cầu, không thiếu hoặc dư.

## Cách đọc kết quả

| Trường | Ý nghĩa |
|---|---|
| status | SUCCESS hoặc FAIL; chỉ tổng hợp các run SUCCESS |
| mode | debug hoặc official; validation hiện chỉ dùng debug |
| config | Snapshot đầy đủ, kể cả write policy và mapping |
| counters | Access, hit/miss, read/write miss, eviction, dirty writeback và fills trong khoảng đo |
| metrics | Hit/miss rate, memory traffic, metadata logic bytes |
| observed/requested | Số access khởi động và đo đã xử lý/yêu cầu |
| trace.sha256 | Hash input; kiểm tra lại sau khi đọc để phát hiện trace thay đổi lúc chạy |
| simulator | Phiên bản và fingerprint mã nguồn/config |
| protocol/design_freeze_sha256 | Nhận diện tài liệu nguồn dùng cho lượt chạy |
| metrics_validated | False nếu run FAIL; các số khi đó chỉ phục vụ debug |

Khi không có access đo, hit/miss rate là `null`. Không tự flush cuối run; dirty lines còn trong cache chưa tạo traffic ghi trả. Counter không gồm warmup; cache/dirty/LRU vẫn được giữ qua ranh warmup/measurement. JSONL events có cả warmup, được phân biệt bằng `measured`.

Runner mặc định warmup=10.000, measure=100.000 và mode=debug. Cờ `--mode official` chỉ kiểm tra kích thước khoảng đo chuẩn và yêu cầu trace ID; nó **không tự xác minh trace manifest đã được nhóm chốt hoặc validation đã được duyệt**. Batch chính thức dùng `tools/run_official_batch.py` để xác minh pre-run inputs và trace hashes trước chạy; 96 run đã được thực hiện theo cách đó.

Lõi không tính AMAT. Phân tích riêng tại `results/BATCH01/amat_sensitivity.csv` sử dụng counters và `analysis_plan.json` chốt trước benchmark. Thời gian chạy Python không phải latency phần cứng.

## Tổ chức mã nguồn

| Thành phần | Trách nhiệm |
|---|---|
| src/simulator/models.py | Config cố định, line state, counters và kiểm tra access |
| src/simulator/mapping.py | Tính index/tag và khôi phục block cho writeback |
| src/simulator/cache.py | Hit/miss, victim, dirty, exact LRU và invariants |
| src/simulator/trace.py | Đọc trace với lỗi có số dòng |
| src/simulator/runner.py | Khởi động/đo, nhận diện nguồn, xuất kết quả và CLI |
| configs/ | Bốn cấu hình theo thiết kế đã chốt |
| tests/ | Expected tests, input/runner tests và oracle biểu diễn khác |
| traces/debug/ | Năm trace nhỏ để kiểm tra |
| tools/validate_simulator.py | Tái tạo validation evidence |

Tham khảo [bảng kiểm tính tay](validation/manual_checks.md), [protocol](experiment_protocol.md), [thiết kế đã chốt](ai/AI_DESIGN_FREEZE.md) và [kế hoạch xây simulator](Ke_hoach_xay_simulator.md).

## Bước tiếp theo

Sử dụng raw results, bảng tổng hợp và evidence để viết Results/Discussion của báo cáo. DAI chỉ giảm miss so D0 ở W5 stress trong bộ input này; W1–W4 có miss rate bằng nhau. Giữ nguyên kết quả và giới hạn, không thay mapping hoặc layout để tạo lợi thế sau khi xem số liệu. Bộ bàn giao được đóng tại `delivery/Q10_BATCH01_evidence.zip`, với hash và receipt riêng; cách tái lập có trong `REPRODUCE.md`.
