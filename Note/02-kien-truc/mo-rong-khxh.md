# Mở rộng sang môn khác — không làm trong đồ án

Người thực hiện: Trần Việt Hoàng. MSSV: 25MSA13219.

Hạ tầng ba database giữ nguyên. Đổi ontology. Đây là hướng của dự án, không phải hạng mục bảo vệ đồ án.

| Môn | Node trung tâm | Edge gợi ý |
| --- | --- | --- |
| Lịch sử | Person, Group, Event, Place, TimeSpan, Artifact, Concept, Source | COMMANDED, TOOK_PLACE_AT, EMPLOYED_STRATEGY, LEFT_HERITAGE, SUPPORTS |
| Triết | Concept, Philosopher, Treatise | INFLUENCED_BY, CRITIQUES, PROPOSES, DERIVES_FROM |
| Văn | Author, Work, Character, Movement | WRITTEN_BY, BELONGS_TO_GENRE, INSPIRED_BY |
| Địa | Place, Phenomenon, AdminUnit | LOCATED_IN, ADJACENT_TO, EVOLVED_IN |
| Chính trị, xã hội | Institution, Policy, PoliticalEvent, Movement | ENACTED_BY, OPPOSES, SUPPORTS, IMPACTS |

Phần dùng lại: Neo4j, ChromaDB, PostgreSQL, cách gắn `linked_entity_ids`, FastAPI.

Phần viết lại: hệ thống chủ thể và từ khóa của môn đó, danh mục phân loại, edge, câu Cypher mẫu, tập văn bản nguồn. Cách đặt mã theo tiền tố và mốc phân biệt dùng lại được.

Đừng trộn node triết vào graph thí điểm Bạch Đằng. Một graph một miền trong đồ án.
