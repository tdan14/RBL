# Hướng dẫn tái lập Q10 BATCH01

## Thành phần phải giữ cùng nhau

Giữ mã trong `src/`, công cụ trong `tools/`, `tests/`, bốn config, `traces/official/`, trace manifest, protocol, workload spec, analysis plan và design freeze. Raw results/log trong `runs/BATCH01/` là bằng chứng gốc, không ghi đè khi chạy lại. Evidence chứa nguồn trước benchmark, checksums, log AI hiện có và audit.

Simulator và generator dùng Python standard library. Phiên bản Python được ghi trong từng result/manifest. Matplotlib và NumPy chỉ dùng để tạo hình ở bước analysis; phiên bản thực tế được lưu trong evidence môi trường cuối. Không cần chúng để tái lập counters của một run.

## Chạy lại một kết quả

Từ thư mục gốc dự án, trong PowerShell:

```powershell
$simPython = 'C:\Users\Thinkpad\AppData\Local\Programs\Python\Python311\python.exe'
& $simPython tools/reproduce_run.py --run-id RUN-000040 --output reproduction/replay_RUN-000040.json
```

Trên máy khác, thay đường dẫn Python bằng Python 3.11 phù hợp. Đầu ra phải là `MATCH`, với `reproduction.matches_original=true`. So counters, metrics, config, observed periods và hash trace. Thời gian, run ID và đường dẫn tuyệt đối thay đổi giữa máy/lượt nên không đòi SHA của toàn JSON mới giống JSON cũ.

Có thể chạy lại mọi ID RUN-000001..RUN-000096 vào output mới. Replay được gắn nhãn debug, không phải mẫu độc lập mới hoặc thay thế raw result gốc. Trace reference dùng đường dẫn tương đối theo gốc dự án để chuyển máy; các đường dẫn tuyệt đối trong raw JSON chỉ mô tả máy đã chạy lần đầu.

## Kiểm tra lại generator mà không đổi input

```powershell
& $simPython -c "from pathlib import Path; import hashlib,json; from src.workloads import encoded_trace; m=json.loads(Path('traces/manifests/manifest.json').read_text(encoding='utf-8')); checks=[hashlib.sha256(b''.join(encoded_trace(t))).hexdigest()==t['sha256'] for t in m['traces']]; print(checks); assert all(checks)"
```

Lệnh sinh lại bytes trong bộ nhớ và so hash, không ghi đè trace. Với W4 random, phiên bản/thuật toán RNG được ghi trong đặc tả và manifest; nếu khác môi trường, dùng chính trace đã đóng gói để kiểm tra simulator, rồi điều tra riêng sai khác generator.

## Chạy lại validation

```powershell
& $simPython tools/validate_simulator.py
```

Tạo thư mục validation mới. Không thay hoặc xóa báo cáo trước benchmark. Lần validation này có thể thay `validation/LATEST.txt`; snapshot trước run vẫn giữ đường dẫn và hash của báo cáo dùng lúc chốt.

## Tạo lại bảng và hình

Script `tools/analyze_experiments.py` đọc 96 raw JSON qua manifest và kiểm tra hash trước khi phân tích. Nó từ chối ghi đè `results/BATCH01/`. Để chạy lại, giải nén/copy dự án sang thư mục làm việc mới và giữ thư mục kết quả bàn giao ở nơi khác; không xóa raw evidence gốc. Chạy:

```powershell
& $simPython tools/analyze_experiments.py
```

Kết quả phải có 96 dòng all_runs, 60 dòng scenario/design summary và 864 dòng AMAT sensitivity. So các giá trị số; hình/PDF có thể khác bytes metadata giữa môi trường. File analysis plan đã chốt quy tắc zero baseline, seed summary và giả định latency.

## Chạy lại toàn bộ ma trận

Trong một bản sao làm việc mới không chứa `runs/BATCH01/`, nhưng có đủ trace, manifest và pre-run source inputs, chạy `tools/run_official_batch.py`. Script kiểm tra input đã chốt, không đổi thiết kế hoặc sinh lại input và từ chối ghi đè batch cũ. Việc này tạo một phép tái lập cùng thí nghiệm; không được tính thành thêm 96 mẫu độc lập.

## Phạm vi bằng chứng

Người phụ trách/xác nhận theo chỉ định: Trương Tô Dân — QE210127. Công cụ trực tiếp: Codex/Python. Lịch sử AI lưu theo phạm vi tại `evidence/AI_USAGE.md`; không có bản xuất toàn bộ chat, theo lựa chọn người dùng. Không có số đo trạm cân thật hoặc phép đo hardware timing/energy. Những giới hạn này phải được giữ khi đưa kết quả vào report.
