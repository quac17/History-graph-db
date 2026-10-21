# HistoricalKnowledgeDatabase

Mã nguồn database của đồ án. PostgreSQL là master registry: cấp mã mờ, giữ danh xưng, nguồn và log. Neo4j giữ node và edge bằng đúng mã đó.

Bốn tầng của hệ thống:

- Neo4j: graph tám chủ thể. Container có trong `docker-compose.yml`.
- ChromaDB: đoạn văn và embedding. Chưa chạy ở bước này.
- PostgreSQL: master registry và các bảng danh mục. Container có trong `docker-compose.yml`.
- Agent: lớp hỏi đáp. Thuộc Phase 2, chưa có trong thư mục này.

## Chuẩn bị

Cần Docker và Python. Chạy ở thư mục gốc của repo.

- `yarn setup`: tạo `.env` từ `.env.example` nếu chưa có, cài `requirements.txt` và kiểm tra `docker compose`. Không bật container, không xóa `.env` đang có. Không commit `.env`.

## Lệnh

- `yarn init_db`: bật lại container PostgreSQL và Neo4j. Không xóa volume.
- `yarn generated_db`: tạo bảng, sequence, chỉ mục và ràng buộc Neo4j nếu chưa có. Không xóa dữ liệu.
- `yarn reset_db`: xóa dữ liệu, tạo lại schema, nạp danh mục niên hiệu, can chi và đơn vị đo. Không nạp seed sử liệu.
- `yarn seed_db`: nạp cụm mẫu Bạch Đằng vào PostgreSQL rồi MERGE sang Neo4j. Chạy lại không nhân đôi.
- `yarn dump_db`: ghi `dumps/postgres-*.sql` và `dumps/neo4j-*.cypher`.

Máy mới: `yarn setup`, rồi `yarn init_db`, đợi container healthy, `yarn generated_db`, `yarn reset_db`, `yarn seed_db`.

## Seed

Tám mã mẫu: `P00001`, `GRP0001`, `EV00001`, `LOC0001`, `TIM0001`, `CON0001`, `ART0001`, `SRC0001`. Quan hệ: `COMMANDED`, `OPPOSED_IN`, `TOOK_PLACE_AT`, `OCCURRED_DURING`, `EMPLOYED_STRATEGY`, `SUPPORTS`. Câu trong `data/seed.json` là câu minh họa để thử schema, không phải đoạn trích nguyên văn từ chính sử. Năm 1288 nằm ở thuộc tính của `TIM0001`, không nằm trong mã.
