# Kế hoạch xây simulator cache Q10

**Đầu vào đã chốt:** Q10-PROTOCOL-v1.0 và DAI-v1, phương án B — XOR 2-way. Người dùng đã xác nhận kiểm tra và chốt thiết kế.

**Trạng thái triển khai:** Đã xây simulator và bốn config, parser, runner, xuất JSON/JSONL và validation tự động. Lần kiểm tra được ghi trong `validation/LATEST.txt` có 21 unit tests và 20 phép đối chiếu trace/config, đều PASS. Chưa ghi nhận thành viên nhóm xác nhận implementation và chưa chạy official benchmark. Xem [hướng dẫn chạy](C:/Tai_Lieu_Hoc/CEA201/RBL/README.md) và [bảng đối chiếu tính tay](C:/Tai_Lieu_Hoc/CEA201/RBL/validation/manual_checks.md).

Mục tiêu của giai đoạn này là tạo chương trình đọc trace, mô phỏng đúng bốn thiết kế D0/D1/D2/DAI và xuất kết quả có thể kiểm tra lại. Hoàn thành simulator và validation trước khi tạo bộ kết quả benchmark chính thức.

## 1. Sản phẩm cần có

1. Một lõi cache dùng chung, lựa chọn mapping/replacement theo config.
2. Bốn config D0, D1, D2 và DAI-v1.
3. Bộ đọc trace có kiểm tra đầu vào.
4. Runner xử lý khởi động, đo và xuất JSON.
5. Unit tests, trace nhỏ và báo cáo validation.
6. Hướng dẫn chạy, phiên bản môi trường và nhận diện phiên bản nguồn.

Ưu tiên Python standard library và `unittest` để giảm dependency. Simulator chính chỉ cần mô phỏng tag, valid, dirty, replacement state và traffic. Trace hiện không có giá trị cân/payload, nên không cần tính trọng lượng hoặc giả lập nội dung word thực.

## 2. Cấu trúc dự kiến

```text
src/
  simulator/
    __init__.py
    models.py       # Config, CacheLine, Counters
    mapping.py      # Index, tag và khôi phục block
    cache.py        # Lookup, hit/miss, eviction, dirty, LRU
    trace.py        # Đọc và kiểm tra dòng trace
    runner.py       # Khởi động, đo, xuất result
configs/
  D0.json
  D1.json
  D2.json
  DAI-v1.json
tests/
  test_mapping.py
  test_cache.py
  test_runner.py
traces/
  debug/            # Chỉ trace nhỏ phục vụ validation
validation/
  manual_checks.md
  test_report.txt
```

Cấu trúc mã nguồn trên đã được triển khai. Báo cáo thực tế được lưu theo từng thư mục `validation/check_<thời điểm>/`, gồm `test_report.txt`, `summary.json`, JSON kết quả và JSONL events. `validation/LATEST.txt` chỉ tới lần gần nhất; không dùng đường dẫn báo cáo phẳng trong sơ đồ như một xác nhận file đó đã tồn tại.

## 3. Bước A — Cấu hình và trạng thái cache

### Cấu hình

| ID | Sets | Ways | Line | Data capacity | Mapping | Replacement |
|---|---:|---:|---:|---:|---|---|
| D0 | 128 | 1 | 32 B | 4 KiB | Modulo | Vị trí duy nhất |
| D1 | 64 | 2 | 32 B | 4 KiB | Modulo | Exact LRU |
| D2 | 32 | 4 | 32 B | 4 KiB | Modulo | Exact LRU |
| DAI-v1 | 64 | 2 | 32 B | 4 KiB | XOR theo đặc tả | Exact LRU như D1 |

Config phải được kiểm tra khi nạp: `sets × ways × line_size == 4096`, đúng write-back/write-allocate và không prefetch/bypass.

### Trạng thái

Mỗi line cần valid, dirty và tag. D1/DAI dùng một bit `lru_way` cho mỗi set. D2 dùng rank exact LRU cho bốn way, phù hợp giả định metadata 2 bit/way trong đặc tả đã chốt. Rank phải được cập nhật trên cả hit và fill; các line valid trong cùng set có thứ tự recency xác định. Không dùng tree pseudo-LRU thay exact LRU.

Counter tối thiểu: accesses, hits, misses, read_misses, write_misses, evictions, dirty_writebacks và line_fills. Có hàm reset toàn run và hàm reset counter riêng.

**Điều kiện đạt:** tạo đúng số line, trạng thái khởi tạo rõ ràng và config sai bị từ chối.

## 4. Bước B — Viết và kiểm tra mapping trước

```text
b = address >> 5

D0/D1/D2:
    index = b % sets
    tag = b // sets
    recover_block(index, tag) = tag * sets + index

DAI-v1:
    index = (b ^ (b >> 6)) & 63
    tag = b >> 6
    recover_block(index, tag) = (tag << 6) | (index ^ (tag & 63))

writeback_base = recover_block(index, victim_tag) << 5
```

Không tái sử dụng phép ghép địa chỉ chuẩn D1 cho DAI. Ví dụ DAI với block 64 có index=1, tag=1; địa chỉ ghi trả phải là 2048, không phải 2080.

Test round-trip `recover_block(index(b), tag(b)) == b` trên các biên và một tập block xác định, bao gồm bit địa chỉ cao. Kiểm tra địa chỉ 28/32, 0x80000000 và 0xFFFFFFFC. Dùng chứng minh đại số trong R003 để giải thích toàn miền; không gọi lấy mẫu là kiểm tra exhaustive toàn miền.

**Điều kiện đạt:** công thức, tag width và địa chỉ khôi phục đúng trước khi ghép với xử lý hit/miss.

## 5. Bước C — Viết lõi access và replacement

Xử lý theo đúng thứ tự:

1. Kiểm tra op thuộc R/W, size=4, địa chỉ nguyên trong 0..2^32−4 và chia hết cho 4. Input sai không được thay đổi state/counters.
2. Tính block/index/tag; chỉ lookup các way của set hợp lệ.
3. Nếu hit: tăng hit khi đang đo; W đặt dirty; R giữ dirty; cập nhật LRU.
4. Nếu miss: tăng đúng một read/write miss khi đang đo.
5. Ưu tiên invalid way nhỏ nhất. Nếu set đầy, chọn victim exact LRU; D0 chỉ có vị trí duy nhất.
6. Nếu victim valid: tăng eviction khi đang đo. Nếu dirty: phát sinh writeback địa chỉ cũ trước khi ghi đè và tăng dirty_writeback khi đang đo.
7. Fill đúng một line mới; tăng line_fill khi đang đo. Line mới dirty nếu demand là W.
8. Cập nhật recency và kết thúc access.

Writeback và fill là sự kiện memory theo line, không được gọi lại demand access để tạo thêm access hoặc miss. Kiểm tra không có hai way cùng hit một block.

Nên hoàn thiện D0 trước, sau đó D1, D2, cuối cùng DAI dùng lại lõi D1 với mapping riêng. Tránh viết bốn bản hit/miss độc lập dễ lệch chính sách.

**Điều kiện đạt:** các trace nhỏ cho đúng kết quả và counter; D1 và DAI chỉ khác mapping cùng hàm khôi phục đi kèm.

## 6. Bước D — Đọc trace và điều khiển khoảng đo

Định dạng đề xuất, mỗi dòng là một demand access:

```text
R 0x00000000 4
W 0x00000800 4
R 0x00000020 4
```

Parser quy định rõ có chấp nhận dòng trống/comment hay không, hỗ trợ địa chỉ thập phân/hex nếu đã khai báo, và báo số dòng khi lỗi. Không âm thầm bỏ qua dòng sai.

Runner chính:

1. Reset toàn cache/counters/replacement.
2. Xử lý 10.000 access khởi động; state vẫn cập nhật nhưng counters khoảng đo chưa tăng.
3. Chỉ reset counters, giữ contents/dirty/LRU, không flush.
4. Xử lý đúng 100.000 access đo.
5. Xuất kết quả; không flush cuối vào traffic chính.

Runner phải báo lỗi nếu trace không đủ số access yêu cầu. Chế độ debug được phép dùng số khởi động/đo nhỏ hơn để test; kết quả phải mang nhãn debug, không trộn vào official runs. Cùng trace và cùng khoảng đo được dùng cho mọi design.

**Điều kiện đạt:** test đọc cuối warmup rồi đọc lại đầu measurement phải hit; run kế tiếp phải bắt đầu rỗng.

## 7. Bước E — Xuất kết quả và khả năng truy vết

Xuất JSON cho từng run, gồm:

- Run ID, design ID, protocol ID và phiên bản simulator.
- Config snapshot, trace ID/path, checksum trace và seed nếu có.
- Số warmup access, số measured access và các counters gốc.
- Hit rate, miss rate, memory traffic byte.
- SUCCESS/FAIL/INVALID và lý do nếu không hợp lệ.

Các kiểm tra nhất quán:

```text
hits + misses == accesses
read_misses + write_misses == misses
line_fills == misses
dirty_writebacks <= evictions <= misses
memory_traffic_bytes == (line_fills + dirty_writebacks) * 32
```

Các đẳng thức áp dụng trong mô hình không prefetch/bypass/flush vào counters chính. Khi accesses=0, tỷ lệ phải được xử lý rõ thay vì chia cho 0.

Chế độ debug có thể xuất từng access: block, index, tag, H/M, victim và writeback base. Không bắt buộc ghi từng access trong mọi lượt dài vì sẽ tạo log lớn. Lưu config và kết quả gốc thay vì chỉ in màn hình.

**Điều kiện đạt:** người khác có thể lấy config và trace đã ghi để chạy lại đúng một kết quả; không chỉnh tay số trong JSON.

## 8. Bước F — Validation trước khi làm benchmark

Triển khai T01–T06 và X01–X07 trong R003. Các ví dụ trọng tâm cho DAI, bắt đầu cache rỗng:

| Trace | Kết quả đúng |
|---|---|
| R0, R0 | M,H |
| R0, R2080, R0, R4160, R2080 | M,M,H,M,M; hai eviction |
| W2048, R2048, R32, R4192 | M,H,M,M; writeback tại 2048; traffic 128 B |
| R28, R32, R28 | M,M,H |
| R0, R2080, R4160, R0, R2080, R4160 | Sáu miss; đây là phản ví dụ DAI kém D0/D1 |

Với D2, bổ sung trace lấp đủ bốn way cùng set, chạm lại một line rồi nạp line thứ năm để kiểm tra victim đúng exact LRU. Kiểm tra cả read hit, write hit và fill đều cập nhật recency.

So simulator chính với một mô hình tham chiếu nhỏ biểu diễn khác, ví dụ full block ID và danh sách LRU, trên trace debug xác định. Giữ 3–5 bảng tính tay để kiểm tra độc lập; Ripes chỉ dùng với cấu hình tương thích. Script self-check hiện có trong `ai/verification/` là nguồn hỗ trợ, không thay test của simulator mới hoặc đối chiếu độc lập.

Lưu test report, phiên bản code, expected/actual và reviewer. Việc người dùng đã duyệt thiết kế không có nghĩa các test simulator tự động pass.

**Điều kiện kết thúc giai đoạn:** toàn bộ test áp dụng pass, khác biệt đối chiếu được giải thích, có file kết quả debug và hướng dẫn chạy lại.

## 9. Phân công và thứ tự bàn giao

| Người | Việc chính trong giai đoạn này | Đầu ra |
|---|---|---|
| Hoàng Nam | Cấu trúc cache, mapping, access, exact LRU và runner | Simulator cùng bốn config |
| Quốc Thịnh | Parser, trace debug, kiểm tra counter/output và hỗ trợ test | Trace nhỏ, test runner và kết quả đối chiếu |
| Tô Dân | Đối chiếu implementation với thiết kế đã chốt; rà expected và bằng chứng | Bảng kiểm tra, validation notes và điều kiện chuyển bước |

Các thành viên có thể hỗ trợ nhau nhưng không để người viết một phần là người duy nhất xác nhận phần đó đúng.

Làm theo thứ tự: **config/state → mapping → D0 → D1/D2 → DAI → trace/runner → output → validation**. Có thể bổ sung test ngay sau từng phần thay vì chờ viết xong toàn bộ.

Sau khi giai đoạn này đạt, mới hoàn thiện generator W1–W5, chốt bố trí địa chỉ, sinh official traces và checksum, rồi thực hiện 96 run theo protocol. Không dùng trace official để tinh chỉnh thiết kế DAI-v1 đã chốt.

## 10. Nguồn đặc tả

- [Protocol](C:/Tai_Lieu_Hoc/CEA201/RBL/experiment_protocol.md).
- [Thiết kế đã chốt](C:/Tai_Lieu_Hoc/CEA201/RBL/ai/AI_DESIGN_FREEZE.md).
- [Pseudocode và expected tests trong R003](C:/Tai_Lieu_Hoc/CEA201/RBL/ai/responses/R003.md).
