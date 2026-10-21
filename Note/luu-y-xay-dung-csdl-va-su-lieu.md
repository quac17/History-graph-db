# Lưu ý khi xây dựng cơ sở dữ liệu và xử lý sử liệu

PostgreSQL là master registry: cấp mã mờ, giữ danh xưng, nguồn và log. Neo4j giữ node và edge theo đúng mã đó. ChromaDB giữ đoạn văn. Trong đồ án, ChromaDB chỉ có schema và vài bản ghi mẫu. Nạp embedding hàng loạt thuộc phần sau của Phase 1.

Ba việc dưới đây là quy tắc dữ liệu. Đồ án áp dụng quy tắc nguồn trên quan hệ và bước giải đại từ trong pipeline trích xuất. Quy trình tái bản đầy đủ và việc gỡ một kho đoạn văn lớn thuộc phần sau.

## Gỡ đoạn sử liệu sai

Một edge trên Neo4j có thể được nhiều đoạn văn củng cố. Xóa edge chỉ vì một đoạn sai sẽ mất các đoạn đúng còn lại.

Mỗi edge quan hệ, ví dụ `COMMANDED` hoặc `TOOK_PLACE_AT`, giữ:

- `source_chunk_ids`: các mã đoạn văn minh chứng.
- `evidence_count`: số phần tử của mảng đó.

Khi một đoạn bị gán nhãn sai hoặc trích xuất lỗi:

1. PostgreSQL đặt `chunk_status = REJECTED` trên đoạn đó. Đây là trạng thái của đoạn văn, không thay `DRAFT`, `VERIFIED`, `FLAGGED` của bản ghi trích xuất.
2. ChromaDB xóa hoặc vô hiệu hóa vector của đoạn, khi đoạn đó đã được nạp. Đồ án chưa nạp hàng loạt nên bước này chỉ có trong thiết kế.
3. Neo4j rút mã đoạn khỏi `source_chunk_ids` và tính lại `evidence_count`. Chỉ `DELETE` edge khi mảng rỗng.

```cypher
MATCH (p:Person {id: 'P00001'})-[r:COMMANDED]->(e:Event {id: 'EV00001'})
SET r.source_chunk_ids = [id IN r.source_chunk_ids WHERE id <> 'chunk_001'],
    r.evidence_count = size([id IN r.source_chunk_ids WHERE id <> 'chunk_001'])
WITH r
WHERE size(r.source_chunk_ids) = 0
DELETE r
```

Thiếu đoạn trích ngay từ lúc trích xuất thì bản ghi là `DRAFT`, chưa thành edge `SUPPORTS`. `REJECTED` dùng khi một đoạn đã nạp về sau bị xác định là sai.

## Tái bản

Không ghi đè văn bản gốc. Bản cũ và bản mới cùng được giữ.

Trên PostgreSQL:

- Bản cũ: `doc_status = SUPERSEDED`.
- Bản mới: `doc_version` tăng, `doc_status = ACTIVE`.
- Đoạn không đổi trỏ sang bản mới.
- Đoạn có sửa: đoạn cũ `is_deprecated = true`, tạo đoạn mới.

Trên ChromaDB, khi đã có vector:

- Đoạn cũ giữ vector, `is_latest = false`.
- Đoạn mới có `is_latest = true`.
- Bộ lọc mặc định của phần hỏi đáp sau này là `is_latest = true`. Muốn xem lịch sử đính chính thì bỏ lọc đó. Đồ án không làm lớp hỏi đáp.

Trên Neo4j, chỉ trích xuất lại đoạn đã sửa:

- Sửa chính tả, tri thức không đổi: thay mã đoạn trong `source_chunk_ids`, giữ node và edge.
- Sửa làm đổi sự kiện, ví dụ dời năm: rút đoạn cũ khỏi quan hệ cũ, xóa edge nếu đó là minh chứng duy nhất, rồi nạp quan hệ mới từ đoạn mới. Năm mới nằm ở thuộc tính `:TimeSpan`, không sửa mã `EV`.

Đối chiếu hai nguồn thành edge dị bản vẫn thuộc cuối Phase 1, không thuộc đồ án. Tái bản ở trên là phiên bản của cùng một tài liệu, khác với hai bộ sử kể lệch nhau.

## Đại từ và từ chỉ trỏ

Sử liệu dày đại từ (ông, y, ngài), tước hiệu (Quốc công, Thượng hoàng) và từ chỉ không gian, thời gian (nơi đây, bấy giờ, năm ấy). Nếu tạo node từ các từ đó, graph bị đứt.

Bốn bước, chạy trước khi khử trùng lặp danh xưng và trước khi tạo node:

1. Nhận span và gắn loại: đại từ người, tước hiệu, hoặc từ chỉ nơi và lúc.
2. Nối span về tiền đề trong cửa sổ ngữ cảnh. Trục người, trục nơi và trục lúc xét riêng. Ví dụ "Ông cho quân giả thua" nối về Trần Quốc Tuấn nếu câu trước vừa nêu người đó. "Tại đây" nối về sông vừa nêu. "Bấy giờ" nối về mốc vừa nêu.
3. Tra `entity_aliases` trên master registry để lấy mã đã có. "Ông" đã giải thành Trần Quốc Tuấn thì về `P00001` nếu danh xưng đó đã có. Mã mới chỉ do PostgreSQL cấp. Không nhét năm vào mã: mốc "năm 1284" là một `:TimeSpan` kiểu `TIM0002`, năm nằm ở thuộc tính.
4. Chỉ những mã đã giải mới vào tuple quan hệ. Neo4j không lưu đại từ làm node. ChromaDB giữ câu gốc và ghi `metadata.linked_entity_ids` bằng các mã đã giải.

Chưa đủ chắc thì `FLAGGED`, không tạo edge và không tạo node mới. Không có cam kết giải hết mọi đại từ.

Hai trường hợp thêm:

- Câu khuyết chủ ngữ: mô hình được đề xuất `implicit_subject` từ câu liền trước. Đề xuất không có đoạn làm tiền đề thì `FLAGGED`.
- Tước hiệu chung như "Thượng hoàng" hoặc "Vua": lọc thêm bằng mốc thời gian của đoạn, ví dụ tước đang dùng trong năm của đoạn. Vẫn nhiều ứng viên thì `FLAGGED`, không chọn người có điểm cao nhất để ghi thành sự thật.

## Tóm tắt thao tác

| Việc | PostgreSQL | ChromaDB | Neo4j |
| --- | --- | --- | --- |
| Gỡ đoạn sai | `chunk_status = REJECTED` | Xóa hoặc vô hiệu hóa vector nếu đã nạp | Rút mã đoạn khỏi `source_chunk_ids`. Xóa edge khi không còn minh chứng |
| Tái bản | Bản cũ `SUPERSEDED`, bản mới `ACTIVE` | Bản cũ `is_latest = false`, bản mới `is_latest = true` | Đổi mã đoạn, hoặc nạp quan hệ mới nếu sự kiện đổi |
| Đại từ | Tra `entity_aliases` lấy mã mờ | Giữ câu gốc, ghi `linked_entity_ids` | Chỉ nối mã đã giải. Span `FLAGGED` không thành edge |
