# Đối chiếu tính tay cho simulator Q10

Các bảng dưới đây là expected suy ra từ đặc tả và được tự động đối chiếu trong validation. Chưa ghi tên thành viên nhóm là người đã kiểm tra implementation; người đọc thực hiện kiểm tra rồi mới điền xác nhận cuối tài liệu.

Năm trace nhỏ tại `traces/debug/` đều là input kiểm tra, không phải W1–W5 official. Địa chỉ dùng đơn vị byte. M=miss, H=hit; thứ tự trong mỗi ô tương ứng thứ tự dòng của trace.

## 1. Kết quả kỳ vọng bốn thiết kế

| Trace | D0 | D1 | D2 | DAI-v1 |
|---|---|---|---|---|
| repeat: R0,R0 | MH | MH | MH | MH |
| lru: R0,R2080,R0,R4160,R2080 | MMHHH | MMHHH | MMHHH | MMHMM |
| dirty: W2048,R2048,R32,R4192 | MHMM | MHMM | MHMM | MHMM |
| boundary: R28,R32,R28 | MMH | MMH | MMH | MMH |
| warmup: W0,R2080,R0; đo R4160,R0 | HH | HH | HH | MH |

Ở trace dirty, D0/D1/D2 không có eviction nên traffic là 96 B, WB=0; DAI có một dirty eviction nên traffic 128 B, WB=1. Ở trace warmup, chỉ hai access cuối được đếm; phần khởi động vẫn thay cache/dirty/LRU.

## 2. Chi tiết T03 cho DAI

Các block 0,65,130 đều có index XOR 0, tag lần lượt 0,1,2. Way invalid nhỏ nhất được chọn trước.

| Bước | Thao tác | H/M | Nội dung sau access (way 0 / way 1) | lru_way |
|---|---|---|---|---:|
| 1 | R0 | M | b0 / invalid | 1 |
| 2 | R2080 | M | b0 / b65 | 0 |
| 3 | R0 | H | b0 / b65 | 1 |
| 4 | R4160 | M | b0 / b130; loại b65 | 0 |
| 5 | R2080 | M | b65 / b130; loại b0 | 1 |

Tổng: accesses=5, hits=1, misses=4, read_misses=4, write_misses=0, eviction=2, dirty_writeback=0, fills=4, traffic=128 B.

## 3. Dirty eviction và nghịch đảo XOR

DAI: b64 (a2048), b1 (a32), b131 (a4192) đều thuộc set 1, tag lần lượt 1,0,2.

1. W2048: miss, đặt b64 vào way 0, dirty=true.
2. R2048: hit, dirty vẫn true; way 1 là LRU.
3. R32: miss, dùng way 1 trống; way 0 trở thành LRU.
4. R4192: miss, loại b64 dirty tại way 0. Khôi phục `(1<<6)|(1^(1&63)) = 64`, ghi trả base=2048; nạp b131.

Tổng: H=1, M=3, read_miss=2, write_miss=1, eviction=1, WB=1, fills=3, traffic=(3+1)×32=128 B. Ghi trả 2080 là lỗi dùng công thức modulo cho XOR.

## 4. Ranh giới line và warmup

R28 thuộc block 0, R32 thuộc block 1. Vì hai block có vị trí riêng ở cả bốn design, R28,R32,R28 cho MMH.

Warmup DAI W0,R2080,R0 tạo b0 dirty và b65 clean trong set 0, với b65 là LRU. Reset counter không reset cache. Đo R4160 loại b65 clean (M), sau đó R0 vẫn hit và dirty. Counter đo: access=2,H=1,M=1,eviction=1,WB=0,fills=1,traffic=32 B.

## 5. Kiểm tra exact LRU của D2

R0,R1024,R2048,R3072 nạp b0,b32,b64,b96 vào set 0. Chạm lại b0 rồi R4096 (b128): phải loại b32. Fill b128 làm nó mới nhất; R5120 (b160) tiếp theo phải loại b64. Nếu W0 thay R0 ở bước chạm lại, victim vẫn như trên và b0 phải dirty.

## 6. Xác nhận kiểm tra implementation của nhóm

- Người kiểm tra: [Điền sau khi thực hiện]
- Thời điểm: [Điền thời điểm thật, UTC+07:00]
- Phiên bản/fingerprint nguồn: [Lấy từ summary.json của lần kiểm tra]
- Các trace đã đối chiếu: [Điền cụ thể]
- Kết quả và khác biệt: [Điền sau khi kiểm tra]

Việc Dân đã xác nhận thiết kế trước giai đoạn này không được tự chuyển thành xác nhận implementation mới đã pass. Báo cáo tự động và checksum nằm trong thư mục được chỉ bởi `validation/LATEST.txt`.
