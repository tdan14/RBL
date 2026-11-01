# Tổng Hợp và Đánh Giá Thư Mục Tài Liệu Nghiên Cứu (`_research_sources/`) (Phiên Bản v2)
## Đề tài: AI-Assisted Cache Mapping for Continuous Data Streams (Q10 - CEA201)

---

## Mục Lục

- [1. Cây Thư Mục Thực Tế (`_research_sources/`)](#1-cây-thư-mục-thực-tế-_research_sources)
- [2. Bảng Tra Cứu và Đánh Giá Chi Tiết 9 Bài Báo Nghiên Cứu](#2-bảng-tra-cứu-và-đánh-giá-chi-tiết-9-bài-báo-nghiên-cứu)
- [3. Bảng Các Tệp Hỗ Trợ Kiểm Tra và Siêu Dữ Liệu Nguồn](#3-bảng-các-tệp-hỗ-trợ-kiểm-tra-và-siêu-dữ-liệu-nguồn)
- [4. Danh Sách Tài Liệu Thiếu Nguồn hoặc Có Bất Thường](#4-danh-sách-tài-liệu-thiếu-nguồn-hoặc-có-bất-thường)

---

## 1. Cây Thư Mục Thực Tế (`_research_sources/`)

Thư mục `_research_sources/` hiện lưu trữ đúng **25 tệp tin** (tổng dung lượng khoảng 9,6 MB) bao gồm 8 bản PDF toàn văn, 8 bản trích xuất text, 6 tệp siêu dữ liệu Crossref JSON, cùng 3 tệp JSON phục vụ kiểm toán nội dung và liên kết nguồn:

```text
_research_sources/
├── 3579371.3589097.json         # Metadata Crossref của LIT-006 (ACM DOI suffix: 10.1145/3579371.3589097)
├── chrome.pdf                   # Toàn văn PDF của LIT-007 (CHROME, HPCA 2024)
├── chrome.txt                   # Bản trích xuất text từ chrome.pdf
├── document_validation.json     # Kết quả script kiểm thử cấu trúc của Tong_hop_9_bai_bao_tham_khao_Q10.md
├── emissary.pdf                 # Toàn văn PDF của LIT-006 (EMISSARY, ISCA 2023)
├── emissary.txt                 # Bản trích xuất text từ emissary.pdf
├── furby.pdf                    # Toàn văn PDF của LIT-005 (From Optimal to Practical / FURBYS, HPCA 2025)
├── furby.txt                    # Bản trích xuất text từ furby.pdf
├── HPCA57654.2024.00090.json    # Metadata Crossref của LIT-007 (IEEE DOI suffix: 10.1109/HPCA57654.2024.00090)
├── ISCA59077.2024.00013.json    # Metadata Crossref của LIT-002 (IEEE DOI suffix: 10.1109/ISCA59077.2024.00013)
├── maya.pdf                     # Toàn văn PDF của LIT-002 (The Maya Cache, ISCA 2024)
├── maya.txt                     # Bản trích xuất text từ maya.pdf
├── metadata_check.json          # Báo cáo kết quả truy vấn Crossref API của cả 9 bài báo LIT-001..LIT-009
├── paic.pdf                     # Toàn văn PDF của LIT-008 (PAIC, JCST 2023)
├── paic.txt                     # Bản trích xuất text từ paic.pdf
├── s11390-022-1573-3.json       # Metadata Crossref của LIT-008 (Springer DOI: 10.1007/s11390-022-1573-3)
├── sass.pdf                     # Toàn văn PDF của LIT-003 (Scatter and Split Securely / SassCache, IEEE S&P 2023)
├── sass.txt                     # Bản trích xuất text từ sass.pdf
├── song.pdf                     # Toàn văn PDF của LIT-001 (Randomizing Set-Associative Caches, IEEE TC 2024)
├── song.txt                     # Bản trích xuất text từ song.pdf
├── source_urls.json             # Danh mục URL tải tài liệu toàn văn gốc (gồm 9 URL)
├── SP46215.2023.10179440.json   # Metadata Crossref của LIT-003 (IEEE DOI suffix: 10.1109/SP46215.2023.10179440)
├── tartan.pdf                   # Toàn văn PDF của LIT-004 (Tartan, ISCA 2024)
├── tartan.txt                   # Bản trích xuất text từ tartan.pdf
└── TC.2024.3349659.json         # Metadata Crossref của LIT-001 (IEEE DOI suffix: 10.1109/TC.2024.3349659)
```

---

## 2. Bảng Tra Cứu và Đánh Giá Chi Tiết 9 Bài Báo Nghiên Cứu

> **Nguyên tắc đối chiếu:** Toàn bộ tên bài báo được lấy chính xác từ `Tong_hop_9_bai_bao_tham_khao_Q10.md` hoặc các tệp siêu dữ liệu Crossref JSON trong `_research_sources/`. Sắp xếp theo thứ tự mã số tăng dần từ LIT-001 đến LIT-009. Cột "Gợi ý đổi tên" chỉ mang tính đề xuất chuẩn hóa, **tuyệt đối KHÔNG thực hiện đổi tên** để bảo toàn file gốc.

| Mã LIT | Tên file trong repo | Nội dung chính (1–2 câu) | Liên quan RQ/CLO | Link/nguồn gốc | Gợi ý đổi tên (Không sửa file gốc) |
|---|---|---|---|---|---|
| **LIT-001** | `song.pdf`<br>`song.txt`<br>`TC.2024.3349659.json` | Bài báo *"Randomizing Set-Associative Caches Against Conflict-Based Cache Side-Channel Attacks"* (IEEE TC 2024, Wei Song et al.) nghiên cứu cơ chế băm ngẫu hóa địa chỉ để phân tán xung đột set và đo độ trễ phần cứng. | RQ1, RQ2, CLO10 | [DOI: 10.1109/TC.2024.3349659](https://doi.org/10.1109/TC.2024.3349659)<br>[Bản PDF tác giả](https://wsong83.github.io/publication/comparch/tc2024.pdf) | `LIT-001_song_tc2024.pdf`<br>`LIT-001_song_tc2024.txt`<br>`LIT-001_metadata.json` |
| **LIT-002** | `maya.pdf`<br>`maya.txt`<br>`ISCA59077.2024.00013.json` | Bài báo *"The Maya Cache: A Storage-efficient and Secure Fully-associative Last-level Cache"* (ISCA 2024, Anubhav Bhatla et al.) đề xuất kiến trúc tách rời mảng tag và data để đạt hiệu quả phân tán va chạm như fully-associative với ngân sách bộ nhớ tối thiểu. | RQ2, RQ3, CLO10 | [DOI: 10.1109/ISCA59077.2024.00013](https://doi.org/10.1109/ISCA59077.2024.00013)<br>[Bản PDF IIT Bombay](https://www.cse.iitb.ac.in/~biswa/ISCA2024.pdf) | `LIT-002_maya_isca2024.pdf`<br>`LIT-002_maya_isca2024.txt`<br>`LIT-002_metadata.json` |
| **LIT-003** | `sass.pdf`<br>`sass.txt`<br>`SP46215.2023.10179440.json` | Bài báo *"Scatter and Split Securely: Defeating Cache Contention and Occupancy Attacks"* (IEEE S&P 2023, L. Giner et al. / SassCache) đề xuất kỹ thuật skewed mapping độc lập trên từng way để giải quyết xung đột có chu kỳ. | RQ1, RQ2, CLO10 | [DOI: 10.1109/SP46215.2023.10179440](https://doi.org/10.1109/SP46215.2023.10179440)<br>[Bản PDF tác giả](https://antoonpurnal.github.io/files/pdf/SassCache.pdf) | `LIT-003_sass_sp2023.pdf`<br>`LIT-003_sass_sp2023.txt`<br>`LIT-003_metadata.json` |
| **LIT-004** | `tartan.pdf`<br>`tartan.txt` | Bài báo *"Tartan: Microarchitecting a Robotic Processor"* (ISCA 2024) nghiên cứu vi kiến trúc bộ xử lý robot; `Tong_hop_9_bai_bao_tham_khao_Q10.md` dùng nó để rút ra cách thiết kế workload có ngữ nghĩa và đánh giá từng thành phần riêng (không phải nguồn trực tiếp của W1–W5). | RQ1, RQ3, CLO10 | [DOI: 10.1109/ISCA59077.2024.00047](https://doi.org/10.1109/ISCA59077.2024.00047)<br>[Bản PDF CMU PDL](https://www.pdl.cmu.edu/PDL-FTP/associated/Tartan-ISCA24.pdf) | `LIT-004_tartan_isca2024.pdf`<br>`LIT-004_tartan_isca2024.txt` |
| **LIT-005** | `furby.pdf`<br>`furby.txt` | Bài báo *"From Optimal to Practical: Efficient Micro-op Cache Replacement Policies for Data Center Applications"* (HPCA 2025, Kan Zhu et al.) làm rõ phương pháp đối chứng với thuật toán tối ưu lý thuyết (Bélády/Oracle) và chọn baseline đúng. | RQ2, RQ3, CLO10 | [DOI: 10.1109/HPCA61900.2025.00060](https://doi.org/10.1109/HPCA61900.2025.00060)<br>[Bản PDF THU-HASLab](https://www.thu-haslab.org/publication/co-public/2025-from-optimal-to-practical/19_HPCA2025_micro-op_cache.pdf) | `LIT-005_optimal_furby_hpca2025.pdf`<br>`LIT-005_optimal_furby_hpca2025.txt` |
| **LIT-006** | `emissary.pdf`<br>`emissary.txt`<br>`3579371.3589097.json` | Bài báo *"EMISSARY: Enhanced Miss Awareness Replacement Policy for L2 Instruction Caching"* (ISCA 2023) chứng minh chi phí thực sự của miss (latency và memory traffic) không đồng nhất với số lượng miss đơn thuần. | RQ3, CLO10 | [DOI: 10.1145/3579371.3589097](https://doi.org/10.1145/3579371.3589097)<br>[Bản PDF Princeton Liberty](https://liberty.princeton.edu/Publications/isca23_emissary.pdf) | `LIT-006_emissary_isca2023.pdf`<br>`LIT-006_emissary_isca2023.txt`<br>`LIT-006_metadata.json` |
| **LIT-007** | `chrome.pdf`<br>`chrome.txt`<br>`HPCA57654.2024.00090.json` | Bài báo *"CHROME: Concurrency-Aware Holistic Cache Management Framework with Online Reinforcement Learning"* (HPCA 2024) áp dụng học tăng cường (RL) quản lý cache và làm rõ sự khác biệt giữa AI hỗ trợ thiết kế tĩnh với mô hình học máy trực tuyến. | RQ2, CLO10 | [DOI: 10.1109/HPCA57654.2024.00090](https://doi.org/10.1109/HPCA57654.2024.00090)<br>[Bản PDF tác giả](https://xiaoyang-lu.github.io/files/HPCA2024/CHROME_paper.pdf) | `LIT-007_chrome_hpca2024.pdf`<br>`LIT-007_chrome_hpca2024.txt`<br>`LIT-007_metadata.json` |
| **LIT-008** | `paic.pdf`<br>`paic.txt`<br>`s11390-022-1573-3.json` | Bài báo *"A Prefetch-Adaptive Intelligent Cache Replacement Policy Based on Machine Learning"* (JCST 2023) nghiên cứu ứng dụng ML cho chính sách thay thế kết hợp prefetch, đóng vai trò tham khảo kiểm soát biến khi đánh giá độc lập mapping. | RQ2, CLO10 | [DOI: 10.1007/s11390-022-1573-3](https://doi.org/10.1007/s11390-022-1573-3)<br>[Bản PDF JCST ICT](https://jcst.ict.ac.cn/en/article/pdf/preview/10.1007/s11390-022-1573-3.pdf) | `LIT-008_paic_jcst2023.pdf`<br>`LIT-008_paic_jcst2023.txt`<br>`LIT-008_metadata.json` |
| **LIT-009** | *(Không có file cục bộ trong thư mục)* | Bài báo *"Sketching the Path to Efficiency: Lightweight Learned Cache Replacement"* (OPODIS 2023 / Schloss Dagstuhl 2024) khảo sát mô hình ML nhẹ trên cửa sổ dữ liệu trượt cho cache phần mềm; hỗ trợ thảo luận giới hạn chi phí bảng tra cứu. | RQ2, CLO10 | [DOI: 10.4230/LIPIcs.OPODIS.2023.34](https://doi.org/10.4230/LIPIcs.OPODIS.2023.34)<br>[Toàn văn Dagstuhl](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.OPODIS.2023.34) | `LIT-009_sketching_opodis2023.*` |

---

## 3. Bảng Các Tệp Hỗ Trợ Kiểm Tra và Siêu Dữ Liệu Nguồn

| Tên file trong repo | Chức năng và nội dung kiểm tra cụ thể | Ghi chú phản ánh trung thực nội dung file |
|---|---|---|
| `document_validation.json` | Tệp JSON ghi lại kết quả chạy script kiểm tra định dạng nội dung tệp `Tong_hop_9_bai_bao_tham_khao_Q10.md`. | File này kiểm tra 4 trường cho 9 mục LIT-001..009 gồm: `analysis_and_conclusion_words` (số từ phân tích/kết luận), `owner` (người phụ trách), `has_conclusion` (có mục kết luận), `has_doi` (có trường DOI) và cờ tổng kết `all_passed: true`. |
| `metadata_check.json` | Tệp JSON ghi nhật ký các truy vấn tự động qua cổng Crossref REST API cho mã DOI của cả 9 bài báo. | Phản ánh kết quả ngày xuất bản, loại ấn phẩm, trang; ghi nhận lỗi `HTTP 429 Too Many Requests` cho LIT-004 và LIT-005, cùng lỗi `HTTP 404 Not Found` cho LIT-009. |
| `source_urls.json` | Tệp JSON lưu danh sách 9 liên kết URL dùng để tải tệp toàn văn PDF gốc cho các bài báo tham khảo. | Chứa các đường link tải cho `song`, `maya`, `sass`, `tartan`, `furby`, `chrome`, `paic`, `emissary`, và liên kết `lstm`. |

---

## 4. Danh Sách Tài Liệu Thiếu Nguồn hoặc Có Bất Thường

Đối chiếu giữa danh sách tệp vật lý trong `_research_sources/`, tệp chỉ mục `source_urls.json` và kết quả truy vấn `metadata_check.json`, các bất thường và thiếu sót cụ thể gồm:

1. **LIT-009 hoàn toàn không có tệp lưu trữ cục bộ trong thư mục:**
   - **Tên công trình:** *Sketching the Path to Efficiency: Lightweight Learned Cache Replacement* (Hội nghị OPODIS 2023 / Schloss Dagstuhl).
   - **Tình trạng:** Trong thư mục `_research_sources/` hoàn toàn **không có** tệp PDF, tệp TXT hay tệp JSON metadata riêng của bài này.
   - **Ghi nhận trong repo:** truy vấn Crossref cho DOI `10.4230/LIPIcs.OPODIS.2023.34` trả `HTTP Error 404: Not Found` (xem `metadata_check.json`); `Tong_hop_9_bai_bao_tham_khao_Q10.md` ghi bài được xác minh trực tiếp tại Dagstuhl và không coi 404 là DOI không tồn tại. **Lý do không có PDF cục bộ: chưa rõ - cần xác nhận** (repo không ghi).
   - **Nguồn thay thế:** Nhóm đọc trực tiếp toàn văn qua giao diện web tại kho mở Dagstuhl: `https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.OPODIS.2023.34`.

2. **LIT-004 thiếu tệp siêu dữ liệu JSON độc lập và gặp lỗi kiểm tra API:**
   - **Tên công trình:** *Tartan: Microarchitecting a Robotic Processor* (ISCA 2024).
   - **Tình trạng:** Đã có `tartan.pdf` và `tartan.txt`, nhưng **chưa có tệp `.json` metadata riêng** nằm trong thư mục như các bài khác.
   - **Lỗi ghi nhận:** Trong `metadata_check.json`, truy vấn DOI `10.1109/ISCA59077.2024.00047` trả về mã lỗi `HTTP Error 429: Too Many Requests` (bị giới hạn tần suất gọi API).

3. **LIT-005 thiếu tệp siêu dữ liệu JSON độc lập và đặt tên tệp lệch quy ước:**
   - **Tên công trình:** *From Optimal to Practical: Efficient Micro-op Cache Replacement Policies for Data Center Applications* (HPCA 2025).
   - **Tình trạng:** Đã có file toàn văn nhưng đặt tên là `furby.pdf` và `furby.txt` (lấy theo tên chính sách đề xuất `FURBYS` trong nội dung bài). Đồng thời, tệp này **chưa có tệp `.json` metadata riêng**.
   - **Lỗi ghi nhận:** Trong `metadata_check.json`, truy vấn DOI `10.1109/HPCA61900.2025.00060` cũng bị chặn bởi lỗi `HTTP Error 429: Too Many Requests`.

4. **Liên kết dư thừa bài báo bị loại trong `source_urls.json` (`lstm`):**
   - **Tên công trình:** *LSTM-CRP: Algorithm-Hardware Co-Design and Implementation of Cache Replacement Policy Using Long Short-Term Memory* (Tạp chí MDPI Technologies).
   - **Tình trạng:** Khóa `"lstm": "https://www.mdpi.com/2504-2289/8/10/140/pdf"` xuất hiện ở dòng 10 tệp `source_urls.json`, nhưng trong thư mục **không có bất kỳ file `lstm.pdf` hay `lstm.txt` nào**.
   - **Ghi nhận trong repo:** `Tong_hop_9_bai_bao_tham_khao_Q10.md` ghi bài này có liên quan nhưng trang toàn văn/PDF bị từ chối truy cập trong phiên khảo cứu; mã lỗi cụ thể không được ghi. URL vẫn còn trong `source_urls.json`.

