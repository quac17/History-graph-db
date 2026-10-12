## 2. TỔNG QUAN NGHIÊN CỨU

**Vấn đề và động cơ:** Chương trình môn Lịch sử 2018 yêu cầu người học nêu sự kiện có thời gian và địa điểm, chỉ ra tư liệu, và nối nguyên nhân với diễn biến. Trên lớp, phiếu 5W1H nằm lại trong vở, không dùng lại và không đo được độ bám nguồn. Thư viện số tìm được cuốn sách nhưng không trả lời được câu bên trong tệp, ví dụ ai có mặt ở trận Bạch Đằng 1288. LLM trả lời trôi chảy nhưng có thể thêm năm hoặc người không có trong nguồn. Một nhân vật có nhiều tên gọi nên kho dễ bị nhân đôi. Đồ án làm một pipeline đo được: từ văn bản sử tiếng Việt, qua bản ghi chủ thể và quan hệ có đoạn trích, tới knowledge graph, với gold set do người gắn nhãn.

**Mục tiêu và câu hỏi nghiên cứu:** Mục tiêu chung là xây và đo một pipeline, trong đó sử liệu tiếng Việt đã có chữ được trích xuất thành bản ghi chủ thể và quan hệ, danh xưng của cùng một người được gộp về một node, và kết quả được nạp vào knowledge graph.

- O1. Chốt schema của hệ thống chủ thể và từ khóa (tám chủ thể cố định, bộ từ khóa, mã định danh mờ do PostgreSQL cấp, danh mục phân loại, kiểu quan hệ) và dựng ba database chạy bằng Docker.
- O2. Dựng bốn API, pipeline trích xuất–khử trùng lặp danh xưng–nạp graph, và giao diện demo cho người vận hành.
- O3. Lập gold set khoảng 150 đến 200 đoạn sử liệu do người gắn nhãn, rồi đo độ khớp F1 và precision trên test set.

Câu hỏi nghiên cứu:

- RQ1. Cách quản lý sử liệu và trích xuất sự kiện hiện nay thuận lợi và vướng ở đâu với tiếng Việt và môn Lịch sử phổ thông?
- RQ2. Trong phạm vi đồ án, cách nào vừa sức để trích xuất bản ghi chủ thể và quan hệ, khử trùng lặp danh xưng và nạp vào graph?
- RQ3. Đo chất lượng trích xuất và chất lượng khử trùng lặp danh xưng bằng cách nào?

**Tính mới và đóng góp:** Đồ án đóng góp một cách lưu trữ theo chủ thể, và một pipeline trích xuất bám nguồn.

Cách lưu trữ:

- Lưu theo từng chủ thể thay vì lưu theo từng file sách.
- Một chủ thể chỉ có một định danh trong database. Nhiều tên gọi vẫn là một chủ thể.
- Nếu nhiều đoạn sử liệu khác nhau cùng gắn vào chủ thể. Mỗi đoạn vẫn được giữ nguyên vẹn cùng với nguồn của mình thay vì gộp nội dung.

Pipeline trích xuất:

- Chỉ lưu trữ thông tin nguồn có viết, và lưu kèm câu gốc.
- Xác định các đoạn sử liệu cùng chủ thể và gộp về chung một định danh.
- Hai nguồn không bị trộn thành một câu. Tránh việc gây ra ảo giác AI.

**Phạm vi và giới hạn:**

Nằm trong đồ án:

- Nhận đầu vào là văn bản tiếng Việt.
- Kho thí điểm là các sử liệu dựa trên một sự kiện lịch sử được lấy từ nhiều nguồn.
- Tám chủ thể đã chốt: Person, Group, Event, Place, TimeSpan, Artifact, Concept, Source, cùng các quan hệ giữa chúng.
- Neo4j có dữ liệu demo. PostgreSQL là master registry: cấp mã mờ, giữ danh xưng, nguồn và log. ChromaDB dựng schema và vài bản ghi mẫu.
- Bốn endpoint: `/extract-5w1h`, `/resolve-entity`, `/ingest-graph`, `/entities/{entity_id}`, và demo Streamlit.

Không nằm trong đồ án, để dành cho phần sau:

- Chatbot cho học sinh, ToolPlanner và thử trên lớp.
- Cắt đoạn và embedding hàng loạt.
- Ghi dị bản giữa hai nguồn.
- OCR.

Cách ghi kết quả trong đồ án:

- Từ khóa hoặc quan hệ thiếu đoạn trích ở trạng thái DRAFT, không được trình như đã kiểm.
- Ca chưa đủ chắc để tự gộp danh xưng thì FLAGGED.
