# Kiểm tra bổ sung của AI sau P003

Mục đích: kiểm tra tính nhất quán của số học và expected result đã viết trong R001–R003, không lựa chọn candidate bằng benchmark. R001–R003 được giữ nguyên sau khi lưu; kết quả kiểm tra được ghi riêng ở đây.

Chạy tại thư mục `ai` bằng Node.js:

```text
node verification/check_q10_spec.mjs
```

Lần chạy của phiên Codex hiện tại hoàn tất với exit code 0 và 16 nhóm PASS; kết quả gốc lưu tại [AI_SELF_CHECK.json](AI_SELF_CHECK.json). Mốc ghi nhận lần chạy được lưu trong `../evidence/SESSION_TIMES.json` và nhật ký phiên. Có thể chạy lại để so nội dung JSON; script tự kiểm tra SHA-256 input/prompt gốc.

Phạm vi:

- Round-trip XOR/tag của A và B trên b=0..262.143 cộng ba probe biên cao cho mỗi phương án; không gọi đây là exhaustive toàn miền b 27 bit. Chứng minh đại số toàn miền nằm trong R001/R003.
- Kiểm tra địa chỉ writeback bằng công thức nghịch đảo, các nhóm block va chạm A/B/C, tag width và phép tính metadata.
- Kiểm tra expected của T01–T06, X01–X06 bằng một mô hình rất nhỏ dùng full block ID và danh sách LRU→MRU. Mô hình này biểu diễn recency khác với LRU bit của đặc tả, giúp đối chiếu kết quả tính tay nhưng không chứng minh code simulator tương lai đúng.
- Kiểm tra input/prompt gốc không đổi SHA-256.

Giới hạn: chưa kiểm tra implementation cache với tag nén/way vật lý/LRU bit, cơ chế reset toàn run của simulator nghiên cứu, payload dữ liệu, generator official W1–W5, D2 implementation, placement/insertion chi tiết của C, run manifests hoặc phần phân tích. Test T06 ở đây chỉ sinh một vòng buffer debug 1 KiB, không xác nhận generator nghiên cứu đã viết.

Đây là tự kiểm tra của cùng AI, không phải đánh giá độc lập. Chưa có official trace/run/benchmark. Không thay thế điều kiện protocol yêu cầu reviewer khác owner đối chiếu 3–5 trace và simulator vượt validation trước khi benchmark.
