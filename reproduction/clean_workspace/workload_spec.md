# Đặc tả official workloads Q10 v1.0

Người phụ trách và xác nhận cho chạy: **Trương Tô Dân — QE210127**. Codex trực tiếp tạo file và thực thi theo ủy quyền trong cuộc trò chuyện. Các lựa chọn dưới đây được xác định trước khi chạy official benchmark, không lựa chọn theo kết quả thắng/thua. DAI-v1 và protocol không thay đổi.

## Quy tắc chung

24 trace; mỗi trace đúng 110.000 demand access gồm 10.000 warmup + 100.000 đo. Access R/W 4 B, địa chỉ unsigned 32-bit, căn chỉnh 4 B. Viết địa chỉ hex trong file, không comment giữa dữ liệu. Trace có thể kết thúc giữa một chu kỳ của generator; đây là cắt prefix theo số access, không phải cố tạo đủ số mẫu cân. Không có access khởi tạo ẩn hoặc truy cập phụ ngoài đặc tả.

## Bố trí và thao tác

| ID | Trường hợp | Base / vùng | Quy tắc sinh |
|---|---|---|---|
| W1-read / W1-write | 2 trace | 0x10000000; vùng dùng 440.000 B | Access i tại base+4i, i=0..109999, tất cả R hoặc tất cả W. Không quay vòng. |
| W2-1024/4096/16384 | 3 trace | 0x20000000; buffer tương ứng 1/4/16 KiB | Toàn R, địa chỉ base+4×(i mod (buffer_bytes/4)). |
| W3-N8/N32/N128/N512/N2048 | 5 trace | 0x30000000; ring 4.096 mẫu = 16 KiB | Mỗi chu kỳ t: W mẫu t mod 4096; sau đó R đúng N mẫu từ mới nhất về cũ nhất, có tính mẫu hiện tại. Địa chỉ R thứ j là base+4×((t−j) mod 4096), j=0..N−1. |
| W4-even | 1 trace | Sensor s=0..3: base 0x40000000+s×1024, mỗi buffer 1 KiB, liền nhau, không chồng lấn | Mỗi access ghi một mẫu vào sensor được chọn. Chọn luân phiên 0,1,2,3. Mỗi sensor có write pointer riêng, tăng 1 rồi wrap sau 256 mẫu. |
| W4-random-S01..S10 | 10 trace | Như W4-even | Chọn sensor bằng `random.Random(seed).randrange(4)` của Python, seed=1..10. Mỗi sensor có pointer riêng như trên. Mỗi lần chọn tạo đúng một W. Phiên bản Python được lưu. |
| W5-K2/K4/K8 | 3 trace | 0x50000000 + k×4096 | Toàn R; luân phiên block k=i mod K, K=2,4,8. Truy cập offset 0 của mỗi block. |

W3 giả định ring trong memory đã chứa lịch sử trước t=0; cache CPU bắt đầu rỗng. Chỉ mô phỏng địa chỉ, không có payload hoặc giá trị mẫu cân; đọc các chỉ số wrap biểu diễn mẫu lịch sử chứ không phải đọc trước mẫu tương lai. Số line thực sự chạm bởi cửa sổ phụ thuộc vị trí mẫu đầu/cuối, không chỉ N/8.

W4 chủ ý dùng bốn buffer liền nhau thành tổng 4 KiB, không cố đặt sensor cách nhau 4 KiB để tạo conflict nhân tạo. Mô hình này cô lập việc thu mẫu và interleaving, không thêm bộ lọc/log vào cùng trace; bộ lọc được kiểm tra ở W3. Nếu kết quả W4 không phân biệt thiết kế, vẫn giữ nguyên và báo cáo. Chỉ W5 được gắn nhãn conflict stress, không đại diện mọi trạm cân.

Base thuộc các vùng khác nhau nhằm dễ kiểm tra; mỗi trace chạy độc lập sau reset, không cộng working set của các trace khác nhau.

## Kiểm tra và chốt

Generator được test prefix, wrap-around, moving-average thứ tự và 10 seed. Trước freeze, toàn bộ trace được kiểm tra từng dòng bằng công thức theo số thứ tự access trong validator, kiểm tra R/W, range, căn chỉnh, số dòng và hash sinh lại; W5 kiểm tra index D0 giống nhau. Manifest lưu tham số, seed, counters R/W, range và SHA-256. Không chạy cache official để chọn trace.

`WORKLOAD_FREEZE.md` chỉ được tạo sau khi kiểm tra generator/trace đạt, với thời điểm thực tế. Mỗi run của bốn design dùng đúng file và SHA-256 trong manifest; không tạo file khác nhau theo cache.
