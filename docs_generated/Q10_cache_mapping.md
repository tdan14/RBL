# Q10: cache mapping cho dòng dữ liệu trạm cân

Tài liệu này mô tả cấu trúc và bằng chứng hiện có trong repo. Nó không báo cáo kết quả official benchmark.

## Mục lục

- [Bối cảnh truy cập dữ liệu](#bối-cảnh-truy-cập-dữ-liệu)
- [Các thiết kế và DAI-v1](#các-thiết-kế-và-dai-v1)
- [So sánh cấu trúc](#so-sánh-cấu-trúc)
- [Ví dụ tính tay và validation debug](#ví-dụ-tính-tay-và-validation-debug)
- [Giả định và giới hạn](#giả-định-và-giới-hạn)
- [Minh chứng AI và design freeze](#minh-chứng-ai-và-design-freeze)
- [Trạng thái kết quả](#trạng-thái-kết-quả)

## Bối cảnh truy cập dữ liệu

Q10 dùng simulator Python trace-driven cho cache dữ liệu một cấp. Một trace tối thiểu chứa operation `R/W`, địa chỉ và kích thước access; nó mô tả truy cập bộ nhớ trong mô hình trạm cân, không phải dữ liệu đo trực tiếp từ thiết bị thật. Mọi thiết kế giữ 4 KiB data capacity, cache line 32 B, địa chỉ logic 32-bit không dấu và access 4 B căn chỉnh 4 byte.

| Workload | Đặc điểm truy cập đã đặc tả | Mục tiêu |
|---|---|---|
| W1 | Đọc tuần tự và ghi tuần tự. | Kiểm tra spatial locality và stream. |
| W2 | Circular buffer 1 KiB, 4 KiB, 16 KiB. | Kiểm tra reuse khi working set nhỏ, bằng hoặc lớn hơn cache. |
| W3 | Moving average với cửa sổ 8, 32, 128, 512, 2.048 mẫu; một mẫu 4 B. | Kiểm tra ảnh hưởng window và working set. |
| W4 | Bốn buffer sensor 1 KiB; xen kẽ đều hoặc ngẫu nhiên. | Kiểm tra tương tác giữa các stream. |
| W5 | Luân phiên 2, 4, 8 block cách nhau 4 KiB. | Tạo conflict có kiểm soát ở D0. |

W4 là chuỗi access tuần tự có kiểm soát. Protocol nêu rõ W4 không tự được coi là mô phỏng CPU multicore, coherence hoặc thực thi đồng thời. Các base address, thứ tự đọc/ghi chi tiết, generator và manifest official của W3/W4 vẫn cần hoàn thiện trước official runs.

Nguồn: `experiment_protocol.md` §2–5; `Ke_hoach_RBL_Q10_AI_Cache_Mapping.docx` §4, §7.

## Các thiết kế và DAI-v1

### D0, D1, D2

Với các baseline modulo, `b = address >> 5`; `index = b % sets`; `tag = b // sets`. D0 là direct mapping bắt buộc; D1 và D2 tách ảnh hưởng của associativity.

### Ba phương án A/B/C

| Phương án | Tổ chức đề xuất trong R001 | Trạng thái lựa chọn |
|---|---|---|
| A | XOR direct-mapped tĩnh, 128 set × 1 way. | Không chọn; chỉ có một vị trí cho mỗi block. |
| B | XOR set-associative tĩnh, 64 set × 2 way và exact LRU. | Được chọn, freeze thành DAI-v1. |
| C | Skewed tĩnh, 2 bank × 64 slot với cặp vị trí hợp lệ. | Không chọn; R003 nêu đặc tả/debug phức tạp hơn và metadata theo R001 cao hơn. |

R002 là tự phản biện của cùng Codex, không phải đánh giá độc lập. R003 chọn B dựa trên tính khả thi và khả năng kiểm chứng, không dựa vào benchmark.

Nguồn: `ai/responses/R001.md` §2–6; `ai/responses/R002.md` §2–6; `ai/responses/R003.md` §1.

### DAI-v1: XOR 2-way

DAI-v1 giữ 4 KiB dữ liệu với 64 set × 2 way; replacement là exact LRU, write policy là write-back + write-allocate, prefetch và bypass đều tắt.

```text
b     = address >> 5
index = (b ^ (b >> 6)) & 63
tag   = b >> 6

recover_block(index, tag) =
    (tag << 6) | (index ^ (tag & 63))
```

Một block chỉ lookup ở hai way của `index`. `recover_block` cần dùng khi ghi trả victim: dùng công thức modulo của D1 cho DAI-v1 sẽ lấy sai địa chỉ ở một số block. Trong code, two-way LRU dùng một `lru_way` cho mỗi set; khi chạm way `w`, way `1 - w` thành LRU.

Lý do chọn B trong design freeze là nó dùng tổ chức 2-way tương tự D1, không cần học online hay quản lý cặp slot chồng lấn như C, đồng thời có index/tag/writeback xác định được. Điều này không cam kết DAI-v1 thắng D0 hoặc D1.

Nguồn: `ai/AI_DESIGN_FREEZE.md` §Cấu hình, §Hàm khôi phục, §Lý do lựa chọn; `src/simulator/mapping.py`; `src/simulator/cache.py`.

## So sánh cấu trúc

| Thiết kế | Set × way | Mapping | Replacement | Metadata logic | Complexity lookup/mapping |
|---|---:|---|---|---:|---|
| D0 | 128 × 1 | Modulo | Vị trí duy nhất | 352 B | So 1 tag; `index = block % 128`. |
| D1 | 64 × 2 | Modulo | Exact LRU 2-way | 376 B | So tối đa 2 tag; một bit LRU/set. |
| D2 | 32 × 4 | Modulo | Exact LRU 4-way | 416 B | So tối đa 4 tag; rank 2 bit/way. |
| DAI-v1 | 64 × 2 | XOR | Exact LRU 2-way | 376 B | So tối đa 2 tag; XOR index và inverse mapping khi writeback. |

Metadata gồm tag, valid/dirty và replacement state; không gồm ECC, comparator, control logic, dây dẫn hay Python object overhead. DAI-v1 và D1 có cùng metadata logic theo đặc tả, nhưng DAI-v1 có thêm logic XOR/inverse mapping. So sánh DAI-v1 với D1 giúp quan sát mapping dưới cùng 64 set × 2 way; so với D0 hoặc D2 đồng thời thay đổi associativity.

Nguồn: `ai/AI_DESIGN_FREEZE.md` §Chi phí và phép so công bằng; `src/simulator/models.py`; `src/simulator/cache.py`; `configs/`.

## Ví dụ tính tay và validation debug

Năm trace trong `traces/debug/` là input debug, không phải W1–W5 official. `validation/manual_checks.md` ghi kết quả kỳ vọng trên D0/D1/D2/DAI-v1; summary mới nhất báo 21 unit test và 20 đối chiếu debug PASS, đồng thời ghi rõ không có human sign-off, Ripes, W1–W5 official trace hay benchmark.

| Trace debug | Chuỗi access | DAI-v1 | Có phân biệt DAI với D1? |
|---|---|---|---|
| `repeat` | `R0, R0` | `MH` | Không; cả hai đều miss rồi hit. |
| `boundary` | `R28, R32, R28` | `MMH` | Không; hai block có vị trí riêng ở cả bốn thiết kế. |
| `lru` | `R0, R2080, R0, R4160, R2080` | `MMHMM` | Có; D0, D1 và D2 đều ra `MMHMH`, còn DAI-v1 tạo xung đột tại set XOR 0. |
| `dirty` | `W2048, R2048, R32, R4192` | `MHMM` | Có về writeback: DAI-v1 có dirty eviction và base ghi trả 2048. |
| `warmup` | Warmup `W0,R2080,R0`; đo `R4160,R0` | Trong measurement là `MH`. | Có; DAI-v1 có một eviction clean trong measurement. |

Ví dụ `lru` dùng block 0, 65, 130: ở DAI-v1 cả ba có index XOR 0, nên 2-way không chứa đồng thời cả ba; D1 modulo đặt chúng vào ba set khác nhau. Đây là ví dụ debug/tính tay, không phải workload benchmark.

Nguồn: `validation/manual_checks.md` §1–4; `validation/LATEST.txt`; `validation/check_20261031_154117_072086/summary.json`; `traces/debug/`.

## Giả định và giới hạn

- Simulator là mô hình chức năng tag/valid/dirty/replacement/traffic, không mô phỏng payload word, timing CPU, latency phần cứng, area, năng lượng, prefetch hay bypass.
- Trace của nghiên cứu là dữ liệu tổng hợp cho bối cảnh trạm cân; không được trình bày như dữ liệu thực thu từ thiết bị nếu chưa có phép thu thực tế.
- Không suy hiệu năng phần cứng, điện năng hay đáp ứng thời gian thực từ thời gian chạy Python, hit/miss hoặc traffic của simulator.
- DAI-v1 có phản ví dụ có thể thua: R002 nêu block 0, 65, 130 cùng vào một set DAI-v1 nhưng nằm ở ba set khác nhau của D0/D1; lặp ba block có thể làm DAI-v1 mất reuse mà D0/D1 giữ được.
- DAI-v1 đã chốt đặc tả, nhưng base address, generator W3/W4, manifest trace, môi trường simulator và hit-time sensitivity còn cần hoàn thiện trước official runs.

Nguồn: `README.md`; `experiment_protocol.md` §2, §5.2, §7.3; `ai/responses/R002.md` §3; `ai/AI_DESIGN_FREEZE.md` §Test dự kiến và giới hạn.

## Minh chứng AI và design freeze

| Nội dung | Bằng chứng trong repo |
|---|---|
| Công cụ | `AI_SESSION_LOG.md` ghi công cụ là Codex trong workspace AI; model ID hiển thị cụ thể không xác định và không tự điền phiên bản. |
| P001 | Xử lý từ `2026-10-31T15:10:40+07:00` đến mốc lưu `15:13:27+07:00`; tạo R001 với ba phương án A/B/C. |
| P002 | Xử lý từ `15:13:56+07:00` đến mốc lưu `15:16:30+07:00`; là tự phản biện, không phải reviewer độc lập. |
| P003 | Xử lý từ `15:16:59+07:00` đến mốc lưu `15:19:40+07:00`; chọn B và hoàn thiện đặc tả đề xuất. |
| Chốt thiết kế | `AI_DESIGN_FREEZE.md` ghi phương án B XOR 2-way đã chốt thành DAI-v1; Trương Tô Dân — QE210127 là người kiểm tra và xác nhận. |
| Mốc ghi nhận chốt | `2026-10-31T15:33:41+07:00`; đây là thời điểm ghi nhận xác nhận, không suy ngược thời điểm kiểm tra. |

Nguồn duy nhất của mục này: `ai/AI_SESSION_LOG.md`; `ai/AI_DESIGN_FREEZE.md`.

## Trạng thái kết quả

**Chưa có trong repo: chưa chạy official benchmark W1–W5.** README xác nhận chưa tạo official trace W1–W5, chưa chạy 96 run benchmark chính thức và chưa có kết quả hiệu quả DAI trên workload official.

Validation hiện có là validation debug: `validation/LATEST.txt` trỏ đến một summary có 21 unit test và 20 đối chiếu trace/config PASS. Các số này không phải kết quả official benchmark.

Nguồn: `README.md` mục “Trạng thái”; `validation/LATEST.txt`; `validation/check_20261031_154117_072086/summary.json`.
