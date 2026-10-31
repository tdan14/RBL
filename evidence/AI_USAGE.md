# Phạm vi bằng chứng sử dụng AI

Theo chỉ dẫn người dùng trong phiên chạy, không yêu cầu bổ sung bản xuất toàn bộ chat AI. Bộ evidence giữ nguyên P001–P003, R001–R003, `ai/AI_SESSION_LOG.md`, mốc thời gian/checksum hiện có và bản thiết kế đã chốt. Không gọi các file này là bản xuất toàn bộ lịch sử chat.

Trong giai đoạn official benchmark, người dùng xác nhận cho chạy, yêu cầu có log/evidence và chỉ định Dân là người thực hiện/phụ trách. Các trường evidence ghi:

- Operator/phụ trách và xác nhận: Trương Tô Dân — QE210127, theo chỉ định người dùng.
- Executor/công cụ trực tiếp tạo file, kiểm tra, sinh trace, chạy và phân tích: Codex/Python.
- Model ID cụ thể của phiên: không xác định từ dữ liệu có thể xác minh; không tự suy đoán.
- Không gán rằng Dân đã tự gõ từng lệnh hoặc AI là một reviewer con người độc lập.

Nguồn dữ liệu thí nghiệm là trace tổng hợp theo `workload_spec.md`; không có số đo từ trạm cân thật. Kết quả được tạo bởi simulator và lưu tại từng run; không dùng AI để điền hoặc sửa raw counters. Quyết định layout và giả định AMAT được lưu/chốt trước official runs. Sau khi có kết quả không thay mapping hoặc chọn lại trace để tạo lợi thế.

Audit ghi sự kiện chuẩn bị, kiểm tra trace, freeze, bắt đầu/kết thúc từng run và phân tích. Source snapshot trước run lưu cả công cụ sinh và phân tích có lúc đó; công cụ đóng gói/tái lập bổ sung sau run được phân biệt bằng tên file và checksum trong gói bàn giao cuối.
