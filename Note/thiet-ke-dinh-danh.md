# Quy chuẩn định danh và bố trí cơ sở dữ liệu đa mẫu

Người thực hiện: Trần Việt Hoàng. MSSV: 25MSA13219.

Bản đầy đủ: `Note/thiet-ke-dinh-danh-va-bo-tri-csdl-da-mau.docx`. File này là bản làm việc để code và để các note khác trỏ tới.

## Mã định danh mờ

Mã là khóa thay thế, do PostgreSQL cấp qua sequence. Mã không chứa tên, danh xưng, năm sinh hay năm sự kiện. Năm sinh và năm sự kiện là thuộc tính, vì sử liệu có thể ghi lệch nhau. Đổi tên hiển thị hoặc đính chính năm không đổi mã.

| Chủ thể | Label | Mẫu | Ví dụ |
| --- | --- | --- | --- |
| Con người | `:Person` | `P` + 5 số | `P00001` |
| Sự kiện | `:Event` | `EV` + 5 số | `EV00001` |
| Tổ chức | `:Group` | `GRP` + 4 số | `GRP0001` |
| Không gian | `:Place` | `LOC` + 4 số | `LOC0001` |
| Thời gian | `:TimeSpan` | `TIM` + 4 số | `TIM0001` |
| Hiện vật | `:Artifact` | `ART` + 4 số | `ART0001` |
| Kế sách, tư tưởng | `:Concept` | `CON` + 4 số | `CON0001` |
| Nguồn | `:Source` | `SRC` + 4 số | `SRC0001` |

Không ghép tên và năm vào mã. Tiền tố cũ `PERSON_`, `STRAT_`, `IDEO_`, `TIME_`, `ERA_` không còn. Concept dùng `CON`. TimeSpan dùng `TIM`.

Một người nhiều danh xưng cùng trỏ một mã, qua bảng `entity_aliases`. Nhiều người trùng tên là nhiều mã. Nhiều sự kiện cùng địa danh là nhiều mã `EV`, tách nhau bằng thuộc tính và quan hệ thời gian, không bằng cách nhét năm vào mã.

Mô hình không được tự bịa mã. PostgreSQL là master registry: cấp mã mờ, giữ danh xưng, nguồn và log. Mã mới chỉ do PostgreSQL sinh khi master registry chưa có thực thể đó.

## Ba trạng thái kiểm duyệt

`verification_status` trên master registry: `DRAFT`, `VERIFIED`, `FLAGGED`. Kèm `confidence_score`.

- `DRAFT`: thiếu đoạn trích, chưa được xem là đã kiểm.
- `VERIFIED`: đã có đoạn trích và đã qua bước gộp danh xưng hoặc đã được người duyệt.
- `FLAGGED`: chưa đủ chắc để tự gộp, hoặc vi phạm ràng buộc niên đại. Không tự sửa năm, không tự tạo node mới.

## Vai trò ba database

PostgreSQL là master registry, nguồn chân lý của mã. Ba bảng cốt lõi:

- `dim_entities`: `entity_id`, `entity_type`, `canonical_name`, `wikidata_id`, `verification_status`, `confidence_score`.
- `entity_aliases`: danh xưng, loại danh xưng, trích dẫn nguồn. Chỉ mục B-Tree và `pg_trgm` để đối khớp mờ.
- `source_documents`: mã nguồn, nhan đề, người biên soạn, góc nhìn, đường dẫn tệp.

Neo4j giữ node và edge. Khóa node là `entity_id` đã cấp ở PostgreSQL. ChromaDB giữ đoạn văn; `metadata.linked_entity_ids` và `metadata.source_id` dùng cùng các mã đó. Cắt đoạn hàng loạt và truy vấn lai thuộc phần sau của đồ án. Đồ án dựng schema vector và vài bản ghi mẫu.

Khi cần đổi embedding hoặc dựng lại graph, dữ liệu được tái tạo từ PostgreSQL.

## Thứ tự trong đồ án

1. LLM đề xuất bản ghi và quan hệ, chưa được cấp mã cuối.
2. Tra `entity_aliases` trên PostgreSQL. Khớp thì lấy mã cũ. Chưa khớp đủ thì `FLAGGED`. Thực thể mới do sequence cấp mã.
3. Nạp Neo4j bằng `MERGE` trên mã đó. Cùng mã thì cập nhật.
4. Gắn mã vào metadata của đoạn văn khi có bản ghi vector. Nạp hàng loạt để sau.
