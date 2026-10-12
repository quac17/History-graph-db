# KPI và sản phẩm bàn giao

Người thực hiện: Trần Việt Hoàng. MSSV: 25MSA13219.

Chỉ số của đồ án là chỉ số mang ra hội đồng. Chỉ số của dự án là đích của cả dự án, không phải điều kiện tốt nghiệp.

## Đồ án

| Chỉ số | Cách đo | Mốc trong proposal đồ án |
| --- | --- | --- |
| Độ khớp F1 theo từ khóa | Gold set khoảng 150–200 đoạn sử liệu, nhãn do người gắn. So từng từ khóa của từng bản ghi chủ thể, báo riêng từng chủ thể | 85% đến 90% |
| Độ khớp F1 theo quan hệ | Cùng gold set. Một quan hệ khớp khi đúng mã đầu, loại edge, mã cuối và có đoạn trích | 75% đến 85% |
| Precision khử trùng lặp danh xưng | Alias hệ thống tự gán so với danh sách đúng | 90% đến 95% |
| Thời gian trích xuất | Từ đoạn chữ tới JSON hợp lệ | Dưới 3 đến 5 giây mỗi trang |

Gold set không được sinh bởi chính mô hình rồi tự chấm.

## Phương pháp đo của đồ án

Các con số trong bảng là đích đặt ra, chưa phải kết quả đã đo. Đồ án chưa chạy thử trên test set nên chưa có bảng kết quả.

Gold set khoảng 150 đến 200 đoạn sử liệu tiếng Việt. Người gắn nhãn đọc đoạn chữ và ghi ba thứ: chủ thể có trong đoạn, từ khóa có giá trị, và quan hệ giữa các chủ thể. Người gắn nhãn không nhìn kết quả của mô hình. Tập này tách thành dev set và test set. Threshold, prompt và các lựa chọn khác chỉ tinh chỉnh trên dev set. Test set chỉ dùng một lần để ra số đưa vào báo cáo.

Độ khớp F1 theo từ khóa tính trên từng từ khóa có giá trị của từng bản ghi chủ thể.

- Khớp khi cùng chủ thể, cùng từ khóa, cùng giá trị với gold set, và có đúng đoạn trích trong nguồn.
- Hệ thống đưa một giá trị gold set không có, hoặc có giá trị nhưng không có đoạn trích đúng, thì tính là thừa.
- Gold set có giá trị mà hệ thống bỏ sót hoặc để null thì tính là thiếu.
- Cả gold set và hệ thống đều để null thì không tính là lỗi.
- Báo riêng từng chủ thể. Không gộp một số trung bình để che chủ thể yếu.

Độ khớp F1 theo quan hệ thấp hơn vì một quan hệ chỉ khớp khi đủ bốn điều kiện: đúng mã đầu, đúng loại quan hệ, đúng mã cuối, và có đoạn trích. Thiếu một điều kiện là không khớp. Đích vì vậy để ở 75% đến 85%.

Precision của bước khử trùng lặp danh xưng chỉ tính các ca hệ thống tự quyết, tức tự gắn một danh xưng vào một mã đã có. Ca FLAGGED không đưa vào mẫu số, vì hệ thống đã không tự gộp. Gắn đúng mã thì tính đúng. Gắn vào mã của một người khác thì tính sai.

Thời gian trích xuất tính từ lúc nhận đoạn chữ đến lúc có JSON đúng schema. Đo trên các đoạn của test set và báo thời gian trung bình mỗi trang. Đích là dưới 3 đến 5 giây mỗi trang.

Nếu một chỉ số thấp hơn đích, báo cáo vẫn hợp lệ khi có bảng lỗi theo chủ thể và theo loại quan hệ. Bảng đó nói rõ hệ thống bỏ sót gì và trích thêm gì.

Sản phẩm:

1. Source code Python, FastAPI, Docker.
2. Neo4j đã nạp cụm Bạch Đằng và các đoạn thí điểm.
3. PostgreSQL giữ nguồn và log nạp.
4. Streamlit: dán chữ, xem bản ghi chủ thể và quan hệ, nạp graph, thấy node trùng bị gộp.
5. Báo cáo độ khớp F1 theo từ khóa, theo quan hệ, và precision.
6. OpenAPI của `/extract-5w1h`, `/resolve-entity`, `/ingest-graph`, `/entities/{entity_id}`.

Chưa bàn giao: chatbot, ToolPlanner, học liệu cho cả chương trình, khảo sát lớp học.

## Hết Phase 1, thêm

| Chỉ số | Mốc trong proposal dự án |
| --- | --- |
| Độ khớp F1 trích xuất | Từ 90% |
| Precision khử trùng lặp danh xưng | Từ 95% |
| Độ trễ hybrid search | Dưới 1,5 đến 2 giây |
| Provenance trên bản ghi dị bản | Proposal ghi 100% bản ghi dị bản phải có nguồn. Đọc là mọi assertion đưa vào demo đều có source_id, không phải mọi câu trong chính sử |

## Phase 2

| Chỉ số | Mốc ghi trong proposal dự án |
| --- | --- |
| Câu trả lời truy được về node hoặc đoạn văn | Proposal ghi từ 98% |
| Giữ đúng biên thời gian và địa điểm | Proposal ghi từ 92% |
| Khảo sát giáo viên và học sinh | Proposal ghi từ 85% đánh giá tích cực |

Ba mốc Phase 2 chỉ có nghĩa sau khi có tập câu hỏi và phiếu khảo sát. Đừng đưa vào slide đồ án như việc đồ án đã hứa.

## Cách đọc "đúng 100%"

Các bản proposal có chỗ viết graph đúng hoàn toàn hoặc hết ảo giác. Khi làm việc và khi viết báo cáo, dùng cách đo được: một từ khóa hoặc một quan hệ được tính đúng nếu khớp nhãn trong gold set và có đoạn nguồn; một câu trả lời Phase 2 được tính bám nguồn nếu mọi thực thể nó nêu đều nằm trong tập node đã truy. Lỗi trích xuất vẫn đi vào graph nếu bỏ qua trạng thái `draft`.
