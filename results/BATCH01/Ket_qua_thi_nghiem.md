# Kết quả official benchmark Q10 — BATCH01

Người phụ trách/xác nhận chạy: **Trương Tô Dân — QE210127**. Công cụ trực tiếp: Codex/Python. Thời điểm tổng hợp: 2026-10-31T16:03:29+07:00.

Đã thu đủ 96/96 run SUCCESS, 24 trace tổng hợp × 4 design. Mỗi run giữ nguyên 10.000 warmup + 100.000 access đo. Không dùng dữ liệu đo trạm cân thật.

## Bảng kết quả theo scenario

Miss rate tính theo %. W4-random là trung bình 10 seed; độ lệch chuẩn mẫu và từng seed có trong CSV. Các trường hợp deterministic không có mẫu lặp độc lập.

| Scenario | D0 (%) | D1 (%) | D2 (%) | DAI (%) | DAI − D0 (điểm %) | Traffic D0 / DAI (B) |
|---|---:|---:|---:|---:|---:|---:|
| W1-read | 12.50000 | 12.50000 | 12.50000 | 12.50000 | +0.00000 | 400000 / 400000 |
| W1-write | 12.50000 | 12.50000 | 12.50000 | 12.50000 | +0.00000 | 800000 / 800000 |
| W2-1024 | 0.00000 | 0.00000 | 0.00000 | 0.00000 | +0.00000 | 0 / 0 |
| W2-4096 | 0.00000 | 0.00000 | 0.00000 | 0.00000 | +0.00000 | 0 / 0 |
| W2-16384 | 12.50000 | 12.50000 | 12.50000 | 12.50000 | +0.00000 | 400000 / 400000 |
| W3-N8 | 1.38900 | 1.38900 | 1.38900 | 1.38900 | +0.00000 | 88896 / 88896 |
| W3-N32 | 0.37900 | 0.37900 | 0.37900 | 0.37900 | +0.00000 | 21376 / 21376 |
| W3-N128 | 0.09700 | 0.09700 | 0.09700 | 0.09700 | +0.00000 | 3104 / 3104 |
| W3-N512 | 0.02400 | 0.02400 | 0.02400 | 0.02400 | +0.00000 | 768 / 768 |
| W3-N2048 | 12.53700 | 12.53700 | 12.53700 | 12.53700 | +0.00000 | 402752 / 402752 |
| W4-even | 0.00000 | 0.00000 | 0.00000 | 0.00000 | +0.00000 | 0 / 0 |
| W4-random | 0.00000 | 0.00000 | 0.00000 | 0.00000 | +0.00000 | 0 / 0 |
| W5-K2 | 100.00000 | 0.00000 | 0.00000 | 0.00000 | -100.00000 | 3200000 / 0 |
| W5-K4 | 100.00000 | 100.00000 | 0.00000 | 0.00000 | -100.00000 | 3200000 / 0 |
| W5-K8 | 100.00000 | 100.00000 | 100.00000 | 0.00000 | -100.00000 | 3200000 / 0 |

## Nhận xét rút từ dữ liệu

- **W1-read:** miss rate DAI bằng so D0; D0=12.50000%, DAI=12.50000%, D1=12.50000%. Mức giảm tương đối so D0=0.00000%.
- **W1-write:** miss rate DAI bằng so D0; D0=12.50000%, DAI=12.50000%, D1=12.50000%. Mức giảm tương đối so D0=0.00000%.
- **W2-1024:** miss rate DAI bằng so D0; D0=0.00000%, DAI=0.00000%, D1=0.00000%. Relative reduction N/A vì D0=0.
- **W2-4096:** miss rate DAI bằng so D0; D0=0.00000%, DAI=0.00000%, D1=0.00000%. Relative reduction N/A vì D0=0.
- **W2-16384:** miss rate DAI bằng so D0; D0=12.50000%, DAI=12.50000%, D1=12.50000%. Mức giảm tương đối so D0=0.00000%.
- **W3-N8:** miss rate DAI bằng so D0; D0=1.38900%, DAI=1.38900%, D1=1.38900%. Mức giảm tương đối so D0=0.00000%.
- **W3-N32:** miss rate DAI bằng so D0; D0=0.37900%, DAI=0.37900%, D1=0.37900%. Mức giảm tương đối so D0=0.00000%.
- **W3-N128:** miss rate DAI bằng so D0; D0=0.09700%, DAI=0.09700%, D1=0.09700%. Mức giảm tương đối so D0=0.00000%.
- **W3-N512:** miss rate DAI bằng so D0; D0=0.02400%, DAI=0.02400%, D1=0.02400%. Mức giảm tương đối so D0=0.00000%.
- **W3-N2048:** miss rate DAI bằng so D0; D0=12.53700%, DAI=12.53700%, D1=12.53700%. Mức giảm tương đối so D0=0.00000%.
- **W4-even:** miss rate DAI bằng so D0; D0=0.00000%, DAI=0.00000%, D1=0.00000%. Relative reduction N/A vì D0=0.
- **W4-random:** miss rate DAI bằng so D0; D0=0.00000%, DAI=0.00000%, D1=0.00000%. Relative reduction N/A vì D0=0.
- **W5-K2:** miss rate DAI giảm so D0; D0=100.00000%, DAI=0.00000%, D1=0.00000%. Mức giảm tương đối so D0=100.00000%.
- **W5-K4:** miss rate DAI giảm so D0; D0=100.00000%, DAI=0.00000%, D1=100.00000%. Mức giảm tương đối so D0=100.00000%.
- **W5-K8:** miss rate DAI giảm so D0; D0=100.00000%, DAI=0.00000%, D1=100.00000%. Mức giảm tương đối so D0=100.00000%.

## Giới hạn và kết luận

Đây là kết quả mô phỏng của các trace đã chốt, không chứng minh hiệu năng/điện năng phần cứng hoặc tính tối ưu phổ quát. W5 là stress phù hợp cấu trúc XOR; không suy rộng lợi ích ở đây cho dữ liệu cân thực. W4 dùng bốn buffer liền nhau, tổng vừa cache; giữ nguyên layout và kết quả ngay cả khi không phân biệt thiết kế.

So DAI–D1 giúp tách tác động của hash ở cùng 2-way; so DAI–D0 khác cả associativity và mapping. Không dùng một điểm thắng để kết luận DAI thắng mọi workload. AMAT chỉ là ước tính theo ba miss penalty và ba giả định hit-time đã lưu trước benchmark, không gồm writeback stalls.

## File kết quả và evidence

- `all_runs.csv`: 96 dòng đầy đủ counter và phép so paired với D0; ô relative reduction trống nghĩa là N/A.
- `scenario_summary.csv`: thống kê theo scenario/design; W4-random có mean/sample std/min/max và danh sách run IDs.
- `amat_sensitivity.csv`: 864 dòng sensitivity theo giả định đã chốt.
- `figures/`: PNG và PDF của miss rate và traffic, sinh từ raw results bằng script.
- `runs/BATCH01/`: raw JSON, config, trace reference, run.log, batch.log và RUN_MANIFEST.csv.
- `audit/AUDIT_LOG.jsonl`: mốc prepare/freeze/run/analysis với operator/executor và trạng thái.
- `evidence/PRE_RUN_MANIFEST.json`: checksum và Git state trước run; `source_snapshot_before_runs.zip`: bản nguồn trước benchmark.
- `traces/manifests/manifest.json`: 24 trace với tham số, seed và SHA-256.
