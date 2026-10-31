# Tổng hợp và đánh giá 9 bài báo tham khảo cho đề tài Q10

**Đề tài:** AI-Assisted Cache Mapping for Continuous Data Streams.  
**Ngày tìm kiếm và đối chiếu:** 31/10/2026, giờ Việt Nam.  
**Khoảng xuất bản:** 01/01/2023–31/10/2026.  
**Căn cứ:** bộ tiêu chí trong `Tieu_chi_lua_chon_tai_lieu_tham_khao.md`; yêu cầu mới của nhóm nâng số lượng từ mức đề xuất 6–8 lên **9 bài**.

Tài liệu cung cấp hồ sơ công bố, tóm lược đóng góp, thiết lập đánh giá, kết quả có vị trí kiểm tra, đánh giá giới hạn và đề xuất sử dụng trong Q10. Mỗi hồ sơ gồm phần thông tin nghiên cứu và phần phân tích độc lập cho đề tài. Các đề xuất thí nghiệm trong phần phân tích **chưa phải kết quả thực nghiệm của nhóm hoặc kết luận của tác giả bài báo**. Không dùng số liệu của các công trình này thay cho benchmark Q10.

## Thành viên và phân công tìm kiếm

| Người tìm kiếm và phụ trách hồ sơ | MSSV | Bài được phân công | Trọng tâm |
|---|---|---|---|
| Trương Tô Dân | QE210127 | LIT-001–LIT-003 | Mapping, associativity và xung đột cache |
| Trần Châu Hoàng Nam | QE210145 | LIT-004–LIT-006 | Workload, phương pháp mô phỏng và chỉ số đánh giá |
| Dương Quốc Thịnh | QE210121 | LIT-007–LIT-009 | Học máy và chi phí quản lý cache |

Danh sách đã cập nhật theo thông tin nhóm còn ba thành viên. Tên ở cột trên là **phân công phụ trách tìm kiếm, đọc kiểm tra và trình bày**, không phải xác nhận rằng từng thành viên đã tự thực hiện phiên tìm kiếm này. Việc tìm kiếm và soạn bản tổng hợp hiện tại có AI hỗ trợ; từng người cần xác nhận phần phụ trách trước khi ghi vào nhật ký đóng góp cá nhân.

## Phương pháp tìm kiếm và sàng lọc

Đây là tổng quan có mục tiêu cho bài RBL, không phải systematic literature review và không tuyên bố bao phủ toàn bộ nghiên cứu giai đoạn 2023–2026. Google Scholar được xem là công cụ phát hiện nguồn; chứng cứ công bố lấy từ DOI, trang tạp chí, hội nghị, cơ quan nghiên cứu và bản toàn văn do tác giả cung cấp. Không coi việc xuất hiện trong kết quả tìm kiếm là bằng chứng đã phản biện.

Các cụm tìm kiếm đã sử dụng gồm `cache indexing mapping conflict 2023 2024 2025 paper`, `cache replacement machine learning 2023 2024 2025 MICRO ISCA`, `streaming cache bypass processor`, và tên chính xác của các ứng viên. Sau khi tìm được bài, đối chiếu tác giả, năm, venue, DOI và khả năng đọc toàn văn; đọc các phần thiết kế, phương pháp và kết quả liên quan. Bản PDF công khai lấy từ máy chủ nhà xuất bản hoặc trang tác giả/trường, không lấy từ kho chia sẻ trái phép.

**Kết quả chọn:** 9 công trình khác nhau, gồm 3 bài liên quan trực tiếp tới mapping/xung đột; 3 bài hỗ trợ workload, kiểm soát biến và đánh giá chi phí; 3 bài về ML/quản lý cache. Tám bài nghiên cứu cache bộ xử lý; LIT-009 nghiên cứu cache phần mềm và được chọn vì đóng góp trực tiếp về ML và dòng truy cập. LIT-005 và LIT-006 nghiên cứu cache micro-op/lệnh, nên chỉ chuyển giao phương pháp, không chuyển nguyên số liệu sang cache dữ liệu trạm cân.

### Các ứng viên không đưa vào tập 9 bài

| Ứng viên hoặc nhóm kết quả | Quyết định và lý do |
|---|---|
| MESA: Reducing Cache Conflicts by Integrating Static and Run-Time Methods | Loại khỏi tập chính: bài cũ hơn 2023 dù ngày tải/lập chỉ mục trên web có thể mới. |
| Randomized Cache Placement for Eliminating Conflicts | Loại khỏi tập chính: công trình cũ; không dùng năm cập nhật tệp thay năm công bố. |
| A Survey of Cache Bypassing Techniques | Loại khỏi tập chính: xuất bản năm 2016. |
| RECAST: Mitigating Conflict-Based Cache Attacks Through Fine-Grained Dynamic Mapping | Có liên quan, nhưng chưa lấy được toàn văn hợp pháp để kiểm tra đủ sâu trong phiên này. Không dùng abstract để giả định đã đọc toàn bài. |
| Reinforcement Learning-Based Cache Replacement Policies for Multicore Processors | Có liên quan, nhưng đường toàn văn IEEE không đọc được trong phiên kiểm tra; chưa chọn vào tập chính. |
| HBPB, applying reuse distance to improve cache efficiency proactively | Có liên quan, nhưng chưa lấy được toàn văn hợp pháp của phiên bản tạp chí trong phiên này. |
| COBRRA: COntention-aware cache Bypass with Request-Response Arbitration | Có liên quan; chưa lấy được bản toàn văn trực tiếp từ nhà xuất bản/tác giả, nên không lấy bản xem trước ở bên thứ ba làm căn cứ đủ điều kiện. |
| LSTM-CRP: Algorithm-Hardware Co-Design and Implementation of Cache Replacement Policy Using Long Short-Term Memory | Có liên quan; trang toàn văn/PDF bị từ chối truy cập trong phiên này. Không gán trạng thái đạt yêu cầu đọc toàn văn. |
| Các bài cache video/CDN hoặc KV cache LLM | Không chọn chỉ vì có từ “streaming/cache”; mục tiêu, đơn vị dữ liệu và đường truy cập khác phạm vi cache CPU của Q10. |

### Giới hạn kiểm tra tình trạng công bố

Không phát hiện thông báo rút bài/đính chính trong các trang công bố và kết quả tra cứu đã kiểm tra. Các bản ghi Crossref lấy được cho LIT-001, 002, 003, 006, 007, 008 không có mục `update-to` hoặc quan hệ cập nhật được đăng ký. Điều này **không tương đương bảo đảm tuyệt đối chưa từng có vấn đề**: trạng thái nhà xuất bản có thể thay đổi, và Crossref không phải nguồn đăng ký duy nhất. LIT-004, 005 được xác minh bằng nguồn công bố/toàn văn; truy vấn Crossref ban đầu bị giới hạn tần suất. LIT-009 được xác minh tại Dagstuhl, không coi phản hồi 404 từ Crossref là DOI không tồn tại. Trước khi nộp báo cáo, người phụ trách mở lại trang DOI để kiểm tra thông báo mới.

## Danh mục nhanh

| ID | Tên rút gọn | Năm/venue | Vai trò trong Q10 | Người phụ trách |
|---|---|---|---|---|
| LIT-001 | Randomizing Set-Associative Caches | 2024, IEEE Transactions on Computers | Mapping và chi phí đổi mapping | Trương Tô Dân |
| LIT-002 | The Maya Cache | 2024, ISCA | Tag/data, associativity và ngân sách bộ nhớ | Trương Tô Dân |
| LIT-003 | Scatter and Split Securely | 2023, IEEE S&P | Skewed mapping và đánh đổi mục tiêu | Trương Tô Dân |
| LIT-004 | Tartan | 2024, ISCA | Workload có ý nghĩa và tách đóng góp | Trần Châu Hoàng Nam |
| LIT-005 | From Optimal to Practical | 2025, HPCA | Oracle, profile và baseline đúng | Trần Châu Hoàng Nam |
| LIT-006 | EMISSARY | 2023, ISCA | Chi phí miss khác số lượng miss | Trần Châu Hoàng Nam |
| LIT-007 | CHROME | 2024, HPCA | RL, phối hợp policy và metadata | Dương Quốc Thịnh |
| LIT-008 | PAIC | 2023, JCST | ML, prefetch và kiểm soát baseline | Dương Quốc Thịnh |
| LIT-009 | Sketching the Path to Efficiency | 2024, OPODIS 2023 | ML theo cửa sổ và chi phí thống kê | Dương Quốc Thịnh |

## LIT-001 — Randomizing Set-Associative Caches Against Conflict-Based Cache Side-Channel Attacks

### Hồ sơ và nội dung nghiên cứu

- **Người tìm kiếm/phụ trách:** Trương Tô Dân — QE210127.
- **Tác giả:** Wei Song, Zihan Xue, Jinchi Han, Zhenzhen Li, Peng Liu.
- **Cơ quan:** Institute of Information Engineering, CAS; University of Chinese Academy of Sciences; Pennsylvania State University.
- **Công bố:** IEEE Transactions on Computers, 73(4), 1019–1033; online 08/01/2024, số tháng 04/2024. Bài tạp chí đã phản biện.
- **Nguồn:** [DOI](https://doi.org/10.1109/TC.2024.3349659), [toàn văn tác giả](https://wsong83.github.io/publication/comparch/tc2024.pdf), [hồ sơ Penn State](https://pure.psu.edu/en/publications/randomizing-set-associative-caches-against-conflict-based-cache-s/).

Bài thay đổi index của LLC set-associative để chống tấn công xung đột, kết hợp hash, remapping và phát hiện tấn công. Thiết kế được triển khai trên Rocket-Chip, kiểm tra bằng Spike và FPGA chạy Linux. SPEC CPU2006 cung cấp đánh giá hiệu năng; kết quả báo cáo overhead runtime trung bình dưới 1%. Đây là chi phí phòng vệ, không phải mức tăng tốc so với Direct Mapping. Vị trí kiểm tra: phần V–VI, Hình 13 và 16–18 trong toàn văn. Mã triển khai được dẫn tại [kho dự án](https://github.com/comparch-security/chipyard-random-llc).

### Phân tích độc lập cho Q10

**Lý do chọn.** Trong Q10, câu hỏi đầu tiên cần trả lời là thay đổi vị trí đặt block có thể giải quyết vấn đề gì. Ta có thể thiết kế một trace nhỏ gồm hai vùng nhớ cách nhau đúng dung lượng cache, luân phiên đọc chúng và quan sát cùng một index bị sử dụng lặp lại. Trường hợp ấy giúp tách xung đột do quy tắc ánh xạ khỏi thiếu dung lượng toàn cục. Nguồn này phù hợp để mở phần thảo luận về các thiết kế index khác nhau, nhưng nhóm phải tự chứng minh hiện tượng bằng simulator của mình. Một bài về bảo mật không thay thế được bằng chứng về workload cân.

**Cách chuyển thành thí nghiệm.** Nhóm nên bắt đầu bằng D0 với index modulo thông thường và một candidate dùng phép trộn các bit địa chỉ. Cấu hình phải ghi rõ bit nào được dùng, cách tính tag và cách tìm lại block. Nếu dùng XOR, cần kiểm tra cả những địa chỉ chỉ khác ở phần bit cao, những địa chỉ sát ranh giới line và những địa chỉ từng xung đột dưới D0. Mỗi test nên xuất đường đi gồm block number, index, tag và hit/miss. Nhờ vậy, khi một trace cải thiện, nhóm có thể chỉ ra nguyên nhân là phân bố truy cập thay đổi, thay vì chỉ nhìn một con số tổng cuối cùng.

**Biến cần giữ cố định.** Một thiết kế đổi index có thể đồng thời làm thay đổi số set hoặc associativity nếu triển khai thiếu cẩn thận. Khi đó, nhóm không còn biết hiệu quả đến từ đâu. Đề xuất cho Q10 là dùng cùng data capacity 4 KiB và line 32 B theo kế hoạch hiện tại, giữ write policy và quy tắc khởi tạo giống nhau. Nếu so một candidate hai way với D0 một way, phải có thêm D1 hai way dùng index chuẩn để tách tác động của associativity. Nếu không có đối chứng này, báo cáo chỉ được kết luận về toàn bộ candidate, chưa thể quy công cho hàm hash.

**Chi phí đổi mapping cần được tính riêng.** Trong simulator học thuật, thay một phép modulo bằng một hàm khác có thể chỉ thêm vài dòng code, nhưng thời gian chạy chương trình Python không đại diện cho độ trễ mạch cache. Nhóm nên ghi rõ simulator chỉ kiểm tra hành vi truy cập và dùng mô hình latency giả định nếu tính AMAT. Nếu candidate thay đổi index theo thời gian, các block đang nằm trong cache phải được di chuyển, vô hiệu hóa hoặc có cơ chế tra cứu tương thích. Bỏ qua bước đó có thể tạo hit giả hoặc làm mất dữ liệu dirty. Đây là lý do nên ưu tiên candidate tĩnh cho phiên bản đầu của Q10.

**Workload nên sử dụng.** W5 tạo xung đột có chủ đích là nơi tốt để kiểm tra tính đúng của quy tắc ánh xạ, nhưng chưa đủ để chứng minh ứng dụng thực tế. Cần chạy thêm W1 tuần tự để phát hiện tác dụng phụ lên locality, W2 buffer vòng để kiểm tra tái sử dụng và W4 nhiều sensor với các base address khác nhau. Với W4, nên thử cả buffer được căn chỉnh gây va chạm và buffer được đặt lệch nhau. Nếu chỉ trường hợp căn chỉnh đặc biệt có lợi, kết luận phải giới hạn vào tình huống đó. Các trace ngẫu nhiên cần seed và manifest để người khác lặp lại.

**Cách đưa vào báo cáo.** Nguồn này nên xuất hiện trong Literature Review ở nhóm “mapping và conflict”, rồi được nối tới quyết định lựa chọn đối chứng trong Methodology. Nhóm có thể lập một bảng phân biệt mục tiêu của công trình tham khảo với mục tiêu Q10: chống rò rỉ thông tin so với đánh giá hành vi miss trên dữ liệu cân. Khi giải thích kết quả, dùng chính trace của nhóm và kiểm tra phân bố truy cập theo set, số eviction và số lần dữ liệu được tái sử dụng. Không sử dụng mức overhead của công trình như dự đoán cho bộ xử lý hoặc mạch 4 KiB của nhóm.

**Giới hạn khi vận dụng.** Q10 chưa có mô hình kẻ tấn công, khóa bí mật, nhiều lõi chạy Linux hay kiểm chứng phần cứng. Vì thế, thêm randomization không tự động tạo ra một đóng góp về bảo mật. Nếu triển khai hash đơn giản, nhóm phải gọi đúng đó là candidate mapping được đánh giá trong mô phỏng. Một kết quả miss rate tốt cũng chưa chứng minh điện năng giảm, bởi đường tìm kiếm và metadata có thể tăng. Phần Discussion nên nói rõ điều đã đo và điều còn cần mô hình khác để xác nhận; đây là cách giữ kết luận trong phạm vi bằng chứng.

### Kết luận riêng

**Randomizing Set-Associative Caches Against Conflict-Based Cache Side-Channel Attacks** được chọn làm nguồn chính cho thảo luận về ánh xạ và chi phí thay đổi index. Giá trị áp dụng là xây dựng câu hỏi, đối chứng và test đúng cho Q10; công trình không cung cấp bằng chứng trực tiếp rằng candidate AI của nhóm sẽ nhanh hơn D0. Người phụ trách cần kiểm tra các hình đã chỉ ra và ghi lại cấu hình trước khi sử dụng số liệu trong báo cáo.

## LIT-002 — The Maya Cache: A Storage-efficient and Secure Fully-associative Last-level Cache

### Hồ sơ và nội dung nghiên cứu

- **Người tìm kiếm/phụ trách:** Trương Tô Dân — QE210127.
- **Tác giả:** Anubhav Bhatla, Navneet, Biswabandan Panda — Indian Institute of Technology Bombay.
- **Công bố:** ISCA 2024, trang 32–44; hội nghị bắt đầu 29/06/2024. Bài hội nghị đã phản biện.
- **Nguồn:** [DOI](https://doi.org/10.1109/ISCA59077.2024.00013), [toàn văn tại IIT Bombay](https://www.cse.iitb.ac.in/~biswa/ISCA2024.pdf).

Maya tách tag/data, sử dụng thông tin reuse và eviction toàn cục để tạo hành vi bảo mật gần fully-associative. Đánh giá dùng ChampSim, baseline tám lõi, LLC 16 MiB, 16-way, line 64 B; workload từ SPEC CPU2017 và GAP. Bảng X báo cáo storage −2% và performance +0,20% so baseline trong thiết lập của bài. Đây không phải phép so cùng data capacity như Q10. Kiểm tra thiết kế tại phần III, phương pháp/kết quả tại phần V và Bảng V–X. [Artifact tác giả](https://github.com/AnubhavBhatla/maya-cache) hỗ trợ tái lập.

### Phân tích độc lập cho Q10

**Lý do chọn.** Trong một nghiên cứu cache nhỏ, cụm từ “cùng kích thước cache” có thể bị dùng theo hai nghĩa khác nhau: cùng dung lượng chứa dữ liệu hoặc cùng tổng số bit phần cứng. Với Q10, kế hoạch hiện chọn cách thứ nhất làm điều kiện kiểm soát. Nhóm cần ghi điều đó ngay từ đầu, đồng thời theo dõi tag, valid, dirty và thông tin thay thế như chi phí bổ sung. Nguồn này phù hợp để đặt câu hỏi về ngân sách và tính công bằng, bởi người đọc báo cáo rất dễ hiểu nhầm rằng mọi cấu hình ghi “4 KiB” đều tốn tài nguyên như nhau.

**Đối chứng phù hợp.** D0, D1 và D2 nên được định nghĩa bằng số set, số way và kích thước line, không chỉ bằng tên. Với 4 KiB và line 32 B, số line dữ liệu là 128; phân thành 128 set một way, 64 set hai way hoặc 32 set bốn way. Việc thêm way không làm tăng số line dữ liệu nhưng có thể thay đổi số bit tag và metadata thay thế. Nhóm có thể lập một bảng chi phí logic ước tính, ghi công thức thay vì đưa ra số area hoặc power không có mô hình. Cách này giúp phân biệt hiệu quả lưu giữ dữ liệu với độ phức tạp thực hiện.

**Cách kiểm tra thông tin reuse.** Với workload cân, một mẫu có thể được ghi một lần rồi được đọc nhiều lần khi tính moving average; một bản ghi log có thể chỉ được ghi rồi không dùng lại trong khoảng đo. Nhóm có thể gán vùng nhớ theo chức năng để đếm riêng các nhóm truy cập ấy. Đây là một đề xuất phân tích của Q10, không phải tuyên bố rằng mô hình của bài báo trùng với trạm cân. Nếu nhận thấy phần lớn miss đến từ dữ liệu không tái sử dụng, tăng associativity có thể không giải quyết được nguyên nhân. Kết quả đó vẫn có giá trị dù candidate AI không thắng.

**Không mở rộng simulator thiếu kiểm soát.** Một cấu trúc cache có nhiều trạng thái đòi hỏi định nghĩa rất chính xác thế nào là hit. Trong Q10, một block chỉ nên tính là data hit khi dữ liệu cần thiết thực sự có sẵn theo mô hình đã khai báo. Nếu sau này nhóm thêm bảng lịch sử, việc tìm thấy địa chỉ trong bảng đó không được tính thành cache hit. Cần phân biệt metadata lookup, data lookup và yêu cầu xuống memory. Quy tắc này đặc biệt quan trọng khi dùng AI hỗ trợ viết code: một biến tên `found` có thể vô tình gộp hai sự kiện khác nhau và làm hit rate tăng giả.

**Thiết kế thí nghiệm gọn cho ba người.** Nhóm không cần tái hiện một LLC bảo mật phức tạp để dùng nguồn này có ích. Tô Dân có thể chịu trách nhiệm định nghĩa ngân sách và kiểm tra bảng cấu hình; Hoàng Nam cài đặt counter đúng; Quốc Thịnh sinh trace cho mẫu cân, hệ số hiệu chỉnh và log. Một reviewer khác owner phải xác nhận kết quả của một trace nhỏ. Nếu candidate đòi thêm nhiều cấu trúc mới, nhóm nên ghi thành hướng phát triển và hoàn thành phép so mapping cốt lõi trước. Phạm vi vừa sức giúp bằng chứng chắc hơn và giảm thời gian sửa simulator.

**Phân tích kết quả nên đi xa hơn hit rate.** Nhóm có thể trình bày số miss trên từng vùng nhớ, tổng số eviction và dirty writeback. Hai thiết kế có hit rate giống nhau nhưng loại bỏ các line khác nhau có thể tạo memory traffic khác nhau. Một phép đếm tổng byte đọc/ghi xuống memory, với giả định line transfer rõ ràng, sẽ bổ sung ngữ cảnh cho kết quả. Tuy nhiên, chỉ số đó vẫn là traffic trong mô hình; không được đổi tên thành điện năng hay thời gian thực. Các tuyên bố phần cứng cần thêm công cụ ước lượng hoặc phép đo riêng, vượt phạm vi hiện tại.

**Cách sử dụng trong Literature Review.** Khi so sánh các bài, nên có cột “ngân sách được giữ cố định” bên cạnh cột “baseline”. Việc này cho phép giải thích tại sao một mức cải thiện công bố không thể mang sang nghiên cứu khác. Trong Q10, nếu AI đề xuất tăng dung lượng để giảm miss, đó là một phương án không đáp ứng câu hỏi cùng capacity và phải sửa trước design freeze. Nếu đề xuất đổi mapping nhưng cần bảng phụ, nhóm vẫn có thể thử, miễn dung lượng dữ liệu giữ nguyên và bảng phụ được báo cáo minh bạch. Đây là quyết định phương pháp của nhóm, không phải sao chép thiết kế Maya.

### Kết luận riêng

**The Maya Cache: A Storage-efficient and Secure Fully-associative Last-level Cache** được chọn để củng cố phần đánh đổi giữa tổ chức cache, metadata và ngân sách. Q10 nên học cách khai báo điều kiện so sánh và đếm sự kiện chính xác; không triển khai toàn bộ Maya hoặc dùng kết quả của bài để khẳng định hiệu quả cho trạm cân. Kết luận riêng của nhóm phải tiếp tục dựa trên D0/D1/D2/DAI cùng input và cùng data capacity.

## LIT-003 — Scatter and Split Securely: Defeating Cache Contention and Occupancy Attacks

### Hồ sơ và nội dung nghiên cứu

- **Người tìm kiếm/phụ trách:** Trương Tô Dân — QE210127.
- **Tác giả:** Lukas Giner, Stefan Steinegger, Antoon Purnal, Maria Eichlseder, Thomas Unterluggauer, Stefan Mangard, Daniel Gruss.
- **Cơ quan:** Graz University of Technology; imec-COSIC, KU Leuven; Intel.
- **Công bố:** IEEE Symposium on Security and Privacy 2023, trang 2273–2287; hội nghị tháng 05/2023, hồ sơ TU Graz ghi phát hành tháng 07/2023. Bài đã phản biện.
- **Nguồn:** [DOI](https://doi.org/10.1109/SP46215.2023.10179440), [toàn văn tác giả](https://antoonpurnal.github.io/files/pdf/SassCache.pdf), [hồ sơ TU Graz](https://tugraz.elsevierpure.com/en/publications/scatter-and-split-securely-defeating-cache-contention-and-occupan/).

SassCache dùng skewed mapping theo miền bảo mật. Phần 8 đánh giá gem5 và trace: cấu hình gem5 có L2 1 MiB, 16-way, line 64 B; workload gồm MiBench, lmbench, scimark2, GAP và đánh giá SPEC2017 bằng simulator riêng. Mục tiêu chính là phòng vệ; hit rate có thể giảm. Kiểm tra phần 4–6 về thiết kế và phần 8 về hiệu năng. Không diễn giải thay đổi hit rate thành cùng tỷ lệ thay đổi runtime.

### Phân tích độc lập cho Q10

**Lý do chọn.** Đề tài Q10 có nguy cơ bắt đầu từ giả định rằng một mapping phức tạp hơn luôn tốt hơn. Một tổng quan tốt cần có nguồn giúp nhóm xem xét nhiều mục tiêu và khả năng đánh đổi. Trong báo cáo của nhóm, “tốt hơn” phải được định nghĩa bằng metric cụ thể: giảm miss, giảm traffic hay giảm AMAT ước tính. Nếu không nêu mục tiêu, một phương án được lựa chọn vì lý do khác có thể bị xếp hạng sai. Nguồn này được dùng để xây dựng cách đọc phê bình đó, không để mở thêm một đề tài tấn công bảo mật cho nhóm.

**Cần phân biệt skewed mapping và tăng way.** Trong kế hoạch Q10, D1 và D2 là các đối chứng set-associative chuẩn. Nếu AI đề xuất nhiều hàm ánh xạ cho những bank khác nhau, nhóm cần mô tả đó là thay đổi tổ chức placement, không chỉ gọi chung “4-way”. Trong tài liệu thiết kế, nên ghi với mỗi block: những vị trí nào được phép chứa nó, tra cứu qua những vị trí nào và chọn victim trong tập nào. Một sơ đồ nhỏ cùng hai ví dụ địa chỉ sẽ dễ kiểm tra hơn vài đoạn giải thích trừu tượng. Thiếu định nghĩa này có thể khiến hai thành viên triển khai hai thuật toán khác nhau.

**Bộ test nên kiểm tra cả mất và được.** Nhóm có thể tạo một trace mà D0 bị hai sensor tranh cùng index, rồi một trace mà các sensor nằm ở những vùng không xung đột. Cùng một candidate phải chạy cả hai. Tiếp theo, thêm trường hợp buffer nhỏ vừa cache và trường hợp working set lớn hơn cache. Nếu lợi ích chỉ xuất hiện ở trace stress, báo cáo cần giữ nguyên kết quả và giải thích điều kiện đó. Không nên loại trace thuận lợi cho D0 vì làm biểu đồ kém đẹp. Cách chọn workload này trực tiếp hỗ trợ H0 và giả thuyết cải thiện phụ thuộc access pattern của dự án.

**Tính công bằng còn phụ thuộc phần cache thực sự sử dụng được.** Giả sử nhóm tự đề xuất chia dung lượng cố định thành các vùng cho sensor và log. Dù tổng vẫn là 4 KiB, một sensor có thể bị giới hạn dung lượng hữu dụng trong khi vùng khác để trống. Thí nghiệm cần báo cáo tác động ấy, đặc biệt khi lưu lượng giữa các sensor không cân bằng. Nên có trace ba sensor ít hoạt động và một sensor hoạt động mạnh, bên cạnh trace cân bằng. Kết quả sẽ cho thấy việc chia vùng có phù hợp hay gây lãng phí trong mô hình nhóm. Đây là đề xuất kiểm chứng độc lập, chưa phải kết quả có sẵn.

**Giới hạn mô hình phải xuất hiện trước kết luận.** Simulator một cấp, xử lý tuần tự các lần đọc/ghi không mô tả đầy đủ sự tranh chấp của nhiều chương trình thực thi đồng thời. W4 interleaving trong dự án chỉ là chuỗi truy cập được xen kẽ theo quy tắc, không tự trở thành mô phỏng multicore hoặc multi-tenant. Nhóm nên dùng đúng tên đó trong báo cáo. Nếu muốn xét thời điểm đến, hàng đợi hoặc nhiều lõi, cần mở rộng mô hình và kiểm tra thêm. Với nguồn lực ba người, giữ phạm vi trace-driven rõ ràng sẽ giúp giải thích kết quả dễ hơn và tránh các tuyên bố chưa được đo.

**Cách đánh giá một kết quả âm.** Nếu candidate cho miss rate cao hơn D0 ở W1 nhưng thấp hơn ở W4, có thể trình bày hai kết quả cạnh nhau thay vì gộp thành một tỷ lệ thắng chung. Cần tính delta theo điểm phần trăm và mức giảm tương đối với mẫu số ghi rõ. Khi baseline có zero miss trong khoảng đo, mức giảm tương đối không xác định; nên dùng chênh lệch tuyệt đối hoặc ghi N/A. Những chi tiết nhỏ này giúp bảng tổng hợp có thể kiểm tra được và làm rõ rằng thiết kế được đánh giá theo nhiều trường hợp, không được chọn riêng theo tình huống thắng.

**Cách đưa nguồn vào báo cáo.** Trong Literature Review, nguồn này nên được đặt cạnh LIT-001 và LIT-002 để nhóm giải thích rằng cùng nghiên cứu mapping nhưng các tác giả tối ưu theo những ràng buộc khác nhau. Sau đó, Methodology của Q10 phải nêu riêng mục tiêu và giới hạn của nhóm. Phần Discussion có thể đối chiếu về phương pháp phân tích đánh đổi, nhưng không khẳng định candidate đơn giản của nhóm đạt mức bảo mật tương đương. Một danh mục nguồn có ý nghĩa là danh mục tạo được quyết định thực nghiệm rõ ràng; số lượng tên kiến trúc chỉ là phần phụ của câu chuyện nghiên cứu.

### Kết luận riêng

**Scatter and Split Securely: Defeating Cache Contention and Occupancy Attacks** được chọn làm nguồn chính liên quan tới skewed mapping và đánh đổi. Bài giúp Q10 đặt câu hỏi chặt chẽ về placement, dung lượng hữu dụng và mục tiêu tối ưu. Nhóm nên giữ bài trong tổng quan, nhưng giới hạn phần vận dụng vào thiết kế đối chứng và thảo luận; các số liệu bảo mật hoặc hit rate của nguồn không phải kết quả của trạm cân.

## LIT-004 — Tartan: Microarchitecting a Robotic Processor

### Hồ sơ và nội dung nghiên cứu

- **Người tìm kiếm/phụ trách:** Trần Châu Hoàng Nam — QE210145.
- **Tác giả:** Mohammad Bakhshalipour, Phillip B. Gibbons — Carnegie Mellon University.
- **Công bố:** ISCA 2024, trang 548–565; hội nghị 29/06–03/07/2024. Bài hội nghị đã phản biện. Trang bìa tải từ ACM ghi thêm ngày phát hành 23/07/2025; không nhầm ngày tải 19/03/2026 thành năm nghiên cứu.
- **Nguồn:** [DOI](https://doi.org/10.1109/ISCA59077.2024.00047), [toàn văn CMU](https://www.pdl.cmu.edu/PDL-FTP/associated/Tartan-ISCA24.pdf).

Tartan nghiên cứu CPU cho robotics; thành phần FCP kết hợp điều chỉnh indexing và metadata thay thế để giảm tranh chấp trong ứng dụng. Đánh giá dùng workload robot có pipeline perception–planning–control. Phần VIII-D báo cáo FCP đạt tối đa khoảng 8% cải thiện hiệu năng và 18% giảm L2 misses trong thí nghiệm của bài. Không gán speedup toàn Tartan cho riêng cache. Vị trí đọc: phần III-A, VII và VIII-D; Hình 5 về FCP, Bảng I về workload. Mức liên quan trực tiếp là quản lý cache và ngữ nghĩa truy cập, không phải mô hình trạm cân hoàn chỉnh.

### Phân tích độc lập cho Q10

**Lý do chọn.** Trạm cân không chỉ tạo ra một chuỗi số mà còn thực hiện nhiều bước xử lý. Nhóm có thể mô hình hóa ghi mẫu mới, đọc hệ số hiệu chỉnh, đọc cửa sổ lọc, cập nhật thống kê và ghi log thành các vùng địa chỉ khác nhau. Cách xây dựng này giúp giải thích tại sao một dữ liệu được tái sử dụng còn dữ liệu khác chủ yếu đi qua bộ nhớ. So với trace ngẫu nhiên không có ngữ nghĩa, một pipeline có mô tả rõ sẽ làm câu hỏi nghiên cứu dễ hiểu và hỗ trợ kiểm tra tính hợp lý của workload. Đây là cách thiết kế đề xuất cho Q10, chưa phải dữ liệu quan sát từ thiết bị thật.

**Mô hình workload nên đủ chi tiết để kiểm tra.** Mỗi sensor cần có base address, số mẫu trong buffer, kích thước mẫu và tần suất tạo mẫu. Bộ lọc cần có độ rộng cửa sổ và thứ tự đọc; logging cần có kích thước bản ghi và chu kỳ ghi. Generator nên xuất cùng lúc trace và bản mô tả tham số. Không nên sinh một lượng lớn địa chỉ rồi đặt tên “trạm cân” sau khi chạy benchmark. Khi input gắn với pipeline, người reviewer có thể kiểm tra một chu kỳ bằng tay và phát hiện lỗi đọc thiếu, ghi thừa hoặc quay buffer sai trước khi simulator được dùng chính thức.

**Tách đóng góp là yêu cầu quan trọng.** Nếu candidate DAI vừa thay mapping, vừa thêm bypass và đổi replacement, kết quả thắng D0 không cho biết thay đổi nào tạo lợi ích. Nhóm nên giữ phiên bản so sánh chính chỉ thay yếu tố đã chốt trong câu hỏi, hoặc bổ sung một thí nghiệm loại bỏ từng thành phần. Chẳng hạn, có thể chạy index chuẩn với LRU, index mới với LRU, rồi mới chạy index mới với policy phụ. Chỉ thực hiện bước thứ ba nếu nằm trong phạm vi đã freeze. Việc này giúp báo cáo giải thích cơ chế cải thiện và tránh việc AI đề xuất một gói giải pháp quá rộng để kiểm chứng.

**Ngữ nghĩa dữ liệu không được tạo ưu thế không công bằng.** Giả sử DAI được biết trước vùng nào là log ít reuse, còn baseline chỉ nhận địa chỉ. Nhóm phải công bố thông tin bổ sung đó trong cấu hình và trong phần giới hạn. Nếu muốn so riêng mapping, tốt nhất mọi thiết kế nhận cùng thông tin đầu vào. Nếu nghiên cứu rộng hơn về policy có ngữ nghĩa, cần thêm đối chứng được cấp cùng nhãn dữ liệu. Mục đích là phân biệt lợi ích của thuật toán với lợi ích của thông tin mà chỉ một phía được cung cấp. Một bảng input capabilities sẽ giúp người đọc đánh giá điều kiện này nhanh chóng.

**Workload phải có trường hợp thay đổi.** Cấu hình bốn sensor đồng tốc chưa đại diện cho mọi tình huống. Nhóm có thể thử số sensor khác nhau, khoảng ghi log khác nhau và cửa sổ lọc tăng từ nhỏ lên lớn. Mỗi thay đổi nên có lý do: thay working set, thay mức xen kẽ hoặc thay tỷ lệ đọc/ghi. Không cần chạy một ma trận khổng lồ nếu không có thời gian phân tích; nên ưu tiên vài biến tạo khác biệt cơ chế rõ ràng. Giữ các trace dùng để chọn candidate tách khỏi official traces sẽ giúp kết quả có ý nghĩa hơn một phép tinh chỉnh theo bộ dữ liệu đã xem trước.

**Chỉ số nào phù hợp với mô hình hiện tại.** Với simulator không có pipeline CPU, nhóm có thể đo hit/miss, số line transfer, dirty eviction và phân bố miss theo vùng nhớ. Không thể suy ra throughput xử lý cân hoặc deadline đáp ứng chỉ từ các counter đó. Nếu muốn ước tính AMAT, cần khai báo latency giả định và chạy sensitivity thay vì chọn một giá trị khiến DAI thắng. Một biểu đồ miss rate cùng bảng traffic sẽ đáng tin hơn câu “hệ thống thời gian thực nhanh hơn” khi chưa có mô hình thời gian thực. Điều này cũng giúp nhóm xác định ranh giới giữa minh họa kiến trúc và đo trên thiết bị.

**Cách sử dụng trong báo cáo và phân công.** Hoàng Nam nên dùng hồ sơ này để xây phần Experimental Setup: sơ đồ pipeline, ánh xạ vùng nhớ và bảng tham số generator. Quốc Thịnh có thể kiểm tra trace đầu ra so với bảng đó, còn Tô Dân kiểm tra giả thuyết từng workload. Trong Results, mỗi biểu đồ cần nối tới một câu hỏi cụ thể như mức xen kẽ ảnh hưởng conflict ra sao. Khi viết Discussion, nhóm so sánh cách đặt vấn đề và phương pháp tách thành phần, không so trực tiếp phần trăm speedup của robotics với phần trăm miss của dữ liệu cân. Hai chỉ số khác nhau không thể xếp cạnh nhau như cùng một thước đo.

### Kết luận riêng

**Tartan: Microarchitecting a Robotic Processor** được chọn vì hỗ trợ thiết kế workload có ngữ nghĩa và đánh giá từng thành phần riêng. Giá trị lớn nhất cho Q10 là cách biến bối cảnh ứng dụng thành chuỗi truy cập có thể kiểm tra. Nhóm nên vận dụng vào generator và các đối chứng; không coi kết quả của toàn bộ bộ xử lý robot là hiệu quả riêng của cache hay là bằng chứng cho phần cứng trạm cân.

## LIT-005 — From Optimal to Practical: Efficient Micro-op Cache Replacement Policies for Data Center Applications

### Hồ sơ và nội dung nghiên cứu

- **Người tìm kiếm/phụ trách:** Trần Châu Hoàng Nam — QE210145.
- **Tác giả:** Kan Zhu, Yilong Zhao, Yufei Gao, Peter Braun, Tanvir Ahmed Khan, Heiner Litz, Baris Kasikci, Shuwen Deng.
- **Cơ quan:** University of Washington, UC Berkeley, Tsinghua University, UC Santa Cruz, Columbia University.
- **Công bố:** HPCA 2025, trang 716–731, tháng 03/2025; bài hội nghị đã phản biện.
- **Nguồn:** [DOI](https://doi.org/10.1109/HPCA61900.2025.00060), [trang phòng thí nghiệm](https://www.thu-haslab.org/publication/co-public/2025-from-optimal-to-practical/), [toàn văn](https://www.thu-haslab.org/publication/co-public/2025-from-optimal-to-practical/19_HPCA2025_micro-op_cache.pdf).

Bài đề xuất FLACK offline và FURBYS thực dụng cho micro-op cache. Đánh giá dùng Scarab, mô hình gần AMD Zen3, 11 ứng dụng datacenter. FURBYS giảm miss trung bình 14,34% so LRU; abstract báo cáo cải thiện performance-per-watt 3,10%. Kiểm tra phần VI-A, Bảng I–II và Hình 8–9. Bài liên quan về baseline, profile và chi phí miss, không phải dữ liệu sensor. Phân biệt cấu hình oracle, profile và policy triển khai được khi trích dẫn.

### Phân tích độc lập cho Q10

**Lý do chọn.** Một nghiên cứu thực nghiệm cần biết đâu là baseline thực tế và đâu là mốc tham khảo lý tưởng. Trong Q10, AI có thể đưa ra phương án dựa trên kiến thức tổng quát, nhưng không được nhìn trước toàn bộ kết quả official để chọn giải pháp thắng. Nếu simulator được bổ sung một policy biết trước tương lai nhằm tạo giới hạn tham khảo, phải ghi rõ nó không phải thiết kế có thể triển khai online. Nguồn này hữu ích để nhóm xây dựng cách phân loại đó. Một đường “optimal” trên biểu đồ chỉ có ý nghĩa khi giả định và mục tiêu tối ưu của nó được công bố đầy đủ.

**Baseline phải trả lời đúng câu hỏi.** Câu hỏi chính của nhóm yêu cầu so DAI với Direct Mapping, nên D0 phải luôn có trong bảng kết quả. D1 và D2 giúp biết lợi ích đến từ associativity ở mức nào; chúng không được thay thế D0 chỉ vì là đối chứng mạnh hơn hoặc thuận lợi hơn cho candidate. Nếu thêm policy tham khảo, cần ghi rõ nó giải quyết placement, replacement hay cả hai. Có thể dùng một cột “biến thay đổi” để đọc bảng thiết kế. Cách trình bày này giữ cho người xem hiểu mỗi phép so đang kiểm tra điều gì, thay vì thấy nhiều tên thuật toán nhưng không thấy quan hệ với RQ.

**Phải tách dữ liệu phát triển và đánh giá.** Nhóm có thể tạo trace nhỏ để debug, trace phát triển để kiểm tra candidate có hợp lý hay không và official traces để chạy kết quả cuối. Sau design freeze, không dùng kết quả official để thay hash, window hoặc policy mà vẫn giữ nhãn DAI-v1. Nếu buộc sửa vì bug, cần ghi lý do, phiên bản code và đánh dấu các run chịu ảnh hưởng. Nếu thay vì sửa bug mà thực sự chọn lại thiết kế, phải coi đó là phiên bản nghiên cứu mới và công bố quy trình. Quy tắc này đặc biệt quan trọng khi AI có thể đề xuất nhiều biến thể rất nhanh.

**Tính khả thi không chỉ là chạy được bằng Python.** Một thuật toán dựa trên việc quét phần còn lại của trace có thể dễ viết và đạt hit rate tốt, nhưng nó dùng thông tin chưa có tại thời điểm truy cập. Một cấu hình dùng profile cũng cần giải thích profile lấy ở đâu, có trùng input đo hay không và cần bao nhiêu dung lượng. Trong Q10, nhóm nên ưu tiên candidate dùng địa chỉ hiện tại và trạng thái đã có. Nếu dựa vào lịch sử, phải định nghĩa cửa sổ và quy tắc reset. Những thông tin này quyết định phép so có ý nghĩa thực nghiệm hay chỉ là một minh họa giới hạn lý tưởng.

**Không chuyển thẳng kết quả giữa loại cache.** Cache dữ liệu của nhóm chứa các block kích thước cố định theo line size đã khai báo; việc đọc mẫu cân không tương đương nạp và sử dụng micro-op. Bởi vậy, số liệu của nguồn chỉ nên xuất hiện trong đoạn tổng quan về phương pháp, có tên loại cache ngay trong câu. Khi thiết kế simulator, không cần thêm cơ chế frontend chỉ để giống bài tham khảo. Tốt hơn là giữ mô hình đơn giản rồi viết rõ những yếu tố chưa mô phỏng. Một phạm vi rõ ràng vẫn cho phép tạo nghiên cứu hợp lệ và tái lập được với ba thành viên.

**Phân tích mức cải thiện cần cùng mẫu số.** Trong báo cáo Q10, nếu miss rate giảm từ 20% xuống 15%, chênh lệch là 5 điểm phần trăm và mức giảm tương đối là 25%. Hai cách diễn đạt trả lời những câu hỏi khác nhau. Nhóm nên cung cấp cả giá trị gốc để tránh hiểu nhầm, không chỉ một phần trăm lớn trên biểu đồ. Nếu gộp kết quả của nhiều trace, phải ghi cách lấy trung bình và tránh để trace dài áp đảo mọi trường hợp mà không có chủ ý. Một bảng theo workload cùng số access sẽ giúp người đọc kiểm tra phép tổng hợp nhanh hơn.

**Vận dụng vào việc đọc tài liệu.** Hoàng Nam nên dùng bài để kiểm tra cách nhóm phân loại công cụ, dữ liệu và baseline trong literature matrix. Cột “kết quả nổi bật” cần đi cùng “điều kiện so sánh” và “giới hạn áp dụng”. Tô Dân có thể dùng ma trận này để kiểm tra mỗi claim trong bản thảo báo cáo có dẫn đúng nguồn. Quốc Thịnh giữ manifest và seed để cùng một trace đi qua mọi thiết kế. Đóng góp của nguồn vào Q10 vì thế nằm ở chất lượng phương pháp và cách diễn giải, không nằm ở việc bổ sung một thuật toán frontend phức tạp vào simulator học phần.

### Kết luận riêng

**From Optimal to Practical: Efficient Micro-op Cache Replacement Policies for Data Center Applications** được chọn làm nguồn phương pháp về oracle, profile và baseline. Bài hỗ trợ nhóm phân biệt giới hạn tham khảo với thiết kế có thể vận hành khi chưa biết tương lai. Q10 cần giữ D0 và các biến kiểm soát làm trung tâm; các con số micro-op cache chỉ được dẫn như kết quả của công trình gốc với đầy đủ bối cảnh, không phải dự đoán cho dữ liệu cân.

## LIT-006 — EMISSARY: Enhanced Miss Awareness Replacement Policy for L2 Instruction Caching

### Hồ sơ và nội dung nghiên cứu

- **Người tìm kiếm/phụ trách:** Trần Châu Hoàng Nam — QE210145.
- **Tác giả:** Nayana Prasad Nagendra, Bhargav Reddy Godala, Ishita Chaturvedi, Atmn Patel, Svilen Kanev, Tipp Moseley, Jared Stark, Gilles A. Pokam, Simone Campanoni, David I. August.
- **Cơ quan:** Arm, Princeton, Northwestern, Google, Intel; xem affiliation cụ thể trong toàn văn.
- **Công bố:** ISCA 2023, 17/06/2023; bài 62, 13 trang, đã phản biện.
- **Nguồn:** [DOI](https://doi.org/10.1145/3579371.3589097), [toàn văn Princeton](https://liberty.princeton.edu/Publications/isca23_emissary.pdf), [Google Research](https://research.google/pubs/emissary-enhanced-miss-awareness-replacement-policy-for-l2-instruction-caching/).

EMISSARY ưu tiên giữ line lệnh có miss gây chi phí frontend cao. Mô phỏng gem5 full-system với workload server; kết quả geomean speedup 3,24%, tốt nhất 23,7%, so baseline của bài. Kiểm tra phần 5–6, đặc biệt mô hình máy và thí nghiệm. Nguồn hỗ trợ chọn metric chi phí; không chứng minh hiệu quả mapping cho dữ liệu cân. Khi ghi số trang, ưu tiên DOI/article number vì các bản ghi có cách đánh trang khác nhau.

### Phân tích độc lập cho Q10

**Lý do chọn.** Hit rate là chỉ số dễ hiểu, nhưng câu hỏi nghiên cứu còn nhắc đến chi phí truy cập bộ nhớ ước tính. Q10 vì vậy cần định nghĩa rõ cầu nối từ số miss tới một ước lượng thời gian. Nếu simulator không có pipeline, mọi kết luận về CPU thực phải được giới hạn. Nguồn này phù hợp để mở rộng tư duy về metric và giúp người đọc hiểu tại sao bảng kết quả cần nhiều hơn một cột hit rate. Tuy nhiên, lý do lựa chọn là bài học phương pháp; nhóm không cần tái hiện cơ chế xử lý lệnh để hoàn thành đề tài mapping của mình.

**Mô hình AMAT đơn giản nên được công bố.** Một lựa chọn cho Q10 là dùng hit latency và miss penalty giả định, với định nghĩa nhất quán về penalty có bao gồm thời gian tra cache hay chưa. Công thức và đơn vị cần đặt cạnh kết quả, ví dụ cycle/access. Nhóm nên tính trên cùng giả định cho các đối chứng nếu chỉ so hành vi miss; nếu cho candidate latency khác vì phức tạp hơn, phải giải thích phạm vi giá trị đó. Bảng sensitivity với vài mức penalty sẽ cho thấy kết luận có phụ thuộc vào một giả định duy nhất hay không. Các giá trị ấy là tham số mô hình, không phải phép đo thiết bị.

**Dirty writeback cần được tách.** Trong workload ghi liên tục, miss không phải sự kiện duy nhất tạo traffic. Nếu một line đã sửa bị loại, mô hình write-back có thể phát sinh chuyển dữ liệu xuống memory. Nhóm nên đếm read misses, write misses và writebacks riêng, rồi xác định cách chúng được quy đổi thành byte transfer hoặc chi phí ước tính. Không cộng tất cả counter vào một tổng khi chưa kiểm tra một sự kiện đã được tính ở chỗ khác hay chưa. Một vài trace kiểm tra nhỏ sẽ giúp xác nhận công thức, nhất là khi truy cập vượt ranh giới line hoặc khi cần flush cuối lượt chạy.

**Không suy diễn từ miss tới deadline xử lý.** Dòng dữ liệu cân có thể liên quan đến tốc độ lấy mẫu, nhưng một trace chỉ ghi thứ tự địa chỉ không đủ cho biết thời gian giữa hai mẫu. Nếu muốn đánh giá việc kịp xử lý trước mẫu kế tiếp, nhóm cần thêm timestamp, chi phí tính toán và mô hình thực thi. Trong phạm vi hiện tại, nên nói “giảm số lần truy cập memory trong mô hình” hoặc “giảm AMAT ước tính dưới giả định đã nêu”. Cách dùng từ chính xác giúp báo cáo vẫn có giá trị kỹ thuật và không khiến người đọc tưởng nhóm đã đo một hệ thống thời gian thực hoàn chỉnh.

**Ví dụ phân tích nên do nhóm tự tạo.** Nhóm có thể dựng hai cấu hình giả định có miss rate tương tự nhưng số writeback khác nhau, rồi kiểm tra chúng trong simulator. Nếu chi phí tăng do dữ liệu dirty, đây là một cơ chế giải thích trực tiếp từ code và trace. Không dùng ví dụ đó như kết quả quan sát của bài tham khảo. Trong bảng Results, mọi số nên có run ID, trace ID và config ID để phân biệt số được đo với giá trị nhập vào mô hình. Hệ thống ID này cũng giúp người viết phần Discussion tìm đúng bằng chứng khi cần giải thích một trường hợp candidate kém hơn D0.

**Cần kiểm tra cả trường hợp lợi ích nhỏ.** Nếu candidate giảm miss rất ít, chỉ số tương đối có thể trông lớn khi baseline nhỏ hoặc khi chọn một đoạn trace ngắn. Nhóm nên trình bày tổng access và số miss tuyệt đối, cùng chênh lệch theo điểm phần trăm. Với trace có warmup, phải ghi những access nào bị loại khỏi giai đoạn đo. Với workload deterministic, chạy lặp cùng trace cho cùng kết quả không tạo thêm các mẫu độc lập; nên thay tham số hoặc seed hợp lệ thay vì coi nhiều lần chạy giống nhau là tăng độ tin cậy thống kê. Đây là lựa chọn thiết kế thí nghiệm của Q10.

**Cách đưa nguồn vào báo cáo.** Hoàng Nam có thể dùng hồ sơ để đề xuất bảng metric gồm miss rate, traffic và AMAT ước tính, sau đó nhờ Quốc Thịnh kiểm tra cách aggregate. Tô Dân rà soát các câu có từ “nhanh”, “tiết kiệm điện” hoặc “tối ưu” để bảo đảm có bằng chứng tương ứng. Trong Literature Review, bài được xếp vào nhóm đánh giá chi phí cache, đồng thời ghi rõ là instruction caching. Nhóm không nên dùng nguồn này làm tài liệu duy nhất cho công thức cache cơ bản; phần nền tảng vẫn cần giáo trình hoặc nguồn phù hợp nếu được bổ sung theo ngoại lệ đã thống nhất.

### Kết luận riêng

**EMISSARY: Enhanced Miss Awareness Replacement Policy for L2 Instruction Caching** được chọn vì giúp Q10 phân biệt số lượng miss với tác động của miss. Bài có giá trị cho thiết kế metric, sensitivity và cách diễn đạt kết quả. Giới hạn áp dụng là khác loại cache và mô hình thực thi; do đó nhóm chỉ chuyển giao phương pháp đánh giá, không dùng speedup hay tiết kiệm năng lượng của nguồn làm kết quả cho trạm cân.

## LIT-007 — CHROME: Concurrency-Aware Holistic Cache Management Framework with Online Reinforcement Learning

### Hồ sơ và nội dung nghiên cứu

- **Người tìm kiếm/phụ trách:** Dương Quốc Thịnh — QE210121.
- **Tác giả:** Xiaoyang Lu, Hamed Najafi, Jason Liu, Xian-He Sun — Illinois Institute of Technology; Florida International University.
- **Công bố:** HPCA 2024, 02/03/2024, trang 1154–1167; bài hội nghị đã phản biện.
- **Nguồn:** [DOI](https://doi.org/10.1109/HPCA57654.2024.00090), [toàn văn tác giả](https://xiaoyang-lu.github.io/files/HPCA2024/CHROME_paper.pdf), [hồ sơ IIT](https://grc.iit.edu/publications/lu-2024-chrome-1321/), [mã nguồn](https://github.com/Xiaoyang-Lu/CHROME).

CHROME phối hợp replacement, bypass và prefetch với RL online. ChampSim mô phỏng 4/8/16 lõi, LLC 3 MiB/lõi, line 64 B; workload SPEC2006/2017 và GAP. Hình 6 báo cáo +9,2% so LRU cho SPEC homogeneous bốn lõi; phần mở đầu/Hình 1 nêu +13,7% trong ngữ cảnh 16 lõi. Bảng III ghi overhead 92,7 KB. Kiểm tra phần IV–VII, Bảng III và V–VI. Những kết quả này không phải phép đo AI hội thoại đề xuất mapping.

### Phân tích độc lập cho Q10

**Lý do chọn.** Đây là nguồn giúp nhóm đặt phần “AI” vào đúng bối cảnh kỹ thuật. Trong Q10, một công cụ hội thoại có thể đề xuất cách tổ chức cache trước khi chạy benchmark; quá trình truy cập sau đó vẫn có thể hoàn toàn deterministic. Nếu nhóm tự xây bộ học ra quyết định trong mỗi lượt chạy, câu hỏi và chi phí nghiên cứu sẽ khác. Literature Review cần tách hai cách dùng AI ấy để tránh tạo ấn tượng rằng chỉ cần hỏi ChatGPT là đã tái hiện một cơ chế học trong bộ xử lý. Sự phân biệt này cũng giúp giảng viên hiểu chính xác đóng góp mà nhóm đang kiểm nghiệm.

**Ràng buộc phải có trong prompt.** Trước khi hỏi P001–P003, nhóm nên cung cấp data capacity, line size, các workload đã định nghĩa và giới hạn metadata dự kiến. Prompt cần yêu cầu AI giải thích input nào có sẵn tại thời điểm truy cập, những state nào phải lưu và cách reset. Nếu AI đề xuất nhiều cơ chế đồng thời, nhóm yêu cầu tách thành candidate nhỏ có thể triển khai và test. Một bản mô tả có thuật ngữ mạnh nhưng thiếu pseudocode hoặc quy tắc victim chưa đủ để freeze. Trạng thái cuối của thiết kế cần rõ tới mức hai thành viên có thể viết cùng hành vi mà không hỏi thêm AI.

**Chi phí tương đối có thể thay đổi hoàn toàn theo quy mô.** Q10 chỉ dự kiến cache 4 KiB, nên bảng phụ vài kilobyte đã là phần đáng kể của ngân sách dữ liệu. Khi đọc một công trình dành cho LLC lớn, nhóm không nên dùng từ “nhẹ” mà không nêu mẫu số. Có thể báo cáo tỷ lệ metadata/data capacity của candidate và số thao tác logic mỗi access. Nếu không có tổng hợp mạch, chỉ gọi đó là chi phí lưu trữ và thao tác trong mô hình. Không suy ra chip nhỏ hơn, ít điện hơn hoặc đáp ứng timing chỉ vì thuật toán chạy nhanh trong một chương trình mô phỏng trên máy tính cá nhân.

**Nếu có học online, phải định nghĩa việc học.** Một thiết kế thích nghi cần chỉ rõ state, action, reward, tốc độ cập nhật và cơ chế exploration. Seed phải được lưu nếu có quyết định ngẫu nhiên. Warmup cũng trở thành phần quan trọng: candidate có thể học trong giai đoạn đó, còn thời gian đo cần được xác định trước. Một trace ngắn có thể chưa đủ để policy ổn định; một trace phát triển dùng để chọn hyperparameter không nên đồng thời là toàn bộ tập đánh giá. Nếu nhóm chưa đủ nguồn lực kiểm chứng các yếu tố này, nên giữ chúng trong phần Future Work và hoàn thành mapping tĩnh trước.

**Tách tác dụng phối hợp với tác dụng riêng.** Q10 có thể học cách đặt một bảng ablation gọn, nhưng không bắt buộc triển khai mọi kỹ thuật trong nguồn. Ví dụ, nhóm chỉ cần so index chuẩn và index mới dưới cùng replacement, rồi một đối chứng thêm policy nếu được phép. Nếu thêm prefetch, cần ghi rõ nó phát sinh những access nào và những access đó có được đưa vào mẫu số hit rate hay không. Nếu thêm bypass, phải đếm bypass request và memory traffic. Không có các counter ấy thì một candidate có thể trông tốt chỉ vì những sự kiện bất lợi bị bỏ khỏi thống kê.

**Workload thay đổi pha là một phép thử hữu ích.** Trong mô hình cân, có thể tạo giai đoạn thu mẫu bình thường, giai đoạn đọc lại nhiều mẫu để lọc và giai đoạn ghi log mạnh. Đây là đề xuất input cho Q10, không phải hành vi đã đo của một trạm cân thật. Mục đích là xem một candidate có phụ thuộc quá nhiều vào pattern ban đầu không. Cần giữ tổng số mẫu, số byte và quy tắc chuyển pha có thể tái lập. Nếu candidate dùng lịch sử, nên báo cáo kết quả theo từng pha bên cạnh kết quả toàn lượt chạy, để tránh che khuất giai đoạn thích nghi kém.

**Vai trò trong phân công ba thành viên.** Quốc Thịnh phụ trách lập bảng so sánh “AI đề xuất thiết kế” và “ML ra quyết định lúc chạy”, đồng thời lưu transcript không sửa tay. Hoàng Nam kiểm tra rằng implementation chỉ sử dụng thông tin được phép; Tô Dân rà soát claim về AI trong report. Nếu dùng code do AI hỗ trợ, nhóm vẫn phải có test độc lập và ghi nguồn trợ giúp theo nhật ký. Tên thuật toán không thay thế validation. Một kết quả tốt nhưng không thể chỉ ra prompt, config và run tương ứng sẽ không đủ để chứng minh AI thực sự đóng vai trò gì trong nghiên cứu.

### Kết luận riêng

**CHROME: Concurrency-Aware Holistic Cache Management Framework with Online Reinforcement Learning** được chọn làm nguồn chính về ML trong quản lý cache và chi phí đi kèm. Nguồn giúp Q10 định nghĩa đúng vai trò AI, kiểm soát thông tin đầu vào và cân nhắc metadata. Nhóm nên chuyển giao cách đặt ràng buộc và cách kiểm chứng, không coi kết quả RL của tác giả là bằng chứng rằng thiết kế do ChatGPT đề xuất sẽ đạt cùng mức cải thiện.

## LIT-008 — A Prefetch-Adaptive Intelligent Cache Replacement Policy Based on Machine Learning

### Hồ sơ và nội dung nghiên cứu

- **Người tìm kiếm/phụ trách:** Dương Quốc Thịnh — QE210121.
- **Tác giả:** Hui-Jing Yang, Juan Fang, Min Cai, Zhi Cai — Beijing University of Technology.
- **Công bố:** Journal of Computer Science and Technology, 38(2), 391–404, 30/03/2023; nhận 2021, chấp nhận 2022, **xuất bản 2023**, đạt bộ lọc năm. Bài tạp chí đã phản biện.
- **Nguồn:** [DOI](https://doi.org/10.1007/s11390-022-1573-3), [trang tạp chí](https://jcst.ict.ac.cn/EN/Y2023/V38/I2/391), [toàn văn](https://jcst.ict.ac.cn/en/article/pdf/preview/10.1007/s11390-022-1573-3.pdf).

PAIC dùng predictor ISVM riêng cho demand/prefetch. ChampSim/CRC2 đánh giá 27 chương trình SPEC2006/2017. Phần 4.2.1: +37,22% so LRU không prefetch nhưng +3,86% so LRU có SPP. Phần 4.2.3 dùng KPC-P báo +36,61% với baseline tương ứng; không gộp khác cấu hình. Phần 4.1 ghi warmup 200 triệu instruction; Bảng 1 báo hardware budget tối ưu 29,31 KB. Vị trí kiểm tra: phần 3–4, Hình 7–8 và Bảng 1. Đây là replacement, không phải riêng mapping.

### Phân tích độc lập cho Q10

**Lý do chọn.** Nguồn này đặc biệt hữu ích để nhóm học cách đọc một tỷ lệ cải thiện đi cùng baseline. Khi một thiết kế kết hợp nhiều kỹ thuật, phần trăm trong abstract có thể dùng một đối chứng khác với phép so mà người đọc quan tâm. Trong báo cáo Q10, cần ghi rõ DAI thay đổi mapping dưới điều kiện nào và D0 có cùng các cơ chế hỗ trợ hay không. Nếu thiếu thông tin đó, một con số đúng về mặt tính toán vẫn có thể dẫn tới nhận xét sai về nguyên nhân. Nhóm nên kiểm tra điều kiện ngay trong caption, không chỉ sao lại tỷ lệ lớn nhất ở đầu bài.

**Prefetch là biến cần quyết định trước.** Phiên bản Q10 tối thiểu có thể không mô phỏng prefetch; nếu chọn như vậy, mọi cấu hình phải dùng cùng quyết định. Việc tắt một cơ chế không làm nghiên cứu mất giá trị nếu giới hạn được nói rõ. Nếu nhóm mở rộng để có prefetch, generator hoặc cache controller phải đánh dấu access nào do chương trình yêu cầu và access nào được sinh dự đoán. Hai loại đó cần các counter riêng để biết block dự đoán có được dùng lại hay chỉ chiếm chỗ. Không nên thêm prefetch vào riêng DAI trong một phép so được đặt tên là hiệu quả mapping.

**Thí nghiệm nhỏ có thể chỉ ra nhiễu từ policy.** Nhóm có thể dùng cùng trace tuần tự và chạy một cấu hình đọc trước line kế tiếp, một cấu hình không đọc trước. Sau đó, giữ hai chế độ ấy khi đổi mapping. Một bảng hai chiều sẽ giúp thấy tác động của từng biến. Tuy nhiên, chỉ nên làm nếu được freeze thành thí nghiệm riêng trước official runs; không dùng nó như vòng thử vô hạn để chọn kết quả đẹp. Nếu thời gian hạn chế, tập trung vào mapping dưới một môi trường cố định sẽ phù hợp hơn. Nguồn tham khảo giúp xác định mối nguy nhiễu, không bắt buộc mở rộng phạm vi bài RBL.

**Yêu cầu về trace phải thực tế với dữ liệu đang có.** Một predictor dùng program counter cần trace chứa program counter hoặc cơ chế lấy thông tin tương đương. Trace R/W, address, size trong kế hoạch hiện không có trường đó. Nhóm không được tự gán PC dựa trên kết quả cần dự đoán, vì như vậy có thể đưa thông tin tương lai vào input. Nếu bổ sung PC giả theo loại thao tác để làm mô hình, phải ghi đó là nhãn do generator định nghĩa và kiểm tra mọi thiết kế được cấp thông tin công bằng. Không gọi kết quả mô hình ấy là đo trực tiếp trên chương trình trạm cân đã biên dịch.

**Kiểm tra chi phí và khởi tạo.** Khi một candidate dùng bảng dự đoán, cần xác định trạng thái ban đầu, quy tắc đào tạo và cách xử lý address chưa từng thấy. Hai lượt chạy cùng trace phải bắt đầu từ cùng điều kiện, trừ khi nghiên cứu riêng tác động của trạng thái lưu lại. Nếu bảng được giữ từ lượt chạy trước mà baseline bị reset, phép so không công bằng. Ngoài memory budget, nhóm nên ghi số lần cập nhật và số lookup như thông tin độ phức tạp. Các counter này chưa phải timing phần cứng, nhưng giúp người đọc hiểu candidate cần thêm công việc gì để đạt mức miss được quan sát.

**Cách báo cáo kết quả không nhập nhằng.** Mỗi tỷ lệ cải thiện trong Q10 nên đi cùng tên baseline, workload, seed hoặc tập seed, cấu hình và metric. Khi đổi baseline, tính lại tỷ lệ từ giá trị gốc thay vì lấy hai phần trăm trừ nhau. Ví dụ về mặt phương pháp, mức tăng tốc so A và mức tăng tốc so B không trực tiếp cho biết tốc độ của A so B nếu chưa khôi phục mẫu số. Tốt nhất là cung cấp cả bảng raw hoặc processed đủ để tính lại. Nhờ vậy, một thay đổi caption cũng không làm mất khả năng truy vết của kết luận.

**Cách dùng trong tổng quan và viết báo cáo.** Quốc Thịnh nên đặt bài trong nhóm ML có nhận biết loại truy cập, ghi rõ khác với AI hội thoại. Hoàng Nam dùng nó để kiểm tra rằng simulator không âm thầm thay nhiều biến khi tạo config. Tô Dân rà lại các phần trăm và câu kết luận có dẫn nguồn. Bài xuất bản năm 2023 vẫn đạt tiêu chí dù DOI có chuỗi “022” và quá trình duyệt trước đó; nhóm nên dùng năm xuất bản chính thức, không suy năm từ mã DOI. Đây là một ví dụ cụ thể cho việc sàng lọc bằng metadata thay vì chỉ nhìn tên tệp hoặc kết quả tìm kiếm.

### Kết luận riêng

**A Prefetch-Adaptive Intelligent Cache Replacement Policy Based on Machine Learning** được chọn vì làm rõ tương tác giữa ML, prefetch và replacement, đồng thời cho một trường hợp cần đọc baseline cẩn thận. Q10 nên học cách kiểm soát biến và kiểm tra input của predictor. Không dùng mức cải thiện so LRU không prefetch để tuyên bố lợi ích riêng của một thay đổi mapping, và không nhầm năm chấp nhận hoặc mã DOI với năm công bố.

## LIT-009 — Sketching the Path to Efficiency: Lightweight Learned Cache Replacement

### Hồ sơ và nội dung nghiên cứu

- **Người tìm kiếm/phụ trách:** Dương Quốc Thịnh — QE210121.
- **Tác giả:** Rana Shahout — Harvard University; Roy Friedman — Technion.
- **Công bố:** OPODIS 2023, LIPIcs 286, bài 34, trang 34:1–34:21; phát hành **18/01/2024**. Bài hội nghị đã phản biện, giấy phép CC BY 4.0.
- **Nguồn:** [DOI/trang Dagstuhl](https://doi.org/10.4230/LIPIcs.OPODIS.2023.34), [toàn văn](https://drops.dagstuhl.de/storage/00lipics/lipics-vol286-opodis2023/LIPIcs.OPODIS.2023.34/LIPIcs.OPODIS.2023.34.pdf), [mã nguồn tác giả](https://github.com/r4n4sh/sketch_learning).

ALPS dùng sketches và ML chọn policy cho frame tiếp theo thay vì quyết định ML từng access. Triển khai C++ kết hợp Caffeine simulator; Bảng 3 đánh giá cache 1K/10K/100K item, frame bằng 10 lần cache size. Cấu hình All/1K báo hit-ratio increase 20% so LRU. Kiểm tra phần 3–4 và Bảng 3. Đây là cache phần mềm theo item, không phải CPU line; không chuyển “1K item” thành “1 KiB” hoặc dùng kết quả như benchmark mapping phần cứng.

### Phân tích độc lập cho Q10

**Lý do chọn và ranh giới phù hợp.** Bộ tiêu chí cho phép bài đóng góp trực tiếp về ML hỗ trợ tối ưu cache hoặc data streams, không giới hạn tuyệt đối mọi nguồn vào cùng loại cache. Bài này được chọn ở vai trò phương pháp vì Q10 cũng xử lý chuỗi truy cập và phải cân nhắc chi phí theo dõi lịch sử. Tuy nhiên, trong bảng tổng quan cần luôn gắn nhãn software/item cache. Việc một nguồn liên quan ở mức ý tưởng không biến nó thành bằng chứng rằng một hàm index cụ thể sẽ tốt hơn Direct Mapping. Đây là giới hạn áp dụng cần giữ xuyên suốt khi trích dẫn.

**Tổng hợp theo cửa sổ có ích cho phân tích workload.** Nhóm có thể chia trace thành các đoạn số access cố định và thống kê tỷ lệ đọc/ghi, số block phân biệt, mức lặp địa chỉ hoặc phân bố truy cập theo set. Những thống kê này có thể phục vụ giải thích kết quả ngay cả khi candidate không có ML online. Chẳng hạn, nếu một giai đoạn có working set nhỏ và reuse nhiều, nhóm có cơ sở để kiểm tra tại sao hit rate tăng. Nếu một giai đoạn chủ yếu đi qua địa chỉ mới, cần xem compulsory miss thay vì vội thay replacement. Những giả thuyết đó phải được kiểm tra bằng trace và counter của nhóm.

**Kích thước cửa sổ là một lựa chọn nghiên cứu.** Một cửa sổ quá dài có thể che mất thay đổi pha; quá ngắn có thể tạo nhiều dao động và làm bảng phân tích khó đọc. Với Q10, nên chọn quy tắc trước official runs, ví dụ theo số mẫu cân hoặc số access, rồi ghi rõ vì sao đơn vị ấy phù hợp. Nếu chạy sensitivity, chọn một số giá trị định trước và báo cáo đầy đủ. Không thay cửa sổ riêng cho từng kết quả chỉ để làm biểu đồ mượt hoặc tăng độ tách biệt giữa D0 và DAI. Cùng một quy tắc aggregate giúp phép so theo thời gian có ý nghĩa hơn.

**Thống kê phân tích khác trạng thái của cache.** Một script offline có thể đọc toàn trace để vẽ biểu đồ; một policy thực thi chỉ được dùng phần lịch sử đã xuất hiện. Hai loại xử lý cần nằm trong hai module khác nhau để tránh rò rỉ thông tin. Nếu AI được cung cấp đặc tính workload trước freeze, nên cung cấp đặc tả hoặc thống kê từ tập phát triển đã công bố. Không đưa toàn bộ kết quả official vào prompt rồi vẫn gọi phương án là chọn độc lập. Cách tổ chức này bảo vệ tính hợp lệ của nghiên cứu ngay cả khi nhóm dùng những công cụ phân tích rất mạnh ở phía hậu kỳ.

**Nếu chọn policy theo pha, cần tính chi phí chuyển.** Nhóm có thể đề xuất một hướng mở rộng trong đó cache đổi policy khi pattern thay đổi, nhưng khi triển khai phải định nghĩa trạng thái cũ được giữ hay reset. Việc chạy lại hai policy từ đầu trên cùng đoạn rồi chọn policy thắng sau khi xem kết quả là một oracle hậu nghiệm, không phải bộ chọn online. Nếu chỉ dùng cách đó để tìm trần tham khảo, phải ghi nhãn rõ. Q10 phiên bản cốt lõi có thể tránh phức tạp này bằng candidate mapping cố định, còn phân tích theo pha dùng để giải thích giới hạn và đề xuất nghiên cứu tiếp theo.

**Đơn vị và mẫu số cần được bảo vệ.** Một item phần mềm có thể có kích thước hoặc chi phí phục vụ khác line dữ liệu CPU. Trong mô hình Q10, mọi access phải được phân rã theo line size trước khi tính hit/miss nếu nó vượt ranh giới. Khi đọc bài này, nhóm học cách gắn kết quả với cấu hình đánh giá, nhưng không lấy số item để suy dung lượng byte. Tương tự, tăng hit ratio theo phần trăm không nhất thiết đồng nghĩa giảm miss cùng phần trăm. Bảng kết quả của nhóm nên luôn giữ giá trị gốc, đơn vị và công thức chuyển đổi để không tạo sai lệch khi tổng hợp.

**Cách sử dụng phù hợp với nguồn lực hiện tại.** Quốc Thịnh có thể xây thống kê theo cửa sổ trong phần analysis mà không thêm ML vào simulator. Hoàng Nam cung cấp log hoặc counter đủ cho script; Tô Dân dùng biểu đồ để viết phần Discussion theo giả thuyết. Khi muốn đề xuất candidate thích nghi, cả nhóm phải cân nhắc liệu có đủ thời gian test trạng thái và chi phí không. Một kết luận nêu rõ “thiết kế tĩnh tốt ở pha này nhưng kém ở pha khác” đã có giá trị nghiên cứu nếu evidence đầy đủ. Không cần triển khai bộ học mới chỉ để tăng độ phức tạp của báo cáo.

### Kết luận riêng

**Sketching the Path to Efficiency: Lightweight Learned Cache Replacement** được chọn làm nguồn về ML tiết kiệm chi phí trên dòng truy cập và phân tích theo frame. Giá trị chuyển giao cho Q10 nằm ở cách tổng hợp đặc tính workload, tách học với đánh giá và xem xét overhead. Bài không được dùng làm chứng cứ trực tiếp cho cache CPU 4 KiB; nhóm giữ nó trong tập chín bài với vai trò phương pháp đã công bố rõ.

## Kết luận đối chiếu chín bài

### Những điểm nhóm có thể sử dụng

| Vấn đề của Q10 | Nguồn liên quan | Quyết định phương pháp đề xuất |
|---|---|---|
| Xung đột do placement | LIT-001, 002, 003 | Có D0/D1/D2; định nghĩa candidate bằng index/tag/victim và test truy vết. |
| Ngân sách so sánh | LIT-002, 007, 008 | Giữ data capacity; báo cáo riêng metadata và giả định latency. |
| Workload có bối cảnh | LIT-004, 009 | Sinh trace theo pipeline cân, lưu tham số/seed, phân tích theo vùng và pha. |
| Đánh giá đúng đóng góp | LIT-004, 005, 008 | Tách tác động mapping khỏi prefetch/replacement; không đổi baseline âm thầm. |
| Ý nghĩa của metric | LIT-005, 006 | Báo cáo số miss gốc, tỷ lệ, traffic và AMAT với giả định rõ. |
| Vai trò AI | LIT-007, 008, 009 | Phân biệt AI hỗ trợ thiết kế với ML online; lưu transcript và freeze trước benchmark. |

Đây là phần tổng hợp quyết định cho Q10, không phải tuyên bố mọi công trình trong bảng đã thực hiện cùng một thí nghiệm. Từng nguồn giải quyết một bối cảnh khác nhau; không lấy trung bình các phần trăm cải thiện giữa chúng và không xếp hạng thuật toán bằng cách so các con số khác metric hoặc khác baseline.

### Khoảng trống trong phạm vi tập tài liệu đã chọn

Trong **chín bài được chọn**, chưa có một phép so trùng toàn bộ điều kiện Q10: công cụ AI hội thoại đề xuất mapping trước benchmark, cache dữ liệu 4 KiB/line 32 B, cùng trace mô hình trạm cân, so với D0 dưới các biến kiểm soát đã nêu. Đây là nhận xét về tập tài liệu này, **không phải khẳng định chưa từng có công trình tương tự trên toàn thế giới** và không đủ để tuyên bố phát minh kiến trúc mới.

Đóng góp khả thi của nhóm là một đánh giá thực nghiệm có kiểm soát và tái lập được trong bối cảnh workload đã mô tả. Sự mới của nghiên cứu học phần có thể nằm ở cách kết hợp câu hỏi, bộ trace và quy trình kiểm chứng; không cần giả định rằng AI phải tạo ra thuật toán chưa từng xuất hiện.

### Hướng triển khai rút ra cho ba thành viên

1. **Tô Dân** chốt RQ, bảng kiến trúc D0/D1/D2/DAI, điều kiện capacity và ma trận claim–evidence; phụ trách kiểm tra cách trích nguồn về mapping.
2. **Hoàng Nam** xây simulator, test address decomposition và hit/miss/writeback, kiểm chứng trace nhỏ; phụ trách bảng metric và công thức AMAT.
3. **Quốc Thịnh** xây W1–W5, manifest/seed, chạy cùng trace trên mọi thiết kế, aggregate/plot và lưu transcript AI; phụ trách kiểm tra ML được mô tả đúng vai trò.

Mỗi artefact quan trọng có reviewer khác owner. Đây là phương án triển khai đề xuất sau khi nhóm còn ba người; chưa phải xác nhận các công việc đã hoàn thành. Trước official experiment phải có protocol, AI design freeze, validation và workload freeze. Nếu công việc đã được làm trước đó, ghi ngày thực tế và bằng chứng; không tạo lịch sử hoặc mốc freeze hồi tố.

### Kết luận chung

Bộ chín bài đủ để xây tổng quan theo ba trục: tổ chức placement, đánh giá cache theo workload và ML hỗ trợ quản lý cache. Nguồn gần nhất với phần mapping là LIT-001–003; LIT-004 bổ sung cách nối kiến trúc với bối cảnh ứng dụng; LIT-005–006 giúp kiểm soát baseline và metric; LIT-007–009 làm rõ vai trò học máy, dữ liệu lịch sử và overhead.

**Khuyến nghị cho Q10 là ưu tiên một candidate đơn giản, mô tả đầy đủ và kiểm chứng được**, rồi chạy D0/D1/D2/DAI trên cùng W1–W5 dưới cùng data capacity và line size. Đánh giá bằng số liệu của simulator đã validate; nếu tính chi phí truy cập, phải nêu giả định và kiểm tra sensitivity. Không kết luận hiệu năng phần cứng hoặc năng lượng từ hit rate đơn thuần. Nếu DAI chỉ tốt ở workload xung đột hoặc không tốt hơn D0, đó vẫn là kết quả hợp lệ khi quy trình minh bạch và evidence đầy đủ.

Các nguồn hiện tại là cơ sở thiết kế nghiên cứu, chưa phải phần Results của nhóm. Trước khi nộp, từng người phụ trách cần đối chiếu toàn văn, xác nhận thông tin mình sử dụng, kiểm tra trạng thái công bố mới và bổ sung trang/hình cụ thể vào các câu trích trong bản báo cáo cuối.

## Danh mục trích dẫn để dùng trong báo cáo

Số thứ tự tương ứng LIT-001–LIT-009. Khi đưa vào báo cáo, dùng thứ tự xuất hiện thực tế theo kiểu IEEE và đồng bộ lại số tham chiếu.

1. W. Song, Z. Xue, J. Han, Z. Li, and P. Liu, “Randomizing Set-Associative Caches Against Conflict-Based Cache Side-Channel Attacks,” *IEEE Transactions on Computers*, vol. 73, no. 4, pp. 1019–1033, 2024. [DOI: 10.1109/TC.2024.3349659](https://doi.org/10.1109/TC.2024.3349659).
2. A. Bhatla, Navneet, and B. Panda, “The Maya Cache: A Storage-efficient and Secure Fully-associative Last-level Cache,” in *ISCA 2024*, pp. 32–44, 2024. [DOI: 10.1109/ISCA59077.2024.00013](https://doi.org/10.1109/ISCA59077.2024.00013).
3. L. Giner, S. Steinegger, A. Purnal, M. Eichlseder, T. Unterluggauer, S. Mangard, and D. Gruss, “Scatter and Split Securely: Defeating Cache Contention and Occupancy Attacks,” in *IEEE Symposium on Security and Privacy*, pp. 2273–2287, 2023. [DOI: 10.1109/SP46215.2023.10179440](https://doi.org/10.1109/SP46215.2023.10179440).
4. M. Bakhshalipour and P. B. Gibbons, “Tartan: Microarchitecting a Robotic Processor,” in *ISCA 2024*, pp. 548–565, 2024. [DOI: 10.1109/ISCA59077.2024.00047](https://doi.org/10.1109/ISCA59077.2024.00047).
5. K. Zhu, Y. Zhao, Y. Gao, P. Braun, T. A. Khan, H. Litz, B. Kasikci, and S. Deng, “From Optimal to Practical: Efficient Micro-op Cache Replacement Policies for Data Center Applications,” in *HPCA 2025*, pp. 716–731, 2025. [DOI: 10.1109/HPCA61900.2025.00060](https://doi.org/10.1109/HPCA61900.2025.00060).
6. N. P. Nagendra, B. R. Godala, I. Chaturvedi, A. Patel, S. Kanev, T. Moseley, J. Stark, G. A. Pokam, S. Campanoni, and D. I. August, “EMISSARY: Enhanced Miss Awareness Replacement Policy for L2 Instruction Caching,” in *ISCA 2023*, article 62, pp. 1–13, 2023. [DOI: 10.1145/3579371.3589097](https://doi.org/10.1145/3579371.3589097).
7. X. Lu, H. Najafi, J. Liu, and X.-H. Sun, “CHROME: Concurrency-Aware Holistic Cache Management Framework with Online Reinforcement Learning,” in *HPCA 2024*, pp. 1154–1167, 2024. [DOI: 10.1109/HPCA57654.2024.00090](https://doi.org/10.1109/HPCA57654.2024.00090).
8. H.-J. Yang, J. Fang, M. Cai, and Z. Cai, “A Prefetch-Adaptive Intelligent Cache Replacement Policy Based on Machine Learning,” *Journal of Computer Science and Technology*, vol. 38, no. 2, pp. 391–404, 2023. [DOI: 10.1007/s11390-022-1573-3](https://doi.org/10.1007/s11390-022-1573-3).
9. R. Shahout and R. Friedman, “Sketching the Path to Efficiency: Lightweight Learned Cache Replacement,” in *27th International Conference on Principles of Distributed Systems (OPODIS 2023)*, LIPIcs, vol. 286, article 34, pp. 34:1–34:21, 2024. [DOI: 10.4230/LIPIcs.OPODIS.2023.34](https://doi.org/10.4230/LIPIcs.OPODIS.2023.34).

## Ghi chú kiểm tra và lưu trữ

- Mỗi hồ sơ có nguồn DOI và toàn văn; các nhận xét áp dụng cho Q10 được tách khỏi phần thông tin của tác giả.
- Các bản PDF đã tải được và văn bản trích xuất phục vụ đối chiếu nằm trong `_research_sources/`; thư mục này là tài liệu làm việc nội bộ, không tự động đưa toàn bộ PDF vào gói công khai của nhóm.
- LIT-009 đã truy cập toàn văn qua công cụ web; việc tải bản lưu cục bộ bằng Python gặp lỗi xác minh chứng chỉ. Điều này không ảnh hưởng đường toàn văn Dagstuhl đã đọc và liên kết trong hồ sơ.
- `metadata_check.json` lưu kết quả truy vấn Crossref ban đầu, bao gồm cả lỗi 429/404; không xóa các trường hợp không truy vấn được để tạo cảm giác mọi nguồn đều được kiểm tra bằng cùng một cách.
- Độ dài mỗi hồ sơ tính theo các đơn vị văn bản ngăn bằng khoảng trắng; nội dung bao gồm tóm lược, phân tích áp dụng và kết luận riêng. Đây không phải bản dịch toàn văn hay bản sao kéo dài của bài gốc.
