# Simulator cache cho nghiên cứu Q10

Simulator Python đã triển khai D0, D1, D2 và DAI-v1 (B — XOR 2-way) theo protocol và thiết kế đã chốt. Mô hình một cấp cache dữ liệu, tag/valid/dirty, exact LRU, write-back/write-allocate; không mô phỏng nội dung word, timing CPU, prefetch hoặc bypass.

## Trạng thái

- Đã có bốn config, lõi cache dùng chung, parser, runner và xuất JSON/JSONL.
- Bộ validation tự động hiện có **21 test** và **20 phép đối chiếu** trên năm trace debug × bốn thiết kế, đều PASS trong lần chạy được ghi tại `validation/LATEST.txt`.
- Mô hình tham chiếu dùng full block ID và danh sách LRU, khác cách lưu tag nén/LRU bit/rank của implementation chính.
- Các kiểm tra được AI hỗ trợ xây và chạy, chưa phải xác nhận kiểm tra implementation của thành viên nhóm hoặc đối chiếu Ripes.
- Chưa tạo official traces W1–W5, chưa chạy 96 run benchmark chính thức và chưa có kết quả về hiệu quả của DAI trên workload chính thức.

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

Runner mặc định warmup=10.000, measure=100.000 và mode=debug. Cờ `--mode official` chỉ kiểm tra kích thước khoảng đo chuẩn và yêu cầu trace ID; nó **không tự xác minh trace manifest đã được nhóm chốt hoặc validation đã được duyệt**. Chỉ sử dụng khi đã hoàn tất các điều kiện protocol. Chưa có lượt official được chạy trong giai đoạn triển khai này.

Không tính AMAT trong lõi hiện tại để tránh đưa giả định latency chưa chốt vào kết quả. Phần phân tích sau sẽ sử dụng counters, miss rate và analysis plan đã hoàn thiện. Thời gian chạy Python không phải latency phần cứng.

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

Thành viên nhóm đối chiếu implementation và 3–5 trace nhỏ bằng bảng kiểm. Sau đó hoàn thiện bố trí địa chỉ, thứ tự thao tác W3/W4, generator/manifests và analysis plan. Chốt official traces/checksum trước khi thực hiện ma trận 96 run. Không thay hàm mapping của DAI-v1 sau khi xem kết quả chính thức.
