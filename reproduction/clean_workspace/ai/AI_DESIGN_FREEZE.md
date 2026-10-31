# Đặc tả đã chốt DAI-v1 — XOR 2-way

**Trạng thái: ĐÃ CHỐT THIẾT KẾ — DESIGN FREEZE.**

Đặc tả dưới đây chốt phương án B — XOR 2-way trong R003. Người dùng đã xác nhận trong cuộc trò chuyện rằng đã kiểm tra và xác nhận thiết kế, với Trương Tô Dân là người kiểm tra và người xác nhận. Việc chốt này cho phép chuyển sang triển khai simulator; không xác nhận simulator đã vượt validation hoặc đã có official benchmark.

## Nhận diện

- Design ID đã chốt: DAI-v1
- Protocol: Q10-PROTOCOL-v1.0, `inputs/experiment_protocol.md`
- Tên phương án: B — XOR set-associative tĩnh, 64 set × 2 way
- Prompt/response IDs: P001/R001, P002/R002, P003/R003; không có lượt làm rõ bổ sung
- Căn cứ đầy đủ: [R003](responses/R003.md), tự phản biện tại [R002](responses/R002.md); giữ nguyên bản đề xuất ban đầu [R001](responses/R001.md)
- Thời điểm ghi nhận xác nhận chốt: 2026-10-31T15:33:41+07:00 — theo xác nhận trực tiếp của người dùng trong cuộc trò chuyện; không suy ngược thời điểm thực hiện kiểm tra trước đó.
- Người kiểm tra: Trương Tô Dân — QE210127
- Người xác nhận chốt: Trương Tô Dân — QE210127
- Phiên bản nguồn/Git commit: chưa có repository Git được phát hiện tại workspace; không có simulator commit được xác nhận
- Checksum artefact: `evidence/SHA256SUMS.json`, được tạo bằng SHA-256 sau khi lưu các file; manifest không tự chứa hash của chính nó
- Mốc xử lý/lưu câu trả lời: [AI_SESSION_LOG.md](AI_SESSION_LOG.md) và `evidence/SESSION_TIMES.json`; đây không phải mốc nhóm duyệt

## Cấu hình và đặc tả đã chốt

| Thành phần | Nội dung |
|---|---|
| Data capacity | 4 KiB theo protocol |
| Line size | 32 byte theo protocol |
| Địa chỉ/access | Unsigned 32 bit; R/W 4 B; địa chỉ chia hết cho 4 và trong 0..2^32−4 |
| Write policy | Write-back + write-allocate |
| Prefetch/bypass | Tắt trong thí nghiệm chính |
| Sets/ways | 64 set × 2 way × 32 B = 4.096 B, tổng 128 line |
| Index/block/tag | b=a>>5; s=(b XOR (b>>6)) AND 63; t=b>>6, tag 21 bit; offset=a AND 31 |
| Vị trí hợp lệ | Chỉ (s,0) hoặc (s,1); một bản sao valid/block |
| Lookup và hit | Tra hai way ở s; valid và tag khớp duy nhất; W đặt dirty, R giữ dirty; cập nhật LRU cả R/W hit |
| Miss/insertion | Ưu tiên invalid; nhiều invalid chọn way nhỏ nhất; nếu đầy chọn LRU; một fill 32 B/miss, kể cả W miss |
| Tập victim/LRU | Hai way trong s; bit lru_way[s] chỉ victim khi cả hai valid; sau hit/fill ở w đặt lru_way[s]=1−w |
| Dirty writeback | Chỉ victim valid+dirty, trước ghi đè; base khôi phục bằng công thức dưới đây; không đếm writeback như demand access |
| Reset đầu run | Xóa valid/dirty/tag/dữ liệu mô hình/counters/debug events; tất cả LRU bit=0; tắt đếm giai đoạn đo |
| Ranh warmup/đo | Sau 10.000 warmup chỉ reset counters và bật đếm; giữ cache/dirty/LRU, không flush; đo 100.000 access |
| Cuối khoảng đo | Không tự flush vào traffic chính; nếu drain riêng phải có counter flush riêng |
| Metadata | Tag+valid/dirty 368 B; exact LRU 8 B; tổng 376 B bit logic, tách khỏi 4 KiB dữ liệu |
| Input bổ sung/học | Không PC, nhãn sensor, profile, training, remapping, relocation hoặc thông tin tương lai |

## Hàm khôi phục và thứ tự thao tác bắt buộc

```text
recover_block(s,t) = (t << 6) | (s ^ (t & 63))
writeback_base = recover_block(s, victim_tag) << 5
```

Đặt `l=b&63`, `t=b>>6`; `s=l XOR (t&63)` nên thu lại duy nhất `l=s XOR (t&63)`. Vì vậy `(s,t)` phân biệt đúng mọi b 27 bit. Không dùng công thức writeback của D1: b=64 tại s=1,t=1 phải trả base=2.048, không phải 2.080.

Pseudocode chuẩn để triển khai nằm ở R003 mục 3; các quy tắc dưới đây phải được giữ khi chuyển thành code:

1. Validate op/size/alignment/range trước mọi thay đổi state/counters.
2. Lookup valid+tag; assert không quá một hit. Hit cập nhật dirty khi W và exact LRU.
3. Miss đếm đúng một read/write miss; chọn invalid trước LRU. Hai invalid chọn way 0; một invalid chọn way đó, bất kể bit LRU.
4. Nếu victim valid, tăng eviction; dirty mới writeback line cũ theo tag cũ trước ghi đè. Clean không writeback, invalid không eviction.
5. Fill đúng một line mới 32 B; đặt valid, tag, dirty=false rồi áp thao tác W nếu có; sau fill cập nhật LRU như hit.

Trace tối thiểu chỉ có op/address/size, không có payload. Simulator có thể mô phỏng tag/flags/traffic; không gọi đây là kiểm chứng giá trị word end-to-end nếu chưa bổ sung memory/data model.

Counter giai đoạn đo: accesses, hits, misses, read_misses, write_misses, evictions, dirty_writebacks, line_fills. Giữ `hits+misses=accesses`, `read_misses+write_misses=misses`, `line_fills=misses`, `dirty_writebacks<=evictions<=misses`. Traffic chính `(line_fills+dirty_writebacks)×32 B`.

## Chi phí và phép so công bằng

| Thiết kế | Metadata logic | Giả định replacement |
|---|---:|---|
| D0 | 352 B | Không cần LRU |
| D1 | 376 B | 1 bit/set, exact LRU 2-way |
| D2 | 416 B | Rank 2 bit/way, 32 set × 4 way; exact LRU |
| DAI-v1 | 376 B | Như D1 |

Các số gồm tag, valid/dirty và replacement; chưa gồm ECC, control logic, dây dẫn, comparator hoặc object overhead Python. Metadata DAI bằng D1, hơn D0 24 B; tổng dữ liệu + metadata DAI 4.472 B. XOR không có bảng trạng thái nhưng cần logic tính toán; chưa có timing/area/power được đo.

DAI–D1 giữ 64 set, 2 way, tag width, LRU và các biến kiểm soát; thay hàm nhóm set và phép khôi phục block đi kèm. DAI–D0 thay cả associativity và mapping; không quy toàn bộ cải thiện cho XOR. D2 là đối chứng trọn cấu hình khác associativity. Mọi thiết kế dùng cùng input trace, seed và khoảng đo.

## Lý do lựa chọn

Chọn B vì dùng lại lõi D1 với một bit exact LRU/set, không cần học hoặc quản lý cặp slot chồng lấn, có công thức tag/writeback kiểm chứng được. A đơn giản hơn nhưng chỉ một vị trí/block; C hợp lệ nhưng nhiều trạng thái và metadata hơn theo bản R001. Không chọn bằng kết quả benchmark hoặc lời hứa thắng D0. Đây là AI hỗ trợ thiết kế, không phải ML online.

## Test dự kiến và giới hạn

Test đầy đủ và counter kỳ vọng nằm ở R003 mục 6: T01–T06, high-bit/max-address, alias, dirty read hit, writeback base, warmup giữ contents/LRU, invalid input và reset đầu run. Ví dụ:

- `R0,R2080,R0,R4160,R2080` → M,M,H,M,M; hai eviction, không writeback.
- `W2048,R2048,R32,R4192` → M,H,M,M; một dirty writeback tại 2048, traffic 128 B.
- `R0,R2080,R4160,R0,R2080,R4160` → sáu miss của DAI, trong khi D0/D1 có thể giữ ba block sau nạp; đây là phản ví dụ tính tay.

Kiểm tra bổ sung của cùng AI đã chạy sau khi lưu R003: `verification/check_q10_spec.mjs`, kết quả `verification/AI_SELF_CHECK.json` có 16 nhóm PASS. Nó kiểm tra số học, round-trip trên một miền con và các probe biên, expected của trace nhỏ bằng mô hình full block ID/LRU list, cùng tính nguyên vẹn input/prompt. Nó không phải simulator nghiên cứu, không kiểm tra toàn bộ triển khai LRU bit/way vật lý, không phải validation độc lập hay official benchmark. Chi tiết phạm vi tại `verification/README.md`.

Giả thuyết W1 ít lợi với line không tái sử dụng; W2/W3 phụ thuộc working set/căn chỉnh/thứ tự reuse; W4 phụ thuộc base/interleaving; W5 có thể tách stride 4 KiB nhưng chỉ là stress có cấu trúc. Cùng 4 KiB tổng cộng vẫn có thể có >2 block tranh một hashed set. Không kết luận timing/điện năng/deadline từ miss rate.

Base address, generator W3/W4, trace manifests, môi trường simulator và hit-time sensitivity bổ sung còn cần hoàn thiện đúng các bước protocol trước official runs. Chúng không thay định nghĩa mapping ở đây. Việc kiểm tra đặc tả và xác nhận của Trương Tô Dân được ghi nhận theo thông báo trực tiếp của người dùng; validation simulator vẫn là công việc tiếp theo, chưa được đánh dấu hoàn thành.

## Xác nhận chốt thiết kế

- [x] Đã giữ nguyên P001–P003 và lưu câu trả lời gốc R001–R003 tuần tự; không có lượt làm rõ khác.
- [x] AI đã đặc tả index/tag/victim/dirty/reset và kết quả logic kỳ vọng; chưa thay cho reviewer nhóm.
- [x] AI đã đối chiếu cấu hình với protocol, không phát hiện vi phạm tại mức đề xuất.
- [x] Trương Tô Dân đã hoàn thành kiểm tra đặc tả và ví dụ tính tay — theo xác nhận của người dùng.
- [x] Đã ghi thời điểm ghi nhận xác nhận chốt và người xác nhận thực tế.
- [x] Đã lưu phiên bản artefact bằng nội dung và SHA-256 trong manifest; không có Git commit được xác nhận.

Từ mốc ghi nhận xác nhận trên, triển khai DAI-v1 theo đặc tả này. Không đổi hàm index, associativity hoặc policy sau khi xem official results mà vẫn giữ tên DAI-v1. Sửa bug triển khai không được làm thay đổi thiết kế một cách âm thầm. Tài liệu trình bày đặc tả hiện tại, không kèm phần lịch sử phiên bản chi tiết.
