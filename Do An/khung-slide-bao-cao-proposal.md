# Khung slide báo cáo proposal

Bản nháp để duyệt nội dung trước khi dựng slide. Duyệt xong mới tạo file `.pptx`.

- Đề tài: Khung tích hợp CSDL lai và Pipeline LLM trong mô hình hóa tri thức lịch sử Việt Nam theo phương pháp 5W1H
- Người thực hiện: Trần Việt Hoàng, MSSV 25MSA13219
- Giảng viên hướng dẫn: TS Bùi Trung Hiếu
- Số slide: 21, khoảng 15 đến 20 phút trình bày
- Nguồn nội dung: `Do An/thesis-proposal/`, `Do An/mo-ta-do-an.md`, `Note/thiet-ke-dinh-danh.md`

Quy ước thuật ngữ: "dự án" là toàn bộ dự án; "đồ án" là phần bảo vệ tốt nghiệp. Số tháng chỉ xuất hiện ở slide 5 (lộ trình dự án). Các slide khác gọi theo giai đoạn hoặc theo tuần của đồ án.

Bố cục:

| Phần | Slide | Nội dung |
| --- | --- | --- |
| Mở đầu | 1 | Bìa |
| A. Dự án | 2–5 | Bối cảnh, vấn đề, ý tưởng, lộ trình |
| B. Đồ án | 6–12 | Phạm vi, bài toán, cơ sở KHXH, thực trạng, câu hỏi nghiên cứu, tính mới, mục tiêu |
| C. Giải pháp | 13–17 | Hệ thống chủ thể và từ khóa, ví dụ kết quả trích xuất, mạng lưới quan hệ, luồng xử lý, kiến trúc |
| D. Kế hoạch và đánh giá | 18–20 | Kế hoạch và rủi ro, đánh giá, demo và bàn giao |
| Kết | 21 | Tóm tắt và hỏi đáp |

---

## Slide 1. Bìa

Nội dung:

- Trường Đại học FPT · Thesis Proposal
- Khung tích hợp CSDL lai và Pipeline LLM trong mô hình hóa tri thức lịch sử Việt Nam theo phương pháp 5W1H
- An Integrated Framework Combining Hybrid Databases and LLM Pipelines for 5W1H Vietnamese Historical Knowledge Modeling
- Người thực hiện: Trần Việt Hoàng · MSSV 25MSA13219
- Giảng viên hướng dẫn: TS Bùi Trung Hiếu
- Hà Nội, 2026

Gợi ý trình bày: tên tiếng Việt to nhất, tên tiếng Anh nhỏ hơn và in nghiêng. Nền có thể dùng hình mờ sông Bạch Đằng hoặc bãi cọc.

---

# Phần A. Dự án

## Slide 2. Bối cảnh: môn Lịch sử đang đòi hỏi gì

Nội dung:

- Chương trình giáo dục phổ thông môn Lịch sử 2018 (Thông tư 32/2018/TT-BGDĐT) đặt ba năng lực: tìm hiểu lịch sử, nhận thức và tư duy lịch sử, vận dụng.
- Người học phải nêu sự kiện có thời gian và địa điểm, chỉ ra tư liệu mình dựa vào, và giải thích quan hệ giữa nguyên nhân và diễn biến.
- Trên lớp, giáo viên vẫn dùng cách hỏi 5W1H qua phiếu học tập và sơ đồ.

Gợi ý trình bày: ba ô năng lực xếp ngang. Bên dưới là một phiếu 5W1H trên giấy, minh họa cách đang làm.

Lời nói: dự án bắt đầu từ yêu cầu của môn học, không bắt đầu từ công nghệ.

## Slide 3. Vấn đề: tri thức sử chưa có chỗ để hỏi và kiểm

Nội dung:

- Bài giảng lịch sử nằm lại trong vở, khó dùng lại, không đo được độ bám nguồn.
- Thư viện số tìm được cuốn sách, nhưng không trả lời được "ai có mặt ở trận Bạch Đằng 1288".
- Chatbot trả lời trôi chảy nhưng có thể thêm năm, thêm người không có trong nguồn.
- Một nhân vật có nhiều tên gọi: Trần Quốc Tuấn, Hưng Đạo Vương, Hưng Đạo Đại Vương.
- Hai bộ sử có thể kể khác nhau về cùng một trận.
- Thực tiễn cần một hệ thống giải quyết các vấn đề này.

Gợi ý trình bày: năm điểm nghẽn, mỗi điểm một biểu tượng. Có thể đặt một câu chatbot trả lời sai niên đại cạnh câu trích đúng trong sách.

## Slide 4. Ý tưởng dự án

Nội dung:

- Dựng một kho sử liệu mà mỗi sự kiện đều nối được về câu gốc trong nguồn.
- Sự kiện, nhân vật, địa danh, thời gian và nguồn được nối thành một mạng lưới thực thể.
- Trên kho đó, người học đặt câu hỏi và nhận câu trả lời có dẫn nguồn.
- Hệ thống gợi ý ba thao tác của sử học: kiểm nguồn, đặt sự kiện vào đúng thời gian và địa điểm, đối chiếu hai nguồn.
- Máy làm phần thư ký. Không thay giáo viên, không trả lời hộ học sinh.

Gợi ý trình bày: sơ đồ ba tầng từ dưới lên. Tầng dưới là nguồn sử liệu, tầng giữa là mạng lưới thực thể, tầng trên là người học hỏi và kiểm nguồn.

## Slide 5. Lộ trình dự án và vị trí của đồ án

Nội dung:

| Giai đoạn | Thời gian | Việc chính | Đồ án |
| --- | --- | --- | --- |
| Phase 1, phần đồ án | 12 tuần | Schema, mã mờ, master registry, trích xuất, khử trùng lặp danh xưng | Có |
| Phase 1, phần sau | Sau đồ án | Cắt đoạn, embedding hàng loạt, liên kết đoạn văn với node, giữ hai nguồn lệch nhau | Không |
| Phase 2 | Sau Phase 1 | Agent hỏi đáp, lọc thời gian và địa điểm, scaffolding học tập, thử trên lớp | Không |

- Dự án dài 18 tháng. Đồ án là 12 tuần mở đầu Phase 1, theo đề cương.
- PostgreSQL là master registry: cấp mã mờ, giữ danh xưng, nguồn và log.

Gợi ý trình bày: một thanh thời gian ngang, tô đậm đoạn 12 tuần và ghi "Đồ án". Đây là slide duy nhất ghi số tháng của dự án.

---

# Phần B. Đồ án

## Slide 6. Phạm vi đồ án

Nội dung:

Làm trong đồ án:

- Nhận đầu vào là văn bản sử liệu tiếng Việt.
- Mã định danh mờ do PostgreSQL cấp, giữ trong master registry.
- Trích xuất bản ghi chủ thể và quan hệ theo hệ thống chủ thể và từ khóa, khử trùng lặp danh xưng, nạp vào knowledge graph.
- Kho thí điểm: sử liệu đã gắn nhãn về một sự kiện lịch sử, lấy từ nhiều nguồn.
- Bốn API: `/extract-5w1h`, `/resolve-entity`, `/ingest-graph`, `/entities/{entity_id}`.
- Giao diện demo cho người vận hành.

Không làm trong đồ án:

- Chatbot cho học sinh, ToolPlanner, thử trên lớp.
- Cắt đoạn và embedding hàng loạt.
- Ghi dị bản giữa hai nguồn.
- Nhận dạng chữ từ ảnh (OCR).

Gợi ý trình bày: hai cột, bên trái dấu tích, bên phải dấu gạch.

Lời nói: sản phẩm của đồ án là một mạng lưới thực thể đo được, chưa phải chatbot.

## Slide 7. Bài toán của đồ án

Nội dung:

- Đầu vào: một đoạn sử liệu tiếng Việt.
- Đầu ra: các bản ghi chủ thể mà đoạn chữ có nói tới (người, tổ chức, sự kiện, nơi, thời gian, hiện vật, kế sách, nguồn), mỗi bản ghi mang mã và các từ khóa có giá trị, cùng các quan hệ giữa chúng.
- Mỗi từ khóa có giá trị và mỗi quan hệ đều kèm đoạn trích nguồn.
- Danh xưng đã có trong master registry thì gắn vào đúng mã cũ, không sinh node thứ hai.
- Kết quả hợp lệ được nạp vào knowledge graph. Thiếu đoạn trích thì DRAFT. Chưa đủ chắc để tự gộp thì FLAGGED.

Gợi ý trình bày: luồng ngang "đoạn chữ → bản ghi chủ thể và quan hệ → knowledge graph". Đoạn trích tô màu, nối bằng mũi tên tới từ khóa hoặc quan hệ tương ứng.

## Slide 8. Cơ sở khoa học xã hội

Nội dung:

- Tư duy lịch sử (van Drie và van Boxtel): đặt câu hỏi, dùng nguồn, đặt vào bối cảnh, lập luận, dùng khái niệm của ngành.
- Học tập bằng tìm tòi trong môn Sử: người học làm việc với tư liệu, không nhận một bài kể đã viết sẵn.
- 5W1H là cách hỏi quen trên lớp. Mỗi câu hỏi trỏ tới một loại thực thể, nên đồ án chuyển 5W1H thành tám chủ thể có từ khóa.
- Sử học làm việc với lời kể có nguồn. Đơn vị dữ liệu của đồ án là thực thể và quan hệ kèm đoạn trích.
- Câu hỏi "vì sao" thường là lời giải thích của người viết sử. Đồ án chỉ ghi hệ quả khi nguồn có viết.

Gợi ý trình bày: bên trái là sáu câu hỏi 5W1H, bên phải là tám chủ thể. Mũi tên nối từng câu hỏi với chủ thể tương ứng.

## Slide 9. Thực trạng tại Việt Nam

Nội dung:

| Tiêu chí | Phiếu trên lớp | Thư viện số | Knowledge graph từ sách giáo khoa | Đồ án |
| --- | --- | --- | --- | --- |
| Đơn vị ghi | Bảng học sinh điền | Tệp, thông tin bìa | Node theo bài | Tám chủ thể có từ khóa, nối bằng quan hệ |
| Nhiều tên một người | Giáo viên tự hiểu | Không xử lý | Tùy cách làm | Có khử trùng lặp danh xưng, có cờ FLAGGED |
| Đo được | Không | Không sinh sự kiện | Có thử nghiệm truy xuất đoạn | Độ khớp F1 theo từ khóa và theo quan hệ, precision của bước khử trùng lặp danh xưng |

- Có thêm hạ tầng tri thức cấp trường (VNU-LIC, giai đoạn 2026–2035), phục vụ nhiều ngành, chưa cắt riêng cho môn Sử.

Gợi ý trình bày: bảng là trọng tâm, tô nổi cột "Đồ án".

## Slide 10. Khoảng trống và câu hỏi nghiên cứu

Nội dung:

- Khoảng trống: chưa có pipeline đo được từ văn bản sử tiếng Việt -> bản ghi chủ thể đã xác lập quan hệ -> knowledge graph. Gold set do con người gắn nhãn dùng để đối chiếu.
- RQ1: Cách quản lý sử liệu và trích xuất sự kiện hiện nay thuận lợi và vướng ở đâu với tiếng Việt và môn Lịch sử phổ thông?
- RQ2: Trong phạm vi đồ án, cách nào vừa sức để trích xuất bản ghi chủ thể và quan hệ, khử trùng lặp danh xưng và nạp vào graph?
- RQ3: Đo chất lượng trích xuất và chất lượng khử trùng lặp danh xưng bằng cách nào?

Gợi ý trình bày: khoảng trống đặt trong một khung nổi bật, ba câu hỏi xếp dọc bên dưới.

## Slide 11. Tính mới và đóng góp

Nội dung:

Cách lưu trữ:

- Lưu theo từng chủ thể thay vì lưu theo từng file sách.
- Một chủ thể chỉ có một định danh trong database. Nhiều tên gọi vẫn là một chủ thể.
- Nếu nhiều đoạn sử liệu khác nhau cùng gắn vào chủ thể. Mỗi đoạn vẫn được giữ nguyên vẹn cùng với nguồn của mình thay vì gộp nội dung.

Pipeline trích xuất:

- Chỉ lưu trữ thông tin nguồn có viết, và lưu kèm câu gốc.
- Xác định các đoạn sử liệu cùng chủ thể và gộp về chung một định danh.
- Hai nguồn không bị trộn thành một câu. Tránh việc gây ra ảo giác AI.

Gợi ý trình bày: hai cột. Cột trái là cách lưu trữ, cột phải là pipeline.

Lời nói: đóng góp là giữ nhiều nguồn trên một chủ thể, và không nhận câu không có trong nguồn. Chưa phải chatbot.

## Slide 12. Mục tiêu đồ án

Nội dung:

| Mục tiêu | Tuần | Việc phải xong |
| --- | --- | --- |
| O1 | 1–3 | Schema tám chủ thể, mã mờ, master registry, ba database |
| O2 | 4–8 | Các API, pipeline trích xuất, khử trùng lặp danh xưng, nạp graph, demo |
| O3 | 9–12 | Gold set do con người gắn nhãn; đo độ khớp F1 và precision trên test set; luận văn và slide |

Gợi ý trình bày: ba bậc thang đi lên, mỗi bậc là một mục tiêu. Tuần 6 là mốc giữa kỳ.

---

# Phần C. Giải pháp

## Slide 13. Hệ thống chủ thể và từ khóa

Nội dung:

| Câu hỏi | Chủ thể | Mẫu mã | Trường phân loại | Ví dụ |
| --- | --- | --- | --- | --- |
| Ai | Person | `P` + 5 số | historical_role_class | Trần Quốc Tuấn |
| Ai, phe nào | Group | `GRP` + 4 số | group_type | Triều Trần, quân Nguyên |
| Việc gì, thế nào | Event | `EV` + 5 số | event_type | Trận Bạch Đằng 1288 |
| Ở đâu | Place | `LOC` + 4 số | spatial_category | Sông Bạch Đằng |
| Khi nào | TimeSpan | `TIM` + 4 số | temporal_granularity | Năm 1288, Mậu Tý |
| Bằng gì | Artifact | `ART` + 4 số | artifact_type | Bãi cọc Yên Giang |
| Vì sao, kế gì | Concept | `CON` + 4 số | concept_category | Cọc ngầm kết hợp thủy triều |
| Dựa vào đâu | Source | `SRC` + 4 số | source_perspective | Toàn thư, Nguyên sử |

- Tám chủ thể là cố định. Mỗi chủ thể có một bộ từ khóa riêng, có thể bổ sung khi làm dữ liệu thật.
- Mã là khóa mờ do PostgreSQL cấp, không chứa tên hay năm. Trường phân loại là danh mục đóng, nhãn ngoài danh mục thì bị từ chối.

Gợi ý trình bày: tám ô màu xếp quanh một vòng tròn, mỗi ô ghi câu hỏi, tên chủ thể và một ví dụ. Bảng chi tiết có thể đưa vào phụ lục.

Lời nói: mỗi câu hỏi 5W1H trỏ tới một loại thực thể. Không nêu tổng số từ khóa, vì danh mục còn thay đổi.

## Slide 14. Ví dụ kết quả trích xuất: Bạch Đằng 1288

Nội dung:

| Chủ thể | Mã | Một số từ khóa có giá trị |
| --- | --- | --- |
| Event | `EV00001` | Tên, loại MilitaryBattle, mốc đầu 1288; mốc cuối để null nếu nguồn không ghi |
| Person | `P00001` | Tên chính Trần Quốc Tuấn; danh xưng gặp trong đoạn: Hưng Đạo Vương |
| Group | `GRP0002` | Tên quân Nguyên, loại MilitaryForce |
| Place | `LOC0001` | Tên lịch sử sông Bạch Đằng, loại Battlefield |
| Source | `SRC0001` | Tên nguồn, đoạn trích và vị trí |

- Quan hệ đọc theo mũi tên: Trần Quốc Tuấn -> COMMANDED -> trận (chỉ huy); quân Nguyên -> OPPOSED_IN -> trận (đối địch); trận -> TOOK_PLACE_AT -> sông Bạch Đằng (xảy ra tại); Toàn thư -> SUPPORTS -> trận (dẫn nguồn).
- Nguồn không nói tới thì để trống, ghi null. Kết quả và ý nghĩa của trận chỉ ghi khi nguồn có viết.
- Bảng là ví dụ thiết kế, chưa phải kết quả mô hình đã chạy.

Gợi ý trình bày: bên trái là đoạn chữ có tô màu đoạn trích, bên phải là các thẻ bản ghi chủ thể nối với nhau bằng mũi tên quan hệ. Từ khóa null để màu xám để thấy việc để trống là có chủ ý.

## Slide 15. Quan hệ trên knowledge graph và ràng buộc

Nội dung:

- Quan hệ chính: COMMANDED, PARTICIPATED_IN, OPPOSED_IN, TOOK_PLACE_AT, OCCURRED_DURING, EMPLOYED_STRATEGY, LEFT_HERITAGE, SUPPORTS.
- Mỗi quan hệ chỉ nối đúng cặp chủ thể, ví dụ COMMANDED đi từ Person tới Event. Sai cặp thì bị từ chối.
- Ràng buộc trong đồ án:
  - Bản ghi đã xác nhận phải có quan hệ SUPPORTS từ ít nhất một Source.
  - Kiểm niên đại: nhân vật không thể tham gia sự kiện ngoài khoảng sinh và mất; vi phạm thì gắn FLAGGED.
  - Một thực thể chỉ có một mã.
  - Trường modern_name của địa danh điền tay.
- Ghi dị bản giữa hai nguồn để cuối Phase 1.

Gợi ý trình bày: vẽ graph Bạch Đằng 1288. Node Event ở giữa, xung quanh là Person, Group, Place, TimeSpan, Concept, Artifact, Source, mỗi edge ghi tên quan hệ.

## Slide 16. Pipeline bốn bước

Nội dung:

1. Tiếp nhận: lưu văn bản gốc kèm source_id và mã hash để không nhận trùng.
2. Trích xuất: LLM trả về bản ghi chủ thể và quan hệ theo schema, mỗi giá trị kèm đoạn trích và vị trí ký tự. Sai schema thì bị từ chối.
3. Khử trùng lặp danh xưng cho Person, Group, Place: tra `entity_aliases` trên PostgreSQL; chưa chắc thì đo string similarity (threshold khởi điểm khoảng 82%, tinh chỉnh trên dev set) và so embedding; dưới threshold thì FLAGGED. Mã mới do sequence cấp.
4. Nạp graph: nạp theo batch bằng MERGE trên mã đã cấp, cùng mã thì cập nhật, không nhân đôi.

Gợi ý trình bày: bốn khối nối bằng mũi tên. Dưới mỗi khối ghi trạng thái lỗi (từ chối, DRAFT, FLAGGED).

## Slide 17. Kiến trúc và công nghệ

Nội dung:

| Thành phần | Công nghệ | Vai trò trong đồ án |
| --- | --- | --- |
| Backend, API và schema | Python 3.12, FastAPI, Pydantic | Bốn API, từ chối kết quả sai schema |
| Graph database | Neo4j 5 | Bắt buộc có dữ liệu demo |
| Vector database | ChromaDB | Dựng sẵn schema và vài bản ghi mẫu |
| Master registry, nguồn và log | PostgreSQL 16 | Cấp mã mờ, tra danh xưng, giữ văn bản gốc và log nạp |
| Trích xuất | LLM có structured output | Tên mô hình ghi trong báo cáo |
| So danh xưng | Embedding model tiếng Việt (PhoBERT hoặc tương đương) | Chỉ để xếp hạng ứng viên |
| Demo | Streamlit | Dán chữ, xem kết quả trích xuất, nạp graph |
| Triển khai | Docker Compose, Git | Chạy lại được trên máy khác |

Gợi ý trình bày: sơ đồ kiến trúc. Trên cùng là Streamlit, giữa là FastAPI và ba bước xử lý, dưới cùng là ba database. Vector database vẽ nét đứt vì không nằm trên đường đi bắt buộc của demo.

---

# Phần D. Kế hoạch và đánh giá

## Slide 18. Kế hoạch và rủi ro

Nội dung:

| Tuần | Việc chính | Xong khi |
| --- | --- | --- |
| 1–3 | Schema, mã mờ, master registry, ba database | Sequence cấp được mã; bản ghi mẫu trên Neo4j |
| 4–6 | Bốn API, gold set, họp giữa kỳ | Bốn endpoint gọi được; schema đóng để đo |
| 7–9 | Nạp graph, khử trùng lặp danh xưng, demo, đo | Danh xưng đã có về đúng mã cũ; có bảng số đo |
| 10–12 | Luận văn và slide | Bản thảo và slide nộp được |

Rủi ro chính:

- Mô hình bỏ sót hoặc trích thêm: từ chối kết quả sai schema, thiếu đoạn trích thì DRAFT.
- Gộp nhầm hai người: threshold tinh chỉnh trên dev set, dưới threshold thì gắn cờ FLAGGED.
- Phạm vi phình sang chatbot: demo chỉ có ba bước, không có ô chat.
- Đổi mô hình giữa chừng: mỗi lần chạy ghi tên mô hình, báo cáo cuối chỉ dùng một cấu hình.

Gợi ý trình bày: biểu đồ Gantt bốn hàng bên trái, bốn rủi ro bên phải.

## Slide 19. Kế hoạch đánh giá

Nội dung:

| Chỉ số | Cách tính | Đích |
| --- | --- | --- |
| Độ khớp F1 theo từ khóa | So từng từ khóa của từng bản ghi chủ thể với gold set, phải kèm đoạn trích đúng; báo riêng từng chủ thể | 85% đến 90% |
| Độ khớp F1 theo quan hệ | Đúng mã đầu, loại quan hệ, mã cuối và có đoạn trích | 75% đến 85% |
| Precision của bước khử trùng lặp danh xưng | Chỉ tính các ca hệ thống tự quyết | 90% đến 95% |
| Thời gian trích xuất | Từ khi nhận chữ đến khi có kết quả đúng schema | Dưới 3 đến 5 giây mỗi trang |

- Các con số là đích đặt ra, chưa phải kết quả đã đo.
- Gold set do người gắn nhãn, không nhìn kết quả mô hình. Tách dev set và test set. Test set chỉ dùng một lần.
- Khớp từ khóa khi cùng giá trị và có đúng đoạn trích. Thừa, thiếu và null được tính riêng. Báo riêng từng chủ thể.
- Precision chỉ tính ca hệ thống tự gộp. Ca FLAGGED không đưa vào mẫu số.
- Thời gian là trung bình trên test set, từ lúc nhận chữ đến JSON đúng schema.

Gợi ý trình bày: bốn thẻ chỉ số lớn, dưới mỗi thẻ ghi cách tính trong một dòng.

## Slide 20. Demo dự kiến và sản phẩm bàn giao

Nội dung:

Kịch bản demo khoảng ba phút:

1. Mở graph đã có sẵn một số node Person.
2. Dán một đoạn chữ mới chưa có trong kho.
3. Trích xuất và xem các bản ghi chủ thể cùng quan hệ, mỗi giá trị kèm đoạn trích.
4. Nạp graph: danh xưng đã có trong master registry đi vào đúng mã cũ, chủ thể mới và quan hệ mới thành nhánh mới.
5. Hiển thị độ khớp F1 theo từ khóa, theo quan hệ, và precision trên test set.

Bàn giao:

- Source code chạy bằng Docker, tài liệu API.
- Neo4j đã nạp kho thí điểm, PostgreSQL giữ master registry, nguồn và log.
- Gold set khoảng 150 đến 200 đoạn sử liệu có nhãn, báo cáo số đo.

Gợi ý trình bày: ảnh chụp giao diện Streamlit dạng mockup kèm năm bước. Có thể chèn ảnh graph trên Neo4j Browser.

## Slide 21. Tóm tắt và hỏi đáp

Nội dung:

- Dự án: kho sử liệu có dẫn nguồn, để người học hỏi và kiểm nguồn.
- Đồ án: phần mở đầu, trích xuất văn bản sử thành bản ghi chủ thể và quan hệ, khử trùng lặp danh xưng, nạp vào knowledge graph, có số đo.
- Đóng góp: lưu nhiều đoạn sử liệu trên cùng một chủ thể, và không nhận câu LLM thêm ra khi không có đoạn trích.
- Cảm ơn hội đồng. Hỏi đáp.

Gợi ý trình bày: ba dòng tóm tắt và một câu cảm ơn. Nền giống slide bìa.

---

## Điểm cần duyệt

- Đích độ khớp F1 theo quan hệ (75% đến 85%) là đề xuất mới khi bỏ phiếu 10 trường, thấp hơn đích theo từ khóa vì một quan hệ chỉ khớp khi cả hai đầu mã đều đúng. Cần duyệt cùng giảng viên.
- Slide 9 và slide 17 có bảng dày. Có thể chuyển bảng chi tiết ra phụ lục và chỉ giữ ý chính trên slide.
- Thời lượng mỗi phần (gợi ý): phần A khoảng 3 phút, phần B khoảng 5 phút, phần C khoảng 5 phút, phần D khoảng 4 phút.
