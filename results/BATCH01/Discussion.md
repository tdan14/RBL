# Diễn giải kết quả BATCH01

Kết quả gốc cho thấy DAI-v1 không giảm miss rate ở W1–W4 trong bộ trace đã chốt; khác biệt có lợi so D0 chỉ xuất hiện ở W5. Kết luận phù hợp là **lợi ích phụ thuộc cấu trúc truy cập**, chưa có bằng chứng cải thiện cho mọi dòng dữ liệu cân.

## Giải thích theo workload

- **W1:** tám access 4 B trên mỗi line 32 B; stream một lượt tạo miss rate 12,5% cho mọi design. Ghi tuần tự có traffic 800.000 B so với 400.000 B khi đọc vì dirty eviction, dù miss rate giống nhau. Đây là lý do báo riêng traffic.
- **W2:** buffer 1/4 KiB giữ được sau warmup nên miss rate đo bằng 0; buffer 16 KiB là scan lớn hơn cache, miss rate 12,5% cho cả bốn design. Không coi 0% sau warmup là không hề có compulsory miss trong toàn trace.
- **W3:** thứ tự W mẫu mới rồi R từ mới về cũ tạo reuse cao ở cửa sổ nhỏ. Cửa sổ 2.048 mẫu vượt 4 KiB dữ liệu nên miss rate tăng trong trace này. Các design có cùng miss rate với base, thứ tự và prefix đã chọn. Chưa thử mọi căn chỉnh hoặc mọi bộ lọc.
- **W4:** bốn buffer liền nhau tổng 4 KiB, được warmup trước đo, làm cả 10 seed có miss rate bằng 0 và độ lệch chuẩn mẫu bằng 0. Điều đó phản ánh workload/config này, không chứng minh RNG không cần thiết ở mọi bài toán hoặc các sensor thực không có conflict. Không có lý do hợp lệ để đổi base sau khi đã xem kết quả.
- **W5:** D0 bị các block cách nhau 4 KiB tranh một line; DAI phân tán chúng, nên sau warmup D0 miss 100%, DAI 0%. D1 đủ cho K=2, D2 đủ cho K=2/4; chỉ K=8 phân biệt DAI với cả hai associative đối chứng. Stress được biết từ protocol và phù hợp cấu trúc XOR; kết quả không phải phát hiện AI có ưu thế phổ quát.

## Giới hạn của độ dài trace và giả định thời gian

Mọi trace đo 100.000 access, không phải cùng số mẫu cân. Một chu kỳ W3 có N+1 access. Với N=2.048, 110.000 access chỉ chứa 53 chu kỳ đầy đủ và một chu kỳ dở; khoảng khởi động 10.000 access cũng chỉ tương đương vài chu kỳ. Không tự tuyên bố đã đạt steady-state hoặc đại diện đầy đủ cho vận hành dài hạn. Trace v1.0 vẫn được giữ nguyên; nghiên cứu độ dài lớn hơn phải là thí nghiệm bổ sung có kế hoạch và phiên bản riêng, không thay raw batch này.

Khi giả định hit time DAI bằng các đối chứng, các trường hợp có cùng miss rate cũng có cùng AMAT ước tính. Khi giả định DAI tốn thêm 0,5 hoặc 1 cycle mỗi hit-path, nó có AMAT kém hơn D0 tại các W1–W4 có cùng miss rate. Ở W5, chênh lệch miss lớn vẫn có thể tạo lợi ích AMAT theo các penalty đã chọn. Đây là phép tính giả định; không có phép đo latency mạch hay năng lượng.

## Giá trị nghiên cứu và việc còn lại

Batch chứng minh một phép so có kiểm soát: cùng dung lượng dữ liệu, cùng trace, cùng khoảng đo, DAI được chốt trước benchmark, có cả các trường hợp không cải thiện. Đóng góp học phần nằm ở đánh giá có thể kiểm tra và chạy lại, không cần tuyên bố thuật toán mới hoặc AI bắt buộc thắng.

Tất cả claim số học phải dẫn về `all_runs.csv`, `scenario_summary.csv` và các run ID trong evidence index. Dữ liệu là tổng hợp, không thay thế đo trên chương trình/thiết bị trạm cân thật. Cần giữ giới hạn này khi viết Abstract, Results và Conclusion của báo cáo cuối.
