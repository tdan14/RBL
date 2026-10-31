# Quy trình thí nghiệm Q10

**Đề tài:** AI-Assisted Cache Mapping for Continuous Data Streams.  
**Môn học:** Computer Organization & Architecture — CEA201.  
**Protocol ID:** Q10-PROTOCOL-v1.0.  
**Ngày lập:** 31/10/2026, múi giờ Asia/Saigon (UTC+07:00).  
**Trạng thái:** Phương án đã được người dùng chấp thuận trong cuộc trao đổi; văn bản hóa trước bước P001–P003 và benchmark chính thức.  
**Nhóm:** Trương Tô Dân — QE210127; Trần Châu Hoàng Nam — QE210145; Dương Quốc Thịnh — QE210121.

Tài liệu này chốt câu hỏi, biến kiểm soát, đối chứng, workload, chỉ số, cách kiểm chứng và quy tắc sử dụng AI cho nghiên cứu Q10. Thiết kế DAI chưa được lựa chọn; các trường dành cho DAI chỉ được hoàn thiện sau P003 và phải được chốt trước benchmark chính thức. Tài liệu không xác nhận simulator đã hoàn thành, đã vượt validation hoặc đã có kết quả thực nghiệm.

## 1. Câu hỏi nghiên cứu và giả thuyết

### 1.1. Câu hỏi chính

Với cùng dung lượng cache và cùng chuỗi truy cập bộ nhớ mô phỏng trạm cân, phương án mapping do AI đề xuất có giảm miss rate và lưu lượng truy cập bộ nhớ so với Direct Mapping không? Hiệu quả thay đổi thế nào giữa các workload?

### 1.2. Giả thuyết

- **H0:** phương án AI không cải thiện miss rate so với Direct Mapping trên các trường hợp được kiểm tra.
- **H1:** phương án AI giảm miss trên workload có nhiều xung đột.
- **H2:** lợi ích phụ thuộc pattern truy cập; phương án AI không được mặc định tốt hơn trên mọi workload.

Các giả thuyết định hướng phân tích mô tả theo từng workload. Protocol không định trước ngưỡng phần trăm phải đạt và không mặc định sẽ dùng kiểm định thống kê suy luận. Nếu bổ sung kiểm định, phải lập kế hoạch trước khi xem kết quả chính thức.

### 1.3. Tiêu chuẩn thành công

Nghiên cứu thành công khi simulator được kiểm chứng, phép so công bằng, kết quả truy vết được và kết luận nằm trong phạm vi bằng chứng. DAI không bắt buộc phải thắng D0. Các kết quả tương đương, kém hơn hoặc chỉ có lợi trong một số trường hợp vẫn phải được báo cáo.

## 2. Phạm vi mô hình

- Công cụ chính là simulator trace-driven bằng Python.
- Mô phỏng một cấp cache dữ liệu, xử lý tuần tự từng truy cập theo trace.
- Trace biểu diễn thao tác đọc/ghi bộ nhớ trong mô hình trạm cân; không yêu cầu chế tạo trạm cân thật.
- Trace tối thiểu có operation `R/W`, địa chỉ và kích thước truy cập.
- Xen kẽ truy cập nhiều sensor là một chuỗi access có kiểm soát; không tự được coi là mô phỏng CPU multicore, coherence hoặc thực thi đồng thời.
- Không suy ra trực tiếp timing phần cứng, area, điện năng hoặc khả năng đáp ứng thời gian thực từ thời gian chạy chương trình Python.

## 3. Các cấu hình và biến kiểm soát đã chốt

| Thành phần | Quy định |
|---|---|
| Data capacity | 4 KiB = 4.096 byte cho mọi thiết kế |
| Cache line | 32 byte |
| Tổng số line dữ liệu | 128 |
| Không gian địa chỉ | Địa chỉ logic 32-bit không dấu |
| Kích thước access | Đọc hoặc ghi 4 byte |
| Căn chỉnh | Địa chỉ chia hết cho 4; với cấu hình này access không vượt ranh giới line 32 byte |
| Write policy | Write-back + write-allocate |
| Replacement | LRU cho thiết kế có nhiều vị trí chứa hợp lệ; D0 không cần chọn victim |
| Prefetch | Tắt trong thí nghiệm chính |
| Bypass | Tắt trong thí nghiệm chính |
| Trạng thái đầu run | Cache rỗng; reset dữ liệu, valid/dirty, metadata và counters |
| Metadata | Báo cáo riêng tag, valid/dirty, replacement metadata và cấu trúc phụ của candidate |
| Nguồn input | Cùng file trace, cùng khoảng đo và cùng seed giữa các thiết kế |

**Nguyên tắc công bằng:** 4 KiB là dung lượng chứa dữ liệu, không phải tổng ngân sách bit phần cứng. Không tăng data capacity cho DAI. Metadata bổ sung không được giấu trong tên gọi “cache 4 KiB”; phải ghi rõ loại, số entry và chi phí lưu trữ ước tính.

Thí nghiệm chính tập trung vào mapping. Nếu AI đề xuất đổi write policy, thêm prefetch hoặc bypass, phải yêu cầu tách những thay đổi đó khỏi candidate chính. Không tự bổ sung các cơ chế này trong quá trình triển khai.

## 4. Các thiết kế so sánh

| ID | Thiết kế | Sets | Ways | Data capacity | Line | Replacement |
|---|---|---:|---:|---:|---:|---|
| D0 | Direct Mapping chuẩn | 128 | 1 | 4 KiB | 32 B | Vị trí duy nhất |
| D1 | Set-associative chuẩn | 64 | 2 | 4 KiB | 32 B | LRU |
| D2 | Set-associative chuẩn | 32 | 4 | 4 KiB | 32 B | LRU |
| DAI | Candidate được chọn sau P003 | Chưa chốt | Chưa chốt | 4 KiB | 32 B | Theo ràng buộc LRU; mô tả chính xác tập victim hợp lệ |

Với D0/D1/D2, dùng phép phân rã địa chỉ chuẩn:

```text
block_number = address // line_size
set_index    = block_number % number_of_sets
tag          = block_number // number_of_sets
```

DAI phải định nghĩa đầy đủ index, nhận diện block/tag, tập vị trí có thể chứa block, cách lookup và cách chọn victim. Không được coi hai block khác nhau là cùng dữ liệu chỉ vì có index trùng nhau.

D0 là baseline bắt buộc vì trực tiếp trả lời đề bài. D1/D2 giúp xác định tác động của associativity. Ví dụ, DAI hai way có index mới phải được đối chiếu với cả D0 và D1; không quy mọi cải thiện so D0 cho hàm index.

AI không bắt buộc phải phát minh kiến trúc mới. Một thiết kế đã biết được AI lựa chọn dưới các ràng buộc và được nhóm kiểm nghiệm đúng vẫn phù hợp với mục tiêu Q10.

## 5. Workload đã chốt

| ID | Workload | Các trường hợp phải có | Mục tiêu |
|---|---|---|---|
| W1 | Sequential stream | Đọc tuần tự; ghi tuần tự | Kiểm tra spatial locality và xử lý stream |
| W2 | Circular buffer | Buffer 1 KiB, 4 KiB, 16 KiB | Kiểm tra reuse khi working set nhỏ, bằng và lớn hơn cache |
| W3 | Moving average | Cửa sổ 8, 32, 128, 512, 2.048 mẫu; mỗi mẫu 4 B | Kiểm tra ảnh hưởng cửa sổ và working set |
| W4 | Bốn sensor xen kẽ | Mỗi buffer 1 KiB; xen kẽ đều và xen kẽ ngẫu nhiên | Kiểm tra tương tác giữa các stream |
| W5 | Conflict/stride stress | Luân phiên 2, 4, 8 block cách nhau 4 KiB | Tạo xung đột có kiểm soát tại D0 |

### 5.1. Quy tắc đặc tả workload

Trước khi tạo official traces, mỗi workload phải có đặc tả và manifest ghi rõ:

- Base address, vùng nhớ và kích thước buffer; các vùng không được chồng lấn ngoài chủ ý đã giải thích.
- Thứ tự đọc/ghi, tỷ lệ hoặc quy tắc phát sinh thao tác.
- Quy tắc tăng địa chỉ, quay vòng và chọn sensor.
- Với W3: kích thước buffer phải đủ cho cửa sổ lớn nhất; quy định mẫu hiện tại có nằm trong cửa sổ hay không và thứ tự đọc các mẫu.
- Với W4: quy tắc chọn sensor ngẫu nhiên, bố trí địa chỉ từng sensor và seed.
- Với W5: địa chỉ các block và quy tắc lặp. Phải kiểm tra chúng cùng index ở D0 theo cấu hình 4 KiB/line 32 B.
- Số access, phiên bản generator và checksum của trace.

Các chi tiết địa chỉ và quy tắc generator được hoàn thiện trong bước đặc tả workload và chốt trace, không lựa chọn dựa trên việc cấu hình nào thắng benchmark. Khi đưa đặc tính workload vào prompt AI, phải dùng thông tin từ đặc tả hoặc tập phát triển, không cung cấp kết quả chính thức chưa được phép dùng để chọn thiết kế.

### 5.2. Giới hạn diễn giải

W5 là stress test, không phải workload đại diện cho mọi trạm cân. Không chỉ sử dụng W5 để kết luận tổng quát. Tên “trạm cân” mô tả bối cảnh mô hình; không được trình bày trace tổng hợp như dữ liệu thực thu từ thiết bị nếu chưa có phép thu thực tế.

## 6. Quy mô và cách chạy thí nghiệm

### 6.1. Khởi động và khoảng đo

Mỗi trace dùng trong phép so chính có:

- **10.000 access khởi động:** cache cập nhật trạng thái bình thường; không cộng vào counters của khoảng đo.
- **100.000 access được đo:** dùng để tính metric và lưu kết quả chính thức.
- Tổng cộng **110.000 access bộ nhớ** cho một trace.

Không reset cache giữa khởi động và đo. Chỉ reset counters của khoảng đo tại ranh giới; giữ nguyên cache contents và metadata đã hình thành. Reset toàn bộ trạng thái trước run tiếp theo.

Access là thao tác bộ nhớ trong trace, không phải số mẫu cân hoặc số instruction. Nếu nghiên cứu cold-start, phải lập thí nghiệm riêng và không trộn với kết quả sau khởi động.

### 6.2. Số lần chạy và seed

- Mỗi trường hợp deterministic chạy một lần trên từng thiết kế; chạy lặp cùng input để kiểm tra tái lập không tạo thêm mẫu thống kê độc lập.
- Trường hợp ngẫu nhiên dùng **10 seed cố định từ 1 đến 10**. Trước mắt điều này áp dụng cho W4 xen kẽ ngẫu nhiên.
- Mọi thiết kế chạy cùng file trace và cùng khoảng khởi động/đo. Không sinh trace riêng cho từng cache.
- Không nhân seed cho workload không sử dụng ngẫu nhiên.

Với các trường hợp hiện liệt kê: W1 có 2 trace, W2 có 3 trace, W3 có 5 trace, W4 có 1 trace đều và 10 trace ngẫu nhiên, W5 có 3 trace. Nếu mỗi trường hợp chỉ dùng một bố trí địa chỉ đã chốt, tổng là **24 trace × 4 thiết kế = 96 run chính thức**. Đây là số run dự kiến, chưa bao gồm validation, debug hoặc thí nghiệm bổ sung được ghi riêng.

### 6.3. Trạng thái run và kết quả gốc

Mỗi run phải lưu tối thiểu:

| Nhóm thông tin | Nội dung |
|---|---|
| Nhận diện | Run ID, design ID, workload/scenario ID, trace ID |
| Input | Đường dẫn/checksum trace, seed nếu có, config snapshot |
| Phiên bản | Simulator version hoặc commit, protocol version, DAI version |
| Phạm vi đo | Số access khởi động và số access đo |
| Kết quả | Accesses, hits, misses, read/write misses, evictions, dirty writebacks, line fills |
| Trạng thái | SUCCESS, FAIL hoặc INVALID; lý do nếu không hợp lệ |

Không chỉnh tay raw result. Failed/invalid run được giữ lại, ghi lý do và dùng run ID mới khi chạy lại. Nếu lỗi simulator ảnh hưởng nhiều cấu hình, xác định và chạy lại toàn bộ các run bị ảnh hưởng thay vì chỉ chạy lại trường hợp bất lợi.

## 7. Chỉ số và công thức

### 7.1. Chỉ số chính

**Miss rate** là chỉ số chính. Mỗi bảng phải có số access và số miss gốc để tính lại được.

```text
Miss rate = Misses / Accesses
Hit rate  = Hits / Accesses

Relative miss reduction (%) =
    (MR_D0 - MR_candidate) / MR_D0 × 100

Chênh lệch miss rate (điểm phần trăm) =
    (MR_D0 - MR_candidate) × 100
```

Trong công thức, MR có giá trị từ 0 đến 1. Relative miss reduction dương nghĩa là candidate giảm miss; âm nghĩa là tăng miss. Nếu MR_D0 bằng 0, ghi relative reduction là **N/A** và cung cấp chênh lệch tuyệt đối.

### 7.2. Chỉ số bổ sung và memory traffic

Theo dõi read/write misses, evictions, dirty writebacks và line fills riêng. Không đồng nhất mọi eviction với writeback: chỉ line dirty bị ghi trả mới tạo dirty writeback theo mô hình đã chọn.

```text
Estimated memory traffic trong khoảng đo (byte) =
    (Line fills + Dirty writebacks) × 32
```

Mô hình giả định mỗi line fill hoặc dirty writeback chuyển một line đầy đủ 32 byte. Với write-allocate, write miss nạp line theo cùng chính sách đã khai báo. Công thức không bao gồm băng thông metadata, giao thức coherence hoặc giao tiếp phần cứng ngoài mô hình.

Không flush tại ranh giới khởi động/đo. Nếu flush dirty lines sau khoảng đo, ghi traffic flush thành trường riêng; không cộng vào traffic chính khi các cấu hình chưa được so theo cùng quy tắc.

### 7.3. AMAT ước tính và sensitivity

```text
Estimated AMAT = Assumed hit time + Miss rate × Assumed miss penalty
```

Đơn vị là cycle/access theo mô hình giả định. Miss penalty trong công thức là chi phí bổ sung sau cache lookup; không cộng lại hit time bên trong penalty.

- Chạy sensitivity với miss penalty **20, 50 và 100 cycle**.
- Phép so chỉ hành vi miss có thể dùng hit time chung **1 cycle** và phải gắn nhãn đây là giả định chung.
- Kiểm tra bổ sung trường hợp candidate có hit time cao hơn D0; các giá trị giả định phải được ghi vào kế hoạch phân tích trước khi xem kết quả chính thức.
- Các mức hit time chưa được đo trên phần cứng, không được trình bày như latency thật của D0/D1/D2/DAI.
- Công thức AMAT đơn giản này không tự phản ánh đầy đủ writeback stalls, hàng đợi hoặc truy cập chồng lấp. Báo cáo traffic riêng và nêu giới hạn đó.

Không dùng thời gian chạy simulator Python làm thời gian truy cập cache phần cứng. AMAT là phân tích bổ sung, không thay thế kết quả miss rate và traffic.

## 8. Quy tắc phân tích và kết luận

- Báo cáo DAI tốt hơn, tương đương hoặc kém hơn theo từng workload và scenario.
- Trình bày D0/D1/D2/DAI cùng giá trị gốc, sau đó mới tính chênh lệch.
- Với 10 seed ngẫu nhiên, báo cáo kết quả từng seed và thống kê mô tả như trung bình, độ lệch chuẩn, min/max. Không chỉ giữ seed có lợi.
- Không gộp mọi trường hợp thành một con số “thắng chung” rồi bỏ qua kết quả theo workload. Nếu bổ sung chỉ số tổng hợp, phải nêu cách trọng số và giữ bảng chi tiết.
- Khi so tỷ lệ cải thiện, ghi baseline, metric, workload và cấu hình tương ứng.
- Phân biệt kết quả đo từ simulator với tham số do nhóm giả định và nhận xét giải thích của nhóm.
- Không kết luận nhanh hơn trên phần cứng, ít điện hơn hoặc đạt yêu cầu thời gian thực nếu chỉ có hit/miss và AMAT giả định.

## 9. Validation trước benchmark chính thức

| Test | Tình huống | Điều kiện đạt |
|---|---|---|
| T01 | Đọc cùng địa chỉ hai lần khi cache rỗng | Miss rồi hit |
| T02 | Hai block cùng index, truy cập luân phiên | D0 xung đột; 2-way giữ được cả hai sau khi nạp nếu không có truy cập khác |
| T03 | Set đầy rồi nạp block mới | Chọn đúng victim LRU |
| T04 | Loại line dirty | Dirty writeback tăng đúng; không tăng giả cho line clean |
| T05 | Địa chỉ sát ranh giới line | Tính block/index/tag đúng; ví dụ địa chỉ 28 và 32 thuộc hai line khác nhau |
| T06 | Circular buffer quay vòng | Generator quay về đúng đầu buffer, không truy cập ngoài vùng quy định |

Ngoài sáu test tối thiểu, DAI phải có test riêng cho hàm index, nhận diện block và tập vị trí/victim hợp lệ của thiết kế sau khi được chọn.

Đối chiếu **3–5 trace nhỏ** bằng tính tay độc lập hoặc Ripes với cấu hình tương thích. So counter theo cùng quy tắc; nếu công cụ không hỗ trợ write policy hoặc mapping tương ứng, không ép khớp một phép so không tương thích. Mọi khác biệt phải được giải thích bằng chính sách, cách đếm hoặc bug trước khi chạy chính thức.

Điều kiện vào official benchmark: các test áp dụng đều pass, có báo cáo kiểm chứng và có reviewer khác người viết simulator. Không sửa expected result chỉ để phù hợp với output chưa được giải thích.

## 10. Quy trình dùng AI và chốt DAI

### 10.1. P001 — Initial Proposal

Cung cấp protocol, đặc tính workload và ràng buộc cố định. Yêu cầu **ba phương án mapping**, giải thích cơ chế, ưu nhược điểm, overhead, trường hợp có thể tốt/kém và mô tả đủ rõ để triển khai. Không cung cấp kết quả official để AI lựa chọn.

### 10.2. P002 — Critical Review

Yêu cầu phân tích từng phương án về conflict, locality, sensitivity theo workload, metadata, khả năng lookup đúng và tính công bằng với D0/D1/D2. Loại các phương án vi phạm ràng buộc hoặc chưa thể mô tả rõ.

### 10.3. P003 — Final Selection

Chọn một candidate cuối, giải thích lý do và hoàn thiện đặc tả có thể triển khai. Không lựa chọn chỉ dựa trên lời khẳng định “AI sẽ thắng”.

### 10.4. Lưu transcript và design freeze

Lưu nguyên văn từng prompt/câu trả lời với ID, thời gian thực tế, model nếu giao diện cung cấp và file nguồn. Giữ bản gốc nếu viết thêm ghi chú phân tích.

Sau P003, tạo `AI_DESIGN_FREEZE.md` gồm:

- Design ID `DAI-v1` và protocol ID liên quan.
- Capacity, line size, số set/way hoặc tổ chức placement tương đương.
- Index/tag, lookup, insertion, victim selection, dirty handling và reset.
- Metadata bổ sung và cách ước tính dung lượng.
- Prompt/response IDs P001–P003.
- Thời điểm chốt thực tế, phiên bản nguồn/commit nếu đã có và checksum của các artefact liên quan.

Chưa tạo bản design freeze hoàn tất khi DAI chưa được chọn. Test nhỏ phục vụ debug/validation được phép, nhưng benchmark chính thức và kết quả dùng để lựa chọn không được đi trước design freeze.

Sau khi đã xem official results, không âm thầm đổi thiết kế mà vẫn gọi là DAI-v1. Sửa bug phải có nhật ký và xác định run bị ảnh hưởng. Thay đổi thiết kế phải có phiên bản mới và công bố quy trình, không viết lại lịch sử để giả định thiết kế đã được chốt từ trước.

## 11. Phân công ba thành viên

| Thành viên | Trách nhiệm chính | Kiểm tra chéo |
|---|---|---|
| Trương Tô Dân — QE210127 | Protocol, RQ, transcript AI, design freeze, claim–evidence và tính nhất quán báo cáo | Kiểm tra workload, run manifest và kết luận |
| Trần Châu Hoàng Nam — QE210145 | Simulator, cấu hình, counters, unit tests, công thức metric/AMAT | Kiểm tra đặc tả DAI và script phân tích |
| Dương Quốc Thịnh — QE210121 | W1–W5, manifests/seeds, runner, raw results, aggregate/plot và lưu bản transcript cùng nhóm | Kiểm tra validation bằng trace nhỏ và khả năng tái lập |

Một người có thể hỗ trợ nhiều phần nhưng owner không tự là người duy nhất duyệt artefact quan trọng của mình. Phân công không phải xác nhận các công việc đã hoàn thành.

## 12. Thứ tự triển khai và điều kiện chuyển bước

| Bước | Công việc | Đầu ra/điều kiện đạt |
|---|---|---|
| 1 | Chốt protocol | Văn bản hiện tại, phiên bản và thời điểm thực tế được lưu |
| 2 | P001–P003 | Ba phương án, phản biện và một lựa chọn cuối; transcript nguyên văn |
| 3 | Design freeze | `AI_DESIGN_FREEZE.md` mô tả đủ DAI-v1 |
| 4 | Triển khai và validation | Simulator, configs, test report và đối chiếu độc lập đạt |
| 5 | Chốt official traces | Generator specification, trace manifests, seed và checksum |
| 6 | Official benchmark | Cùng trace chạy D0/D1/D2/DAI; raw results và run manifest |
| 7 | Analysis và report | Script tổng hợp/biểu đồ, kết luận theo workload, claim–evidence |
| 8 | Reproducibility | Chạy lại một batch mẫu từ môi trường sạch và lưu báo cáo |

Không tạo mốc freeze hồi tố. Nếu một công việc đã được thực hiện trước văn bản này, ghi ngày thật, nguồn bằng chứng và ảnh hưởng tới tính độc lập của thí nghiệm.

## 13. Quản lý phiên bản và các chi tiết sẽ hoàn thiện

Người dùng đã chấp thuận phương án của protocol v1.0. Thư mục hiện tại chưa có lịch sử Git được xác nhận trong quá trình lập tài liệu, nên không ghi commit giả. Khi tạo repository, lưu protocol vào phiên bản đầu và tạo checksum; giữ bằng chứng chấp thuận và thứ tự các bước thực tế.

Các chi tiết chưa được xác định trong protocol nhưng phải hoàn thiện đúng giai đoạn:

| Chi tiết | Chốt tại đâu | Hạn hoàn thiện |
|---|---|---|
| Thiết kế và metadata cụ thể của DAI | `AI_DESIGN_FREEZE.md` | Sau P003, trước benchmark chính thức |
| Base address, thứ tự thao tác và quy tắc generator chi tiết | Workload specification | Trước official trace freeze; không chọn theo kết quả thắng/thua |
| File trace thực tế và checksum | Trace manifests | Trước official benchmark |
| Hit-time giả định cao hơn cho candidate trong sensitivity | Analysis plan/config | Trước khi xem official results |
| Phiên bản Python, dependency và nguồn simulator | Environment/run manifests | Trước official benchmark |

Mọi sửa đổi ảnh hưởng câu hỏi, workload, metric, baseline hoặc biến kiểm soát phải tạo phiên bản protocol mới, nêu lý do, ngày thay đổi và đã có kết quả chính thức hay chưa. Bổ sung chi tiết triển khai không được dùng để âm thầm đổi phạm vi đã chốt.

## 14. Checklist trước official benchmark

- [ ] Protocol có phiên bản và thời điểm lưu thực tế.
- [ ] P001–P003 và câu trả lời được lưu nguyên văn.
- [ ] DAI-v1 đã được mô tả đủ và chốt trước benchmark chính thức.
- [ ] D0/D1/D2/DAI cùng 4 KiB dữ liệu, line 32 B và write policy.
- [ ] Prefetch/bypass tắt trong thí nghiệm chính.
- [ ] Counters khởi động/đo tách đúng; cache không reset tại ranh giới đo.
- [ ] Sáu test tối thiểu và test riêng của DAI đều pass.
- [ ] Có 3–5 trace đối chiếu độc lập, khác biệt được giải thích.
- [ ] W1–W5 có đặc tả, manifests, seed khi cần và checksum.
- [ ] Cùng file trace được dùng cho mọi thiết kế.
- [ ] Quy tắc traffic, flush và sensitivity đã rõ.
- [ ] Mỗi run lưu đủ input, config, phiên bản, kết quả và trạng thái.
- [ ] Có reviewer khác owner cho các artefact quan trọng.
- [ ] Raw results được giữ nguyên; script tạo processed data và figures.

## 15. Tài liệu liên quan

- [Kế hoạch nghiên cứu RBL Q10](C:/Tai_Lieu_Hoc/CEA201/RBL/Ke_hoach_RBL_Q10_AI_Cache_Mapping.docx).
- [Tiêu chí lựa chọn tài liệu tham khảo](C:/Tai_Lieu_Hoc/CEA201/RBL/Tieu_chi_lua_chon_tai_lieu_tham_khao.md).
- [Tổng hợp chín bài báo tham khảo](C:/Tai_Lieu_Hoc/CEA201/RBL/Tong_hop_9_bai_bao_tham_khao_Q10.md).

Các con số cấu hình và quy mô trong protocol là lựa chọn thực nghiệm đã được chấp thuận cho Q10. Chúng không được trình bày như thông số bắt buộc do các bài tham khảo hoặc giảng viên quy định.
