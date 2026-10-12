## 3. PHƯƠNG PHÁP ĐỀ XUẤT

**Cách tiếp cận:** Backend tên làm việc HistoryDistill, một ứng dụng monolith. Luồng xử lý đi theo thứ tự sau.

- Bước 1. Người vận hành import một file các đoạn sử liệu.
- Bước 2. Hệ thống trả về một file JSON gồm hai danh sách đúng schema: bản ghi chủ thể mà đoạn nói tới, và các quan hệ giữa chúng. Mỗi từ khóa có giá trị và mỗi quan hệ phải kèm đoạn trích cùng vị trí ký tự. Sai schema thì bị từ chối.
- Bước 3. PostgreSQL cấp mã mờ cho từng bản ghi.
- Bước 4. Bản ghi Person, Group và Place đi qua khử trùng lặp danh xưng. Hệ thống tra bảng danh xưng trên PostgreSQL bằng chỉ mục trigram.
- Bước 5. Chưa khớp chắc thì đo string similarity, threshold khởi điểm khoảng 80% và được tinh chỉnh trên dev set, rồi so embedding có ngữ cảnh. Dưới threshold thì gắn FLAGGED, không tự tạo node mới.
- Bước 6. Kết quả nạp Neo4j bằng MERGE theo mã đã cấp. Cùng mã thì cập nhật, không nhân đôi.
- Bước 7. Demo chỉ cần cho thấy một danh xưng đã có trong master registry đi vào đúng mã cũ.

**Dữ liệu và công nghệ:** Kho thí điểm là các sử liệu đã được gắn nhãn về một sự kiện lịch sử, lấy từ nhiều nguồn. Gold set do người gắn nhãn chủ thể, từ khóa và quan hệ, không nhìn kết quả mô hình. Gold set được tách thành dev set và test set. Threshold và prompt chỉ tinh chỉnh trên dev set. Test set chỉ dùng một lần để ra số đưa vào báo cáo.

Công nghệ dùng trong đồ án:

- Python, FastAPI, Pydantic.
- Neo4j, PostgreSQL, ChromaDB.
- LLM có structured output.
- Embedding tiếng Việt (PhoBERT hoặc tương đương), chỉ để xếp hạng danh xưng.
- Streamlit, Docker Compose, Git.

**Kế hoạch đánh giá:** Các con số dưới đây là mục tiêu đặt ra, chưa phải kết quả đã đo.

| Chỉ số | Cách tính | Đích |
| --- | --- | --- |
| Độ khớp F1 theo từ khóa | So từng từ khóa của từng bản ghi chủ thể với gold set; giá trị phải kèm đoạn trích đúng; báo riêng từng chủ thể | 85% đến 90% |
| Độ khớp F1 theo quan hệ | Đúng mã đầu, loại quan hệ, mã cuối và có đoạn trích | 75% đến 85% |
| Precision của bước khử trùng lặp danh xưng | Chỉ tính các ca hệ thống tự quyết | 90% đến 95% |
| Thời gian trích xuất | Từ khi nhận chữ đến khi có kết quả đúng schema | Dưới 3 đến 5 giây mỗi trang |

Độ khớp F1 theo từ khóa tính trên từng từ khóa có giá trị.

- Khớp khi cùng chủ thể, cùng từ khóa, cùng giá trị với gold set, và có đúng đoạn trích.
- Hệ thống đưa giá trị gold set không có, hoặc có giá trị nhưng không có đoạn trích đúng, thì tính là thừa.
- Gold set có giá trị mà hệ thống bỏ sót hoặc để null thì tính là thiếu.
- Cả hai bên đều để null thì không tính là lỗi.
- Báo riêng từng chủ thể, không gộp một số trung bình.

Độ khớp F1 theo quan hệ chỉ khớp khi đủ bốn điều kiện: đúng mã đầu, đúng loại quan hệ, đúng mã cuối, và có đoạn trích.

Precision của bước khử trùng lặp danh xưng chỉ tính ca hệ thống tự gắn một danh xưng vào một mã đã có. Ca FLAGGED không đưa vào mẫu số. Gắn đúng mã thì tính đúng. Gắn vào mã của một chủ thể khác thì tính sai.

Thời gian trích xuất tính từ lúc nhận đoạn chữ đến lúc có JSON đúng schema, lấy trung bình trên test set.

Bản ghi thiếu đoạn trích ở trạng thái DRAFT, không được tính là khớp. Nếu một chỉ số thấp hơn đích, báo cáo vẫn hợp lệ khi có bảng lỗi theo chủ thể và theo loại quan hệ.
