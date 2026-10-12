# Pipeline Phase 1

Người thực hiện: Trần Việt Hoàng. MSSV: 25MSA13219.

Đồ án là phần mở đầu Phase 1 của dự án. Phần dưới gạch đâu là việc của đồ án, đâu để phần còn lại của Phase 1.

## Trong đồ án

### 1. Trích xuất

Đầu vào: một đoạn văn bản đã làm sạch.

Đầu ra: JSON đúng schema Pydantic của hệ thống chủ thể và từ khóa ở `01-bai-toan/he-thong-chu-the-va-tu-khoa.md`, gồm hai danh sách:

- `entities`: các bản ghi chủ thể mà đoạn chữ có nói tới. Mỗi bản ghi có label (một trong tám chủ thể), mã, trường phân loại và các từ khóa của chủ thể đó. Từ khóa nguồn không nói thì null.
- `relations`: các quan hệ, mỗi quan hệ gồm mã đầu, loại edge, mã cuối.

Sai schema thì API trả lỗi, không nạp Neo4j. Schema kiểm:

- Mã do PostgreSQL cấp, đúng mẫu khóa mờ ở `Note/thiet-ke-dinh-danh.md`. LLM không được tự đặt mã.
- Trường phân loại chỉ nhận giá trị trong danh mục đóng. Nhãn lạ thì từ chối.
- Mỗi loại edge chỉ nối đúng cặp label, ví dụ `COMMANDED` đi từ `:Person` tới `:Event`. Sai cặp thì từ chối.
- Mô hình không tự sinh mã linked open data như Wikidata QID.

LLM chỉ đề xuất giá trị và danh xưng, chưa cấp mã cuối. Nguồn của mỗi từ khóa có giá trị và của mỗi quan hệ là `char_start`, `char_end` hoặc câu trích. Không có đoạn trích thì từ khóa hoặc quan hệ đó không được nạp như đã xác nhận. Trạng thái trên master registry (PostgreSQL cấp mã mờ, giữ danh xưng, nguồn và log) là `DRAFT`.

Đo trên gold set khoảng 150–200 đoạn sử liệu, do người gắn nhãn chủ thể, từ khóa và quan hệ, không phải do chính mô hình tự chấm. Mục tiêu proposal đồ án: độ khớp F1 theo từ khóa từ 85% đến 90%, độ khớp F1 theo quan hệ từ 75% đến 85%.

### 2. Khử trùng lặp danh xưng

Thứ tự, làm mức vừa sức:

1. Tra `entity_aliases` trên PostgreSQL, chỉ mục tên và `pg_trgm`. Khớp chắc thì lấy `entity_id` đã có.
2. Chưa khớp chắc thì đo string similarity, threshold khởi điểm 0.82, rồi so embedding của tên cùng một câu ngữ cảnh. Threshold là giả định, tinh chỉnh trên dev set.
3. Vẫn dưới threshold thì trả `FLAGGED`, không âm thầm tạo node mới. Thực thể mới chỉ được mã khi sequence của PostgreSQL cấp.

Bước này chạy cho các bản ghi `:Person`, `:Group` và `:Place`. Mã sau bước này được thay vào hai đầu của mọi quan hệ liên quan.

Demo không gắn vào một nhân vật có tên. Điều kiện là: một danh xưng đã có trong `entity_aliases` phải về đúng mã cũ, không sinh node thứ hai.

Hai sự kiện cùng địa danh nhưng khác thời điểm là hai mã `EV`. Không phân biệt chúng bằng cách nhét năm vào mã.

Mục tiêu proposal đồ án: precision từ 90% đến 95%.

### 3. Nạp Neo4j

JSON đã khử trùng lặp danh xưng thành Cypher theo batch. Node và edge đều dùng `MERGE`. Chạy lại cùng một mã thì cập nhật, không nhân đôi node. Ghi `ingest_logs`.

Kiểm ràng buộc trước khi ghi:

- Người có năm sinh và năm mất mà năm sự kiện nằm ngoài khoảng đó thì `FLAGGED`. Không tự sửa năm.
- Địa danh lấy tên ngày nay từ danh mục địa danh đã điền tay. Mô hình không đoán tên ngày nay.
- Bản ghi hoặc quan hệ thiếu đoạn trích thì `DRAFT`, không có edge `SUPPORTS`.

### 4. Demo hội đồng, khoảng ba phút

1. Mở master registry và graph đã có sẵn một số node Person.
2. Dán một đoạn sử liệu hội đồng chọn, chưa có trong kho.
3. Bấm trích xuất, hiện các bản ghi chủ thể và quan hệ, mỗi giá trị kèm đoạn trích.
4. Bấm nạp. Danh xưng trùng nhập vào node cũ. Chủ thể mới và quan hệ mới thành nhánh mới.
5. Chỉ bảng độ khớp F1 theo từ khóa, theo quan hệ, và precision trên test set của gold set.

Giao diện: Streamlit. Không có chatbot cho học sinh.

## Sau đồ án, vẫn trong Phase 1

- Cắt đoạn theo nghĩa và embedding hàng loạt.
- Gắn `linked_entity_ids` cho mọi đoạn văn.
- Hybrid search giữa graph và vector, đo độ trễ. Proposal dự án đặt mốc dưới 1,5 đến 2 giây. Đồ án không bị chặn bởi mốc này.
- Stance classifier (phân loại lập trường): edge `CORROBORATES` và `CONTRADICTS` giữa assertion của Đại Việt sử ký và Nguyên sử.
- Hoàn thiện API đủ cho Phase 2 gọi.

Ví dụ dị bản, chỉ để thiết kế sau, không demo nếu chưa có nhãn:

```text
(Source_DVSK)-[:ASSERTS]->(Assertion_1: cắm cọc, dụ theo thủy triều)
(Source_NguyenSu)-[:ASSERTS]->(Assertion_2: rút vì lương và địa hình)
(Assertion_1)-[:CONTRADICTS {aspect:'nguyen nhan'}]->(Assertion_2)
```

Hai assertion cùng tồn tại. Pipeline không chọn một câu làm sự thật duy nhất.
