## 5. NGUỒN LỰC VÀ QUẢN LÝ RỦI RO

**Nguồn lực cần có:** Máy cá nhân đủ RAM để Neo4j và PostgreSQL chạy cùng lúc. Ba database chạy bằng Docker Compose, không cần máy chủ riêng. LLM gọi qua API; khóa API không đưa vào repository. Bước so danh xưng dùng embedding nhỏ, không bắt buộc GPU. Văn bản test lấy từ sách giáo khoa và đoạn sử liệu được phép dùng, không mua dữ liệu độc quyền.

**Rủi ro và cách xử lý:**

- R1. Mô hình bỏ sót thực thể hoặc trích thêm điều không có trong chữ. Cách xử lý: từ chối kết quả sai schema; thiếu đoạn trích thì DRAFT.
- R2. Gộp nhầm hai người thành một. Cách xử lý: tinh chỉnh threshold trên dev set; dưới threshold thì FLAGGED, không tự tạo node mới.
- R3. Phạm vi phình sang chatbot. Cách xử lý: demo chỉ có ba bước, không có ô chat.
- R4. Đổi mô hình giữa chừng khiến số đo không so được. Cách xử lý: mỗi lần chạy ghi tên mô hình vào log; báo cáo cuối chỉ dùng một cấu hình.
