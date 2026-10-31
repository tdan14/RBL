# Evidence index Q10 — BATCH01

Người thực hiện/phụ trách và xác nhận theo chỉ định: **Trương Tô Dân — QE210127**. Công cụ trực tiếp: **Codex/Python**. Tất cả mốc giờ dùng UTC+07:00. Không gán các thao tác tự động thành thao tác thủ công của Dân.

| ID | Evidence | Vị trí | Chứng minh |
|---|---|---|---|
| E-001 | Protocol | experiment_protocol.md; ai/inputs/experiment_protocol.md | Cấu hình, metric, warmup/đo và số run |
| E-002 | AI prompt/response và log hiện có | ai/prompts/; ai/responses/; ai/AI_SESSION_LOG.md; ai/evidence/ | AI đã đề xuất ba phương án, phản biện và chọn B |
| E-003 | Chốt thiết kế | ai/AI_DESIGN_FREEZE.md | DAI-v1 được chốt trước khi triển khai và official benchmark |
| E-004 | Mã nguồn/config trước run | evidence/source_snapshot_before_runs.zip; evidence/PRE_RUN_MANIFEST.json | Nguồn dùng tạo số liệu, fingerprint, Git HEAD và trạng thái uncommitted được khai báo |
| E-005 | Validation | validation/IMPLEMENTATION_SIGNOFF.md; thư mục validation được ghi trong trace manifest | Xác nhận người dùng, 28 test tự động và 20 đối chiếu trước freeze trace |
| E-006 | Đặc tả và freeze trace | workload_spec.md; WORKLOAD_FREEZE.md | Layout và quy tắc được quyết định trước kết quả, 24 trace × 110.000 access |
| E-007 | Input chính thức | traces/official/; traces/manifests/manifest.json | Trace, tham số, seed, R/W, range và SHA-256 |
| E-008 | Kế hoạch phân tích | analysis_plan.json | Metric chính, zero baseline, thống kê seed và latency sensitivity chốt trước run |
| E-009 | 96 kết quả gốc | runs/BATCH01/RUN-000001..RUN-000096/result.json | Counter/metric, config, trace hash, nguồn, thời gian, operator/executor và SUCCESS/FAIL |
| E-010 | Log và manifest run | runs/BATCH01/batch.log; RUN_MANIFEST.csv; từng run.log/config.json/trace_reference.json | Mốc start/end, ánh xạ run–trace–design và hash kết quả; giữ cả lỗi nếu xảy ra |
| E-011 | Audit | audit/AUDIT_LOG.jsonl | Chuỗi prepare → trace validation → freeze → 96 run → analysis → reproduction |
| E-012 | Dữ liệu xử lý và hình | results/BATCH01/ | 96 dòng raw-summary, 60 dòng scenario/design, 864 dòng AMAT; PNG/PDF sinh bằng script |
| E-013 | Tái lập mẫu | reproduction/summary.json; replay_*.json | Sáu run tái chạy khớp trong cùng môi trường, không tính là mẫu độc lập |
| E-014 | Kiểm tra bản sao sạch | reproduction/clean_copy_check.json; clean_copy_RUN-000040.json | Một run khớp sau giải nén source snapshot vào workspace mới; cùng Python, chưa phải máy khác |
| E-015 | Hướng dẫn và môi trường | REPRODUCE.md; evidence/ENVIRONMENT.json | Cách chạy lại generator, simulator, validation và analysis |
| E-016 | Phạm vi AI | evidence/AI_USAGE.md | Không bịa model ID hoặc coi log hiện có là bản xuất toàn bộ chat; người dùng không yêu cầu bổ sung export |
| E-017 | Kiểm tra integrity cuối | evidence/FINAL_CHECKSUMS.json; evidence/FINAL_VERIFICATION.json | Hash toàn bộ file bàn giao, 96 run đủ, trace/result bất biến |

## Các giới hạn giữ nguyên trong báo cáo

- Trace là dữ liệu tổng hợp theo mô hình, không phải dữ liệu thu từ trạm cân thật.
- Người dùng đã xác nhận implementation và cho chạy; validator/generator/test và phép đối chiếu tự động được AI hỗ trợ, không tự gán là review con người độc lập hoặc Ripes.
- Batch có 96 SUCCESS và 0 FAIL nếu đúng theo summary gốc; không được tự sửa trạng thái khi soạn báo cáo. Nếu batch khác có lỗi, giữ file và ghi invalid/run thay thế bằng ID mới.
- Source Git HEAD là mốc có trước; các file sinh workload/công cụ mới chưa commit được lưu bằng snapshot và hash, không gán giả một commit đã bao gồm chúng.
- W4 đã chọn buffer liền nhau vừa cache, W5 là conflict stress. DAI không cải thiện miss ở W1–W4 trong bộ input này. Không đổi layout sau khi đã xem kết quả để làm DAI thắng.
- Không suy ra timing/energy phần cứng từ AMAT giả định. Thời gian chạy chương trình chỉ là log thực thi.

## Claim–evidence

| Claim | Kết luận trong phạm vi dữ liệu | Run liên quan | Evidence |
|---|---|---|---|
| C-001 | W1 đọc/ghi: mọi design miss 12,5% | RUN-000001–000008 | E-007, E-009, E-012 |
| C-002 | W2: 1/4 KiB miss 0% sau warmup; 16 KiB miss 12,5%, mọi design bằng nhau | RUN-000009–000020 | E-007, E-009, E-012 |
| C-003 | Năm W3: miss rate DAI bằng D0/D1/D2 với layout và thứ tự đọc đã chốt | RUN-000021–000040 | E-006, E-007, E-009, E-012 |
| C-004 | W4 đều và 10 seed ngẫu nhiên: mọi design miss 0% trong khoảng đo | RUN-000041–000084 | E-006, E-007, E-009, E-012 |
| C-005 | W5 K=2/4/8: D0 miss 100%, DAI miss 0% sau warmup | RUN-000085–000096 | E-006, E-007, E-009, E-012 |
| C-006 | 96 result đủ, không có run lỗi; sáu replay mẫu khớp | Toàn bộ BATCH01 và sáu replay được liệt kê | E-009, E-010, E-013 |
| C-007 | Chưa chứng minh tăng tốc hoặc tiết kiệm điện trên phần cứng | Không có phép đo phần cứng | E-001, E-008, E-016 |

Hash manifest cuối không tự chứa hash chính nó. SHA-256 gói ZIP được ghi trong receipt riêng ngoài ZIP để tránh tham chiếu vòng. Dùng checksum để kiểm tra file không thay đổi, không xem checksum là bằng chứng rằng một kết luận khoa học tự động đúng.
