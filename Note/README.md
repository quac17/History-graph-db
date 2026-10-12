# Note — bản đồ thư mục

Tên đề tài: Triển khai hệ thống CSDL đồ thị tri thức và thiết kế pipeline trích xuất mạng lưới thực thể lịch sử 5W1H bằng LLM.

Người thực hiện: Trần Việt Hoàng. MSSV: 25MSA13219. Giảng viên hướng dẫn: TS Bùi Trung Hiếu.

Các file Word cũ nằm ở `_ban-cu/`. Bản này sắp lại theo chức năng, bám hai proposal đang dùng:

- Dự án: `Project tong/master-proposal-18-thang.docx`
- Đồ án, phần mở đầu Phase 1 của dự án: `Do An/proposal/proposal.md`, bản kỹ thuật `Do An/capstone-proposal-q1-q2-chi-tiet.docx`

Trong note, "đồ án" chỉ phần bảo vệ tốt nghiệp, "dự án" chỉ toàn bộ dự án. Thời lượng của từng phần chỉ ghi ở `05-lo-trinh`.

Thuật ngữ IT thông dụng giữ tiếng Anh: pipeline, knowledge graph, graph, node, edge, schema, database, vector database, embedding, semantic search, hybrid search, LLM, API, endpoint, demo, gold set, threshold, batch, log, DRAFT, VERIFIED, FLAGGED, agent, scaffolding. Ba từ dùng tiếng Việt: khử trùng lặp danh xưng (loại bỏ trùng lặp danh xưng), cắt đoạn và đoạn văn, độ khớp F1. "Trích xuất" thay cho "chưng cất".

Bản 24 tháng trong `Project tong/de-xuat-de-tai-hoan-chinh demo1.docx` được ghi ở mục phụ của lộ trình, không phải lịch đang chạy. Hai chương đầu đã viết nằm ở `Project tong/Capstone_Proposal_Chuong1-2_LichSu_KG.docx`. Mô tả bốn tầng gốc nằm ở `Project tong/mo-ta-4-tang-he-thong-csdl-tich-hop.docx`.

Hai file gốc về hệ thống chủ thể và từ khóa nằm ngay trong `Note/`:

- `danh-muc-tu-khoa-chu-the-lich-su-v2.docx`: mã định danh, danh mục phân loại đóng, thuộc tính từng chủ thể.
- `he-thong-chu-the-va-mang-luoi-quan-he-lich-su.docx`: mô tả bằng lời thường, quan hệ, ràng buộc, ví dụ Bạch Đằng.

Bản tóm tắt để code là `01-bai-toan/he-thong-chu-the-va-tu-khoa.md`. Tám chủ thể đã cố định. Bộ từ khóa của từng chủ thể có thể thay đổi, nên các note không ghi số lượng từ khóa.

Mỗi thư mục có một file `.md` để đọc khi code và một file `.docx` cùng nội dung.

| Thư mục | Việc của nó | Làm trong đồ án? |
| --- | --- | --- |
| `01-bai-toan` | Bài toán, 5W1H, hệ thống chủ thể và từ khóa | Có, đây là schema phải chốt |
| `02-kien-truc` | Bốn tầng database, liên kết graph với vector, mở rộng môn khác | Dựng Neo4j, ChromaDB, PostgreSQL. Liên kết đoạn văn với node để phần sau của Phase 1 |
| `03-pipeline` | Trích xuất, khử trùng lặp danh xưng, cắt đoạn, dị bản | Đồ án làm trích xuất, nạp graph, khử trùng lặp danh xưng. Cắt đoạn và dị bản để sau |
| `04-tac-tu` | Agent hỏi đáp và Phase 2 | Không làm chatbot trong đồ án. Giữ để khỏi lệch phạm vi |
| `05-lo-trinh` | Lộ trình dự án, lộ trình đồ án, phương án 24 tháng | Bám mục đồ án |
| `06-danh-gia` | KPI và sản phẩm bàn giao | KPI đồ án, không lấy KPI dự án làm điều kiện bảo vệ |

Mã định danh mờ do PostgreSQL cấp, theo `thiet-ke-dinh-danh.md`. Ví dụ minh họa `P00001`, `EV00001`, `LOC0001`. Không ghép tên hay năm vào mã. Mã kiểu `NODE_P_001` và mã ghép tên với mốc thời gian không dùng nữa.

Graph là mỏ neo: câu trả lời sau này chỉ được dùng node và đoạn văn đã có nguồn. Đồ án chưa sinh câu trả lời cho học sinh. Đồ án chứng minh văn bản thô thành bản ghi chủ thể và quan hệ, rồi thành node và edge trên Neo4j, có khử trùng lặp danh xưng.
