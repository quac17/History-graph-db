# Bốn tầng database

Người thực hiện: Trần Việt Hoàng. MSSV: 25MSA13219.

Một loại database không đủ. PostgreSQL là master registry: cấp mã mờ, giữ danh xưng, nguồn và log. Neo4j giữ quan hệ, dùng đúng mã đó. ChromaDB giữ đoạn văn, metadata cũng dùng đúng mã đó. Agent là tầng gọi graph và vector, thuộc Phase 2. Đồ án dựng cả ba database. Đồ án bắt buộc nạp master registry và graph. Vector database trong đồ án chỉ cần schema và một bản ghi mẫu. Liên kết hàng loạt giữa đoạn văn và node nằm ở phần sau của Phase 1. Quy chuẩn nằm ở `Note/thiet-ke-dinh-danh.md`.

## Tầng 1 — Neo4j

Vai trò: mỏ neo. Câu trả lời về quan hệ sau này chỉ được dùng edge có trong graph.

Công nghệ proposal ghi: Neo4j 5.x. Virtuoso và Fuseki là phương án RDF, không phải sản phẩm phải bàn giao.

Label của node theo hệ thống chủ thể và từ khóa ở `01-bai-toan/he-thong-chu-the-va-tu-khoa.md`: `Person`, `Group`, `Event`, `Place`, `TimeSpan`, `Artifact`, `Concept`, `Source`.

Ràng buộc nên tạo ngay sprint 1–2:

- `id` là duy nhất trên từng label trong tám label chủ thể, và trùng `entity_id` đã cấp ở PostgreSQL.
- `id` đúng mẫu khóa mờ: `P` + 5 số, `EV` + 5 số, `GRP`/`LOC`/`TIM`/`ART`/`CON`/`SRC` + 4 số. Không ghép tên hay năm vào mã.
- Trường phân loại như `Event.event_type`, `Place.spatial_category` nằm trong danh mục đóng.
- Mọi `Event` dùng để demo phải có ít nhất một `Source` qua edge `SUPPORTS`.

```cypher
CREATE CONSTRAINT person_id IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT event_id IF NOT EXISTS FOR (e:Event) REQUIRE e.id IS UNIQUE;
```

Ví dụ:

```cypher
MERGE (p:Person {id:'P00001'})
  SET p.canonical_name = 'Trần Quốc Tuấn',
      p.historical_role_class = 'MilitaryCommander',
      p.aliases = ['Trần Hưng Đạo', 'Hưng Đạo Vương', 'Hưng Đạo Đại Vương', 'Tiết chế Quốc công']
MERGE (e:Event {id:'EV00001'})
  SET e.event_name = 'Trận Bạch Đằng năm 1288', e.event_type = 'MilitaryBattle'
MERGE (l:Place {id:'LOC0001'})
  SET l.historical_name = 'Sông Bạch Đằng', l.spatial_category = 'Battlefield'
MERGE (c:Concept {id:'CON0001'})
  SET c.concept_name = 'Cọc ngầm đón nước triều', c.concept_category = 'MilitaryTactic'
MERGE (p)-[:COMMANDED]->(e)
MERGE (e)-[:TOOK_PLACE_AT]->(l)
MERGE (e)-[:EMPLOYED_STRATEGY]->(c)
```

Truy vấn mẫu khi đã có alias:

```cypher
MATCH (p:Person)-[r]->(e:Event)
WHERE p.canonical_name = 'Trần Quốc Tuấn' OR 'Hưng Đạo Đại Vương' IN p.aliases
RETURN p, r, e
```

Danh xưng gốc nằm ở `entity_aliases` trên PostgreSQL. Neo4j có thể giữ bản sao tên hiển thị để xem graph. Không tạo node Person mới cho từng cách gọi. Trường `wikidata_id` được phép trống.

## Tầng 2 — ChromaDB

Vai trò: semantic search, tức tìm đoạn văn khi câu hỏi không trùng từ khóa, rồi nhảy sang node.

Công nghệ: ChromaDB trong đồ án. Milvus và pgvector là phương án thay. Embedding model ghi trong proposal: `bkai-foundation-models/vietnamese-bi-encoder` hoặc `bge-m3`.

Mỗi bản ghi:

```json
{
  "id": "vec_chunk_1088",
  "document": "Trần Hưng Đạo cho cắm cọc vạt nhọn đầu bịt sắt xuống lòng sông Bạch Đằng...",
  "metadata": {
    "linked_entity_ids": ["P00001", "EV00001", "LOC0001"],
    "event_type": "MilitaryBattle",
    "source_id": "SRC0001",
    "page": "58"
  }
}
```

Không có `linked_entity_ids` thì đoạn đó không được dùng để khẳng định quan hệ.

Hai chiều:

- Vector sang graph: lấy `linked_entity_ids`, mở các node lân cận bằng Cypher.
- Graph sang vector: metadata filter theo `EV00001` để chỉ lấy đoạn văn của đúng sự kiện.

Metadata filter theo mã chỉ giới hạn tập đoạn văn được dùng. Nó không làm câu trả lời đúng 100% và không xóa hẳn ảo giác.

Score fusion, thí nghiệm ở phần sau Phase 1, không phải điều kiện bảo vệ đồ án:

`score = alpha * kg_score + (1 - alpha) * cosine`

Alpha không được kéo vào câu trả lời một node không nằm trong tập đã truy.

Cắt đoạn theo nghĩa: câu kề nhau có cosine lớn hơn 0.85 thì gộp vào cùng một đoạn. Threshold này là giả thuyết trong note, phải đo lại, không hard-code như chân lý.

## Tầng 3 — PostgreSQL

Vai trò: master registry và nguồn chân lý của mã. Sequence cấp `entity_id`. Bước khử trùng lặp danh xưng tra bảng danh xưng tại đây trước khi nạp Neo4j. Khi dựng lại graph hoặc đổi embedding, dữ liệu được tái tạo từ các bảng này.

Bảng cốt lõi trong đồ án:

| Bảng | Cột chính |
| --- | --- |
| dim_entities | entity_id, entity_type, canonical_name, wikidata_id, verification_status, confidence_score |
| entity_aliases | alias_id, entity_id, alias_name, alias_type, source_citation; chỉ mục tên và pg_trgm |
| source_documents | source_id, title, author_compiler, compilation_era, source_perspective, storage_path |
| raw_documents | doc_id, source_id, text, checksum |
| extraction_runs | run_id, doc_id, model_name, created_at, json_path |
| ingest_logs | run_id, status, message |

`verification_status` nhận `DRAFT`, `VERIFIED`, `FLAGGED`.

Bảng Phase 2, tạo sau: `users`, `learning_logs`.

## Tầng 4 — agent

Không triển khai trong đồ án. Xem `04-tac-tu`. Đồ án chỉ cần FastAPI với các endpoint dữ liệu, chưa có ToolPlanner.

## Stack ghi trong proposal đồ án

- Python 3.12, FastAPI, Pydantic
- Neo4j 5.x, ChromaDB, PostgreSQL 16
- LLM: Llama-3-Vietnamese, Qwen2.5 hoặc API OpenAI, kèm JSON schema
- Sentence transformers tiếng Việt cho embedding
- Docker, Git, Postman, Streamlit cho demo nội bộ

## API đồ án

| Method | Endpoint | Việc |
| --- | --- | --- |
| POST | `/extract-5w1h` | Văn bản thô vào, JSON gồm bản ghi chủ thể và quan hệ ra |
| POST | `/resolve-entity` | Chuỗi danh xưng vào, mã đã có trong master registry, hoặc trạng thái `FLAGGED` |
| POST | `/ingest-graph` | JSON đã khử trùng lặp danh xưng, nạp vào Neo4j |
| GET | `/entities/{entity_id}` | Một chủ thể và các edge một bước, để demo |

Swagger là sản phẩm đóng gói. Tháng 2 của đồ án có API khung. Tháng 4 API phải chạy được ba bước demo.
