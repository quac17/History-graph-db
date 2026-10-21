# CHƯƠNG 3: THIẾT KẾ HỆ THỐNG / PHƯƠNG PHÁP

Track Hybrid. Mục 3.1–3.3 lấy Track A làm chính. Thêm dữ liệu và cách trích xuất của Track B ở mức vừa đủ.

## 3.1 Kiến trúc tổng thể

PostgreSQL là master registry: cấp mã mờ, giữ danh xưng, nguồn và log. Neo4j giữ node và edge bằng đúng mã đó. ChromaDB giữ đoạn văn. Đồ án nạp master registry và graph. Vector database trong đồ án chỉ có schema và vài bản ghi mẫu.

Ba bảng tra cứu nằm trên PostgreSQL và không cấp mã chủ thể: `ref_historical_eras`, `ref_ganzhi_cycles`, `ref_measurement_units`. Một mốc trong câu sử liệu vẫn là `:TimeSpan` với mã `TIM` và bốn số. Một đơn vị đo là một hàng danh mục, không phải node.

Tài liệu có `doc_status` nhận `ACTIVE` hoặc `SUPERSEDED`, và `doc_version`. Đoạn văn bị xác định là sai có `chunk_status = REJECTED`. Bản ghi trích xuất vẫn dùng `DRAFT`, `VERIFIED` và `FLAGGED`. Không dùng trạng thái tài liệu để thay trạng thái kiểm của bản ghi.

## 3.2 Thiết kế phân hệ và luồng thông tin

Luồng đi từ đoạn chữ sang JSON có hai danh sách, bản ghi chủ thể và quan hệ, rồi sang mã do PostgreSQL cấp, rồi sang Neo4j. Thời gian và số đo đi cùng luồng đó, không có pipeline riêng.

Một `:TimeSpan` lưu `raw_text`. Nếu câu có ngày, tháng âm, can chi hoặc niên hiệu thì các trường đó được điền. `solar_year_start` và `solar_year_end` ghi khoảng dương lịch. Hai năm khác nhau thì không gộp thành một năm ở giữa. `solar_date_iso_start` và `solar_date_iso_end` để trống khi chưa có phép đổi đã kiểm. Sự kiện nối thời gian bằng `OCCURRED_DURING`.

Số đo là danh sách thuộc tính của chủ thể mà câu nói tới. Mỗi phần tử có biểu thức gốc, số lượng gốc, đơn vị gốc, loại việc đo, và giá trị SI. "3 vạn quân" được hiểu là 30.000 người chỉ khi ngữ cảnh là quân số và cách đếm là thập phân. "Hộc lương" không đổi ra kilogam nếu nguồn không nói cách đong. Hệ số lấy từ `ref_measurement_units` phải kèm `historical_context`. Không có hàng phù hợp thì giá trị SI là null.

Edge trên Neo4j có `source_chunk_ids` và `evidence_count`. Nhiều đoạn cùng nói một quan hệ thì cùng nằm trong mảng. Khi một đoạn chuyển `REJECTED`, mã đoạn bị rút khỏi mảng. Edge chỉ bị xóa khi mảng rỗng. Thiếu đoạn trích ngay từ đầu thì bản ghi là `DRAFT` và chưa có edge `SUPPORTS`.

Tái bản không ghi đè văn bản. Bản cũ thành `SUPERSEDED`, bản mới là `ACTIVE`. Đoạn chỉ sửa chính tả thì đổi mã đoạn trên edge. Đoạn làm đổi sự kiện thì rút minh chứng cũ và nạp quan hệ mới. Mã sự kiện không đổi chỉ vì năm được đính chính. Năm mới nằm ở `:TimeSpan`. Quy trình đủ cho một kho lớn, gồm cả vector `is_latest`, thuộc phần sau của Phase 1. Đồ án chốt trạng thái và quy tắc, chưa chạy quy trình đó trên nhiều lần xuất bản.

## 3.3 Pipeline xử lý và tích hợp mô hình

Trước khi khử trùng lặp danh xưng, pipeline giải đại từ và từ chỉ trỏ.

- Bước nhận span chia ba loại: đại từ người, tước hiệu, từ chỉ nơi hoặc lúc.
- Bước tìm tiền đề nhìn các câu liền trước trong cùng đoạn. "Ông" nối về người vừa nêu. "Tại đây" nối về nơi vừa nêu. "Bấy giờ" nối về mốc vừa nêu. Câu không có chủ ngữ được đề xuất chủ ngữ ngầm từ câu trước. Không có câu làm tiền đề thì không điền.
- Danh xưng đã giải được tra trên `entity_aliases`. Khớp thì lấy mã cũ. Tước hiệu chung như "Vua" hoặc "Thượng hoàng" chỉ gắn một mã khi mốc của đoạn lọc còn một người. Còn nhiều người thì `FLAGGED`.
- Chỉ mã đã giải mới đứng ở hai đầu quan hệ. Graph không có node tên "ông" hay "đây". Câu gốc vẫn nằm ở nguồn và, khi có bản ghi vector, ở tài liệu của ChromaDB cùng `linked_entity_ids`.

Bước này không cam kết giải hết span. Các công trình trên văn kể tiếng Việt cho thấy chất lượng phụ thuộc mô hình và dữ liệu [3], [4]. Span `FLAGGED` bị loại khỏi mẫu số của precision khử trùng lặp danh xưng, vì hệ thống đã không tự gộp.

Sau bước giải đại từ là khử trùng lặp danh xưng cho người, tổ chức và nơi, rồi `MERGE` vào Neo4j theo mã đã cấp. LLM không được tự đặt mã. Sai schema thì bị từ chối, không nạp.
