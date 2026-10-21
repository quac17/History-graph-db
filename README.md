# History-graph-db

## Lệnh tạo tài liệu

Cần Python, `python-docx`, `python-pptx` và Yarn. Chạy ở thư mục gốc. Đóng file Word hoặc PowerPoint đang mở trước khi chạy, nếu không lệnh ghi đè sẽ bị từ chối.

- `yarn gen_slide`: dựng `Do An/slide-bao-cao-proposal.pptx` từ `Do An/khung-slide-bao-cao-proposal.md`.
- `yarn gen_proposal`: xuất sáu mục đề cương rồi ghép `thesis-proposal.vi.docx` và `thesis-proposal.en.docx`.
- `yarn gen_proposal_vi` và `yarn gen_proposal_en`: cùng quy trình, chỉ một ngôn ngữ.
- `yarn gen_all`: chạy `gen_proposal` rồi `gen_slide`.

## Lệnh database

Cần Docker. ChromaDB chưa được bật.

- `yarn setup`: tạo `.env` nếu chưa có, cài thư viện Python và kiểm tra Docker. Không bật database.
- `yarn init_db`: bật PostgreSQL và Neo4j.
- `yarn generated_db`: tạo schema.
- `yarn reset_db`: xóa dữ liệu, tạo lại schema và nạp danh mục.
- `yarn seed_db`: nạp cụm sử liệu mẫu.
- `yarn dump_db`: ghi file dump vào `Do An/HistoricalKnowledgeDatabase/dumps/`.