## 6. LỘ TRÌNH THỰC HIỆN 12 TUẦN (3 THÁNG)

| Tuần | Giai đoạn | Việc dự kiến | Cột mốc / sản phẩm tuần |
| --- | --- | --- | --- |
| Tuần 1 | Chuẩn bị | Chốt đề cương, dựng Git, đọc tài liệu nền, phác hệ thống chủ thể và từ khóa | Repo chạy được, đề cương gửi giảng viên |
| Tuần 2 | Thiết kế | Schema tám chủ thể, mã định danh mờ, danh mục phân loại, kiểu quan hệ, các bảng master registry trên PostgreSQL | Sơ đồ kiến trúc và schema Pydantic bản nháp |
| Tuần 3 | Baseline | Docker Compose cho Neo4j, PostgreSQL, ChromaDB; nạp một bản ghi mẫu theo schema | Ba database chạy; sequence cấp được mã; bản ghi mẫu trên Neo4j |
| Tuần 4 | Phát triển lõi | API `/extract-5w1h`; bắt đầu gắn nhãn gold set | Endpoint trích xuất gọi được |
| Tuần 5 | Phát triển lõi | `/resolve-entity`, `/ingest-graph`, `/entities/{entity_id}`; tiếp tục gắn nhãn | Bốn endpoint gọi được; tài liệu API bản nháp |
| Tuần 6 | Giữa kỳ | Khóa schema và danh mục ở mức đủ demo; rà gold set; họp giữa kỳ với giảng viên | Báo cáo giữa kỳ; schema đóng để đo |
| Tuần 7 | Tích hợp | Pipeline trích xuất rồi nạp graph bằng MERGE; kiểm ràng buộc nguồn và niên đại | Một đoạn thành node và edge; nạp lại không nhân đôi |
| Tuần 8 | Tối ưu | Khử trùng lặp danh xưng tự động trên master registry; siết DRAFT và FLAGGED | Danh xưng đã có trong master registry trỏ đúng mã cũ, không sinh node thứ hai |
| Tuần 9 | Đánh giá | Demo Streamlit; đo độ khớp F1 và precision trên test set | Bảng số đo; demo ba bước chạy |
| Tuần 10 | Viết luận văn | Soạn chương 1, 2 và 3 theo khung thesis | Bản thảo nửa đầu luận văn |
| Tuần 11 | Viết luận văn | Soạn chương 4, 5 và 6; định dạng theo template | Bản thảo đầy đủ gửi giảng viên |
| Tuần 12 | Hoàn thiện | Sửa theo góp ý, hoàn thiện slide, chạy thử bảo vệ | Nộp luận văn và slide |
