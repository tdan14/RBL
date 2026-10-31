# Bảng tra cứu thuật ngữ và ký hiệu Q10

Tài liệu này chỉ tổng hợp thông tin có trong repo này (bản chưa chạy official benchmark). Các bảng được sắp theo alphabet, riêng nhóm mã W/LIT/thiết kế theo số thứ tự. Khi repo không giải nghĩa tên đầy đủ của ký hiệu, mục đó ghi **Chưa rõ - cần xác nhận**. Các mục mô tả kế hoạch hoặc benchmark chưa được thực hiện được ghi rõ là dự kiến.

## Mục lục

- [Mã workload W](#mã-workload-w)
- [Mã tài liệu LIT](#mã-tài-liệu-lit)
- [Mã thiết kế, quy trình và kiểm tra](#mã-thiết-kế-quy-trình-và-kiểm-tra)
- [Viết tắt](#viết-tắt)
- [Thuật ngữ kỹ thuật](#thuật-ngữ-kỹ-thuật)
- [Tên trường, biến và hằng số](#tên-trường-biến-và-hằng-số)
- [Trạng thái artefact và nguồn nghiên cứu](#trạng-thái-artefact-và-nguồn-nghiên-cứu)

## Mã workload W

`W1`–`W5` là mã **workload**, không phải mã tuần. Repo chưa có official trace W1–W5; phần mô tả bên dưới là đặc tả/kế hoạch trong protocol.

| Ký hiệu | Nghĩa đầy đủ | Giải thích 1 câu | Xuất hiện ở đâu |
|---|---|---|---|
| W1 | Sequential stream | Đọc tuần tự và ghi tuần tự để kiểm tra spatial locality và xử lý stream. | `experiment_protocol.md` §5 |
| W2 | Circular buffer | Dùng buffer 1 KiB, 4 KiB và 16 KiB để kiểm tra reuse theo working set. | `experiment_protocol.md` §5 |
| W3 | Moving average | Dùng cửa sổ 8, 32, 128, 512 và 2.048 mẫu, mỗi mẫu 4 B. | `experiment_protocol.md` §5 |
| W4 | Bốn sensor xen kẽ | Xen kẽ bốn buffer 1 KiB theo thứ tự đều hoặc ngẫu nhiên; đây là chuỗi access tuần tự, không phải mô phỏng multicore, coherence hay thực thi đồng thời. | `experiment_protocol.md` §2, §5 |
| W5 | Conflict/stride stress | Luân phiên 2, 4 hoặc 8 block cách nhau 4 KiB để tạo conflict có kiểm soát tại D0. | `experiment_protocol.md` §5 |

## Mã tài liệu LIT

Repo dùng mã `LIT-001`–`LIT-009`; không dùng chính thức dạng `LiT1`–`LiT9`. `LIT` là tiền tố mã hồ sơ tài liệu; tên viết đầy đủ của tiền tố: **Chưa rõ - cần xác nhận**.

| Ký hiệu | Nghĩa đầy đủ | Giải thích 1 câu | Xuất hiện ở đâu |
|---|---|---|---|
| LIT-001 | *Randomizing Set-Associative Caches Against Conflict-Based Cache Side-Channel Attacks* | Nguồn về randomized mapping và chi phí đổi mapping. | `Tong_hop_9_bai_bao_tham_khao_Q10.md`; `_research_sources/song.txt` |
| LIT-002 | *The Maya Cache: A Storage-efficient and Secure Fully-associative Last-level Cache* | Nguồn về fully-associative cache, tag/data và ngân sách bộ nhớ. | `Tong_hop_9_bai_bao_tham_khao_Q10.md`; `_research_sources/maya.txt` |
| LIT-003 | *Scatter and Split Securely: Defeating Cache Contention and Occupancy Attacks* | Nguồn về skewed mapping và trade-off bảo mật. | `Tong_hop_9_bai_bao_tham_khao_Q10.md`; `_research_sources/sass.txt` |
| LIT-004 | *Tartan: Microarchitecting a Robotic Processor* | Nguồn về workload có ngữ cảnh và tách đóng góp kiến trúc. | `Tong_hop_9_bai_bao_tham_khao_Q10.md`; `_research_sources/tartan.txt` |
| LIT-005 | *From Optimal to Practical: Efficient Micro-op Cache Replacement Policies for Data Center Applications* | Nguồn về oracle, profile và baseline trong micro-op cache. | `Tong_hop_9_bai_bao_tham_khao_Q10.md`; `_research_sources/furby.txt` |
| LIT-006 | *EMISSARY: Enhanced Miss Awareness Replacement Policy for L2 Instruction Caching* | Nguồn phân biệt số lượng miss với chi phí miss. | `Tong_hop_9_bai_bao_tham_khao_Q10.md`; `_research_sources/emissary.txt` |
| LIT-007 | *CHROME: Concurrency-Aware Holistic Cache Management Framework with Online Reinforcement Learning* | Nguồn về RL, metadata và phối hợp policy cache. | `Tong_hop_9_bai_bao_tham_khao_Q10.md`; `_research_sources/chrome.txt` |
| LIT-008 | *A Prefetch-Adaptive Intelligent Cache Replacement Policy Based on Machine Learning* | Nguồn về ML, prefetch và replacement policy. | `Tong_hop_9_bai_bao_tham_khao_Q10.md`; `_research_sources/paic.txt` |
| LIT-009 | *Sketching the Path to Efficiency: Lightweight Learned Cache Replacement* | Nguồn về ML nhẹ và policy theo frame; repo không có PDF/TXT cục bộ của bài này. | `Tong_hop_9_bai_bao_tham_khao_Q10.md` §LIT-009 |

## Mã thiết kế, quy trình và kiểm tra

| Ký hiệu | Nghĩa đầy đủ | Giải thích 1 câu | Xuất hiện ở đâu |
|---|---|---|---|
| D0 | Design ID D0 | Baseline direct-mapped: 128 set × 1 way, modulo mapping. | `configs/D0.json`; `experiment_protocol.md` §4 |
| D1 | Design ID D1 | Baseline 2-way set-associative: 64 set × 2 way, modulo mapping và LRU. | `configs/D1.json`; `experiment_protocol.md` §4 |
| D2 | Design ID D2 | Baseline 4-way set-associative: 32 set × 4 way, modulo mapping và LRU. | `configs/D2.json`; `experiment_protocol.md` §4 |
| DAI / DAI-v1 | Chưa rõ - cần xác nhận (mở rộng DAI) | Candidate AI hiện được freeze thành DAI-v1: XOR mapping, 64 set × 2 way. | `configs/DAI-v1.json`; `ai/AI_DESIGN_FREEZE.md` |
| H0 | Null hypothesis | Phương án AI không cải thiện miss rate so với Direct Mapping. | `experiment_protocol.md` §1.2 |
| H1 | Hypothesis 1 | Phương án AI giảm miss ở workload có nhiều conflict. | `experiment_protocol.md` §1.2 |
| H2 | Hypothesis 2 | Lợi ích của candidate phụ thuộc access pattern. | `experiment_protocol.md` §1.2 |
| P001 | Initial Proposal | Prompt yêu cầu ba candidate mapping dưới các ràng buộc cố định. | `ai/prompts/P001.md` |
| P002 | Critical Review | Prompt yêu cầu phản biện các candidate. | `ai/prompts/P002.md` |
| P003 | Final Selection | Prompt yêu cầu chọn và đặc tả candidate cuối. | `ai/prompts/P003.md` |
| R001–R003 | Response 001–003 | Ba phản hồi AI tương ứng P001–P003. | `ai/responses/` |
| RQ1–RQ4 | Research Questions 1–4 | Các câu hỏi nghiên cứu thành phần của kế hoạch Q10. | `Ke_hoach_RBL_Q10_AI_Cache_Mapping.docx` §3.2 |
| T01–T06 | Test 01–06 | Sáu test validation tối thiểu của protocol. | `experiment_protocol.md` §9 |
| X01–X07 | Extra test 01–07 | Các kiểm tra bổ sung cho DAI-v1, gồm địa chỉ biên, warmup và reset. | `ai/responses/R003.md` §6 |

## Viết tắt

| Ký hiệu | Nghĩa đầy đủ | Giải thích 1 câu | Xuất hiện ở đâu |
|---|---|---|---|
| AI | Artificial Intelligence | Công cụ AI hỗ trợ đề xuất/phản biện thiết kế, không phải policy học online của simulator. | `ai/AI_SESSION_LOG.md`; `ai/README.md` |
| ALPS | Chưa rõ - cần xác nhận (mở rộng tên) | LIT-009 mô tả ALPS dùng sketches và ML để chọn policy cho frame tiếp theo. | `Tong_hop_9_bai_bao_tham_khao_Q10.md` §LIT-009 |
| AMAT | Average Memory Access Time | Protocol dùng công thức AMAT ước tính; lõi simulator không tính AMAT. | `experiment_protocol.md` §7.3; `README.md` |
| B | Byte | Đơn vị dung lượng, ví dụ cache line 32 B. | `experiment_protocol.md` §3 |
| CEA201 | Computer Organization & Architecture | Mã môn học ghi trong protocol. | `experiment_protocol.md` |
| CHROME | Concurrency-Aware Holistic Cache Management Framework with Online Reinforcement Learning | Framework RL trong LIT-007. | `_research_sources/chrome.txt` |
| CLI | Command Line Interface | Giao diện dòng lệnh của runner. | `src/simulator/runner.py` |
| CLO / CLO10 | Chưa rõ - cần xác nhận | Repo dùng mã CLO10 nhưng không có văn bản giải nghĩa tên đầy đủ. | `Ke_hoach_RBL_Q10_AI_Cache_Mapping.docx` |
| CPU | Central Processing Unit | Bộ xử lý trong phần giải thích memory hierarchy; Q10 không mô phỏng timing CPU. (Nghĩa viết tắt là kiến thức chung, repo không định nghĩa.) | `README.md`; `Ke_hoach_RBL_Q10_AI_Cache_Mapping.docx` |
| DOI | Digital Object Identifier | Mã nhận diện công bố được dùng cho nguồn nghiên cứu. (Nghĩa viết tắt là kiến thức chung, repo không định nghĩa.) | `Tong_hop_9_bai_bao_tham_khao_Q10.md` |
| EMISSARY | Enhanced Miss Awareness Replacement Policy for L2 Instruction Caching | Replacement policy trong LIT-006. | `_research_sources/emissary.txt` |
| FIFO | First-in-first-out | Policy loại phần tử vào trước, được nhắc trong tài liệu nền. | `Ke_hoach_RBL_Q10_AI_Cache_Mapping.docx` §2.7 |
| ISVM | Integer Support Vector Machine | PAIC dùng predictor này riêng cho demand và prefetch request. | `_research_sources/paic.txt` |
| JSON / JSONL | JavaScript Object Notation / JSON Lines | Runner xuất JSON cho result và JSONL cho event theo từng access. (Nghĩa viết tắt là kiến thức chung, repo không định nghĩa.) | `README.md`; `src/simulator/runner.py` |
| KiB | Kibibyte | 1 KiB = 1.024 byte; 4 KiB = 4.096 byte trong protocol. | `experiment_protocol.md` §3 |
| LLC | Last-Level Cache | Cấp cache cuối trong các công trình tham khảo, không phải mô hình một cấp của Q10. | `_research_sources/chrome.txt`; `Tong_hop_9_bai_bao_tham_khao_Q10.md` |
| LRU | Least Recently Used | Policy chọn line lâu nhất chưa được dùng. | `src/simulator/cache.py`; `README.md` |
| ML | Machine Learning | Nhóm phương pháp trong LIT-007–009. | `Tong_hop_9_bai_bao_tham_khao_Q10.md` |
| MR / MR_D0 | Miss Rate / miss rate của D0 | Tỷ lệ miss và biến baseline trong công thức relative miss reduction. | `experiment_protocol.md` §7.1 |
| MRU | Most Recently Used | Line mới dùng nhất; rank 0 ở D2. | `src/simulator/models.py` |
| OP / R / W | Operation / Read / Write | Ba ký hiệu dùng trong trace cho thao tác và hai giá trị hợp lệ. | `src/simulator/trace.py` |
| PAIC | Prefetch-Adaptive Intelligent Cache Replacement Policy | Policy trong LIT-008. | `_research_sources/paic.txt` |
| PC | Program Counter | Thông tin predictor trong bài tham khảo, chưa có trong trace Q10. | `_research_sources/chrome.txt`; `Tong_hop_9_bai_bao_tham_khao_Q10.md` |
| PLRU | Pseudo-LRU | Biến thể xấp xỉ LRU được nhắc trong nguồn, không dùng cho D2. | `_research_sources/emissary.txt`; `Ke_hoach_xay_simulator.md` |
| RAM | Random Access Memory | Bộ nhớ chính được dùng để minh họa memory hierarchy. (Nghĩa viết tắt là kiến thức chung, repo không định nghĩa.) | `Ke_hoach_RBL_Q10_AI_Cache_Mapping.docx` |
| RBL | Chưa rõ - cần xác nhận | Viết tắt xuất hiện ở tên repo/báo cáo nhưng không có định nghĩa trong repo. | `CEA201_RBL_Report.pdf`; tên repo |
| RL | Reinforcement Learning | Học tăng cường được CHROME dùng cho quản lý cache. | `_research_sources/chrome.txt` |
| RQ | Research Question | Câu hỏi nghiên cứu. | `Ke_hoach_RBL_Q10_AI_Cache_Mapping.docx` |
| SHA-256 | Secure Hash Algorithm, 256-bit | Hash dùng nhận diện nội dung source, config và trace. (Nghĩa viết tắt là kiến thức chung, repo không định nghĩa.) | `src/simulator/runner.py`; `ai/evidence/SHA256SUMS.json` |
| SPP | Signature Path Prefetcher | Prefetcher dùng trong phép so của PAIC. | `_research_sources/paic.txt` |
| WB | Writeback | Ký hiệu dirty writeback trong các bảng kiểm. | `validation/manual_checks.md` |
| XOR | Exclusive OR | Phép `^` trộn bit block để tính index của DAI-v1. (Nghĩa viết tắt là kiến thức chung, repo không định nghĩa.) | `src/simulator/mapping.py` |

## Thuật ngữ kỹ thuật

| Ký hiệu | Nghĩa đầy đủ | Giải thích 1 câu | Xuất hiện ở đâu |
|---|---|---|---|
| Access | Demand memory access | Một thao tác đọc hoặc ghi trong trace, không phải số instruction hay số mẫu sensor. | `experiment_protocol.md` §6.1 |
| Associativity | Số way trong mỗi set | Quy định số vị trí hợp lệ một block có thể nằm trong set. | `src/simulator/models.py` |
| Cache | Bộ nhớ đệm | Mô hình Q10 là cache dữ liệu một cấp, tag-only. | `README.md` |
| Cache line / block | Dòng cache / khối bộ nhớ | Đơn vị 32 byte được nạp và ghi trả trong mô hình. | `experiment_protocol.md` §3 |
| Conflict miss | Miss do xung đột | Miss do nhiều block cạnh tranh vị trí hợp lệ cùng set. | `experiment_protocol.md` §5 |
| Direct mapping | Ánh xạ trực tiếp | Mỗi block chỉ có một vị trí cache có thể chứa nó. | `experiment_protocol.md` §4; `configs/D0.json` |
| Dirty line | Line đã ghi | Line có dirty true; eviction line này mới tạo dirty writeback. | `src/simulator/cache.py` |
| Eviction | Loại line valid | Thay line hợp lệ để nạp block mới khi không còn way trống. | `src/simulator/cache.py` |
| Exact LRU | LRU chính xác | D1/DAI dùng `lru_way`; D2 dùng `rank` liên tục. | `src/simulator/cache.py` |
| Fill / line fill | Nạp line | Mỗi miss nạp một line trong mô hình không prefetch/bypass. | `src/simulator/cache.py` |
| Hash mapping | Ánh xạ trộn bit | DAI-v1 dùng XOR, khác SHA-256 là hash nhận diện file. | `src/simulator/mapping.py` |
| Hit / miss | Trúng / trượt cache | Hit có line valid khớp tag; miss phải tìm way hoặc victim để fill. | `src/simulator/cache.py` |
| Index / set index | Chỉ số set | Giá trị xác định set cần lookup; modulo dùng `block % sets`, XOR dùng công thức riêng. | `src/simulator/mapping.py` |
| Locality | Tính cục bộ | Gồm temporal locality và spatial locality của chuỗi access. | `Ke_hoach_RBL_Q10_AI_Cache_Mapping.docx` §2.4 |
| Mapping / placement | Quy tắc đặt block | Xác định index và các vị trí chứa block trước replacement. | `src/simulator/mapping.py` |
| Memory traffic | Lưu lượng bộ nhớ | `(line_fills + dirty_writebacks) × 32` byte trong khoảng đo. | `src/simulator/cache.py`; `experiment_protocol.md` §7.2 |
| Metadata | Thông tin quản lý cache | Tag, valid, dirty và replacement state được báo riêng dung lượng dữ liệu. | `src/simulator/models.py`; `ai/AI_DESIGN_FREEZE.md` |
| Prefetch / bypass | Đọc trước / bỏ qua cache | Hai cơ chế bị tắt trong cấu hình Q10. | `src/simulator/models.py` |
| Set | Tập cache | Nhóm các way được lookup bằng một index. | `src/simulator/models.py`; `src/simulator/cache.py` |
| Set / way | Tập / vị trí trong tập | `sets × ways × line_bytes = 4096` cho các config hợp lệ. | `src/simulator/models.py` |
| Tag | Nhãn block | Phần nhận diện block được lưu trong line và so sánh khi lookup. | `src/simulator/mapping.py`; `src/simulator/models.py` |
| Trace | Chuỗi truy cập bộ nhớ | Mỗi dòng hợp lệ là `OP ADDRESS SIZE`; comment và dòng trống bị bỏ qua. | `src/simulator/trace.py`; `README.md` |
| Valid bit | Cờ hợp lệ | Cờ cho biết line tham gia lookup và có thể bị eviction. | `src/simulator/models.py`; `src/simulator/cache.py` |
| Victim | Line bị thay | Way bị chọn khi set đầy; D0 luôn chọn way 0, các thiết kế khác dùng LRU. | `src/simulator/cache.py` |
| Warmup / measurement | Khởi động / khoảng đo | Warmup cập nhật cache nhưng không cộng counters; state được giữ sang measurement. | `src/simulator/runner.py`; `README.md` |
| Way | Vị trí trong set | Một set có 1, 2 hoặc 4 way tùy config. | `configs/`; `src/simulator/cache.py` |
| Write-allocate / write-back | Nạp khi write miss / ghi trả khi loại line bẩn | Hai write policy cố định cho mọi config. | `src/simulator/models.py`; `experiment_protocol.md` §3 |

## Tên trường, biến và hằng số

| Ký hiệu | Nghĩa đầy đủ | Giải thích 1 câu | Xuất hiện ở đâu |
|---|---|---|---|
| `0xFFFFFFFC` | Địa chỉ access tối đa | Access 4 byte hợp lệ phải căn chỉnh và không vượt địa chỉ này. | `src/simulator/models.py` |
| `4` / `32` / `4096` | Access bytes / line bytes / capacity bytes | Ba kích thước cố định của mô hình. | `src/simulator/models.py`; `experiment_protocol.md` §3 |
| `accesses`, `hits`, `misses` | Counters tổng | Luôn thỏa `hits + misses == accesses` trong measurement. | `src/simulator/models.py` |
| `AccessResult` | Bản ghi một access | Dataclass chứa operation, address, block, index, tag, way, hit và thông tin victim/fill/writeback. | `src/simulator/cache.py` |
| `address`, `size`, `operation` | Địa chỉ, kích thước, thao tác | Input access hợp lệ là R/W, địa chỉ nguyên căn 4 byte, size bằng 4. | `src/simulator/models.py`; `src/simulator/trace.py` |
| `block`, `index`, `tag` | Số block, chỉ số set, nhãn block | `Mapping.split()` trả ba giá trị này để lookup cache. | `src/simulator/mapping.py` |
| `capacity_bytes`, `line_bytes`, `sets`, `ways` | Thông số cấu hình | Xác định dung lượng dữ liệu, kích thước line và associativity. | `src/simulator/models.py`; `configs/` |
| `dirty_writebacks`, `evictions`, `line_fills` | Counters sự kiện miss | Ghi trả dirty là một phần của eviction; fills bằng misses trong mô hình này. | `src/simulator/models.py`; `src/simulator/cache.py` |
| `dirty`, `valid`, `rank` | Trạng thái CacheLine | `dirty` đánh dấu ghi; `valid` cho phép lookup; `rank` dùng cho D2. | `src/simulator/models.py` |
| `lru_way` | Way LRU của set 2-way | Mảng chỉ set có 2 way; cập nhật thành `1 - way` khi chạm line. | `src/simulator/cache.py` |
| `measured`, `measuring` | Cờ measurement | Event ghi `measured`; cache dùng `measuring` để quyết định tăng counter. | `src/simulator/cache.py` |
| `metrics_validated` | Cờ metric của run thành công | Runner đặt true khi status là SUCCESS; đây không phải xác nhận độc lập của nhóm. | `src/simulator/runner.py`; `README.md` |
| `read_misses`, `write_misses` | Miss đọc, miss ghi | Tổng hai counter này phải bằng `misses`. | `src/simulator/models.py` |
| `run_id`, `trace_id`, `seed` | Nhận diện run, trace và seed | Result lưu các giá trị này; `trace_id` bắt buộc trong official mode. | `src/simulator/runner.py` |
| `status` | Trạng thái run | Runner hiện trả SUCCESS hoặc FAIL; protocol cũng mô tả INVALID cho run không hợp lệ. | `src/simulator/runner.py`; `experiment_protocol.md` §6.3 |
| `warmup_accesses`, `measured_accesses` | Số access warmup, số access đo | `requested` và `observed` tách yêu cầu khỏi số access thực tế xử lý. | `src/simulator/runner.py` |
| `writeback_base` | Địa chỉ block ghi trả | Bằng `victim_block << 5`; XOR phải dùng recover_block để lấy đúng victim block. | `src/simulator/cache.py`; `validation/manual_checks.md` |

## Trạng thái artefact và nguồn nghiên cứu

| Ký hiệu | Nghĩa đầy đủ | Giải thích 1 câu | Xuất hiện ở đâu |
|---|---|---|---|
| `traces/debug/` | Trace debug | Có năm trace kiểm tra: boundary, dirty, lru, repeat và warmup; chúng không phải official W1–W5. | `traces/debug/`; `README.md` |
| `validation/` | Kết quả validation debug | Có 21 unit tests và 20 đối chiếu trace/config PASS theo README, nhưng chưa là human sign-off hoặc đối chiếu Ripes. | `README.md`; `validation/LATEST.txt` |
| Official W1–W5 traces | Chưa có trong repo | README ghi chưa tạo official trace W1–W5. | `README.md` |
| Official 96 runs | Chưa có trong repo | Protocol nêu 24 trace × 4 thiết kế là số run dự kiến; README ghi chưa chạy benchmark chính thức. | `experiment_protocol.md` §6.2; `README.md` |
| `_research_sources/` | Tài liệu nguồn cục bộ | Có PDF/TXT/JSON cho nhiều nguồn LIT và các file metadata/check; LIT-009 không có bản PDF/TXT cục bộ. | `_research_sources/`; `Tong_hop_9_bai_bao_tham_khao_Q10.md` |

