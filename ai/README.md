# Lưu prompt và bằng chứng thiết kế AI cho Q10

## Cấu trúc

```text
ai/
├── inputs/
│   ├── experiment_protocol.md
│   └── Tong_hop_9_bai_bao_tham_khao_Q10.md
├── prompts/
│   ├── P001.md
│   ├── P002.md
│   └── P003.md
├── responses/
│   ├── R001.md
│   ├── R002.md
│   └── R003.md
├── AI_SESSION_LOG.md
├── AI_DESIGN_FREEZE.md
├── evidence/
│   ├── SESSION_TIMES.json
│   └── SHA256SUMS.json
├── verification/
│   ├── check_q10_spec.mjs
│   ├── AI_SELF_CHECK.json
│   └── README.md
└── README.md
```

## Kết quả phiên thực hiện 31/10/2026

Codex đã đọc trực tiếp hai file trong `inputs/` và thực hiện P001 → P002 → P003 theo yêu cầu người dùng, lưu câu trả lời trước khi chuyển bước. Không có ba lượt gửi prompt riêng qua một dịch vụ AI khác; cách thực hiện và thời gian quan sát được ghi trong [AI_SESSION_LOG.md](AI_SESSION_LOG.md).

| Bước | Câu trả lời đã lưu | Nội dung |
|---|---|---|
| [P001](prompts/P001.md) | [R001](responses/R001.md) | Đúng ba phương án: A XOR direct-mapped, B XOR 2-way, C skewed 2-bank; chưa chọn cuối |
| [P002](prompts/P002.md) | [R002](responses/R002.md) | Tự phản biện cùng AI; kiểm tra capacity, tag/index, dirty/LRU, metadata và phản ví dụ; chưa chọn cuối |
| [P003](prompts/P003.md) | [R003](responses/R003.md) | Đề xuất chọn B cho DAI-v1; đặc tả đầy đủ, pseudocode và expected result tính tay |

P001–P003 và hai input giữ nguyên. R001–R003 là nội dung trả lời gốc được soạn trực tiếp vào file; không chỉnh lại các response sau khi chuyển bước. Chưa có lượt làm rõ riêng.

[AI_DESIGN_FREEZE.md](AI_DESIGN_FREEZE.md) đã chuyển sang **đã chốt XOR 2-way**, theo xác nhận trực tiếp của người dùng rằng đã kiểm tra và đồng ý, với Trương Tô Dân là người kiểm tra và xác nhận. Mốc ghi nhận: 2026-10-31T15:33:41+07:00. Chưa có simulator nghiên cứu/validation report được xác nhận và chưa chạy official benchmark.

Kiểm tra bổ sung của cùng AI có 16 nhóm PASS; xem [phạm vi và giới hạn](verification/README.md), [script tái chạy](verification/check_q10_spec.mjs) và [kết quả JSON](verification/AI_SELF_CHECK.json). Đây là kiểm tra số học/trace debug, không thay validation độc lập. [SHA-256 manifest](evidence/SHA256SUMS.json) lưu checksum các artefact sau khi soạn xong; manifest không tự hash chính nó.

## Bước tiếp theo theo protocol

1. Triển khai simulator D0/D1/D2/DAI-v1 theo [kế hoạch xây simulator](C:/Tai_Lieu_Hoc/CEA201/RBL/Ke_hoach_xay_simulator.md).
2. Kiểm tra T01–T06 và test riêng DAI; đối chiếu độc lập và lập validation report cho simulator.
3. Hoàn thiện workload specification/manifests, analysis plan và môi trường trước official runs; không chọn base/hash bằng kết quả thắng/thua.

Giữ các bản input đã sử dụng làm bằng chứng. Nếu cập nhật tài liệu cho một lượt sau, lưu phiên bản mới và ghi rõ trong log; không ghi đè bằng chứng đầu vào cũ.
