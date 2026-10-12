# Đồ án trong dự án

Tên đề tài: Triển khai hệ thống CSDL đồ thị tri thức và thiết kế pipeline trích xuất mạng lưới thực thể lịch sử 5W1H bằng LLM.

Người thực hiện: Trần Việt Hoàng. MSSV: 25MSA13219. Giảng viên hướng dẫn: TS Bùi Trung Hiếu.

Bản này bám slide `Do An/slide-gioi-thieu-do-an.pptx`, viết dài hơn. Phần mô tả không gắn số liệu thí điểm. Phần ví dụ để riêng ở cuối.

Nguồn đang dùng:

- Dự án: `Project tong/master-proposal-18-thang.docx`
- Đồ án: `Do An/thesis-proposal/muc-01.md` đến `muc-06.md`. Bản chi tiết cũ: `Do An/proposal/proposal.md`.
- Mã và ba database: `Note/thiet-ke-dinh-danh.md`. Chủ thể và từ khóa: `Note/01-bai-toan/he-thong-chu-the-va-tu-khoa.md`.

---



# Phần mô tả



## 1. Đồ án là gì

Đồ án triển khai hệ thống CSDL đồ thị tri thức và thiết kế pipeline trích xuất mạng lưới thực thể lịch sử 5W1H bằng LLM. Về kỹ thuật, đó là hạ tầng multi-model database (graph, vector và relational database) và pipeline trích xuất thực thể và quan hệ theo hệ thống chủ thể và từ khóa.

Đồ án là phần mở đầu của dự án. Sản phẩm của đồ án là mạng lưới thực thể trên knowledge graph, không phải chatbot cho học sinh. Thời lượng của đồ án và của dự án ghi ở mục 3 và mục 11.

## 2. Bài toán

Chương trình môn Lịch sử 2018 yêu cầu người học nêu sự kiện có thời gian và địa điểm, chỉ ra tư liệu, và nối nguyên nhân với diễn biến. Trên lớp, bài giảng lịch sử nằm lại trong vở, khó dùng lại và không đo được độ bám nguồn.

Thư viện số tìm được cuốn sách nhưng không trả lời được câu bên trong tệp, ví dụ ai có mặt ở trận Bạch Đằng 1288.

LLM trả lời trôi chảy nhưng có thể thêm năm hoặc người không có trong nguồn. Một nhân vật có nhiều tên gọi nên kho dễ bị nhân đôi.

Cùng một sự kiện có thể được hai nguồn kể khác nhau. Kho dữ liệu không được xóa một nguồn để chỉ giữ một đáp án.

Vì vậy, thực tiễn yêu cầu cần có một hệ thống giải quyết các vấn đề này.

Mục tiêu chung của đồ án là một pipeline đo được:

- Từ văn bản sử tiếng Việt, tới bản ghi các chủ thể đã xác lập quan hệ bằng cách trích xuất tri thức từ đoạn trích bằng LLM, tới knowledge graph tổng quan xác lập quan hệ của các chủ thể.
- Gold set dữ liệu mẫu do con người gắn nhãn.
- O1. Chốt schema của hệ thống chủ thể và từ khóa, và dựng ba database chạy bằng Docker.
- O2. Dựng các API và pipeline để trích xuất, khử trùng lặp danh xưng, nạp graph, cùng giao diện demo cho người vận hành.
- O3. Lập gold set khoảng 150 đến 200 đoạn sử liệu do con người gắn nhãn, rồi đo độ khớp F1 và precision của việc trích xuất data trên test set.

## 3. Đồ án nằm ở đâu trong dự án

Dự án dài 18 tháng, chia hai giai đoạn.

Phase 1, tháng 1 đến tháng 8, làm kho dữ liệu: schema chủ thể và từ khóa, graph database, vector database, relational database, pipeline trích xuất, khử trùng lặp danh xưng, liên kết đoạn văn với node, và cách giữ hai nguồn mâu thuẫn.

Phase 2, tháng 9 đến tháng 18, làm lớp hỏi đáp: agent chọn loại truy vấn, lọc theo thời gian và địa điểm, scaffolding cho người học kiểm nguồn và đối chiếu.

Đồ án là 12 tuần mở đầu Phase 1, theo đề cương.

## 4. Phạm vi đồ án

Trong đồ án:

- Chốt schema của hệ thống chủ thể và từ khóa: tám chủ thể, bộ từ khóa, mã định danh, danh mục phân loại, kiểu quan hệ.
- Dựng Neo4j, ChromaDB và PostgreSQL, đóng bằng Docker.
- Trích xuất văn bản đã làm sạch thành JSON gồm bản ghi chủ thể và quan hệ.
- Khử trùng lặp danh xưng: gộp các danh xưng của cùng một thực thể về một mã.
- Nạp vào graph, chạy lại không nhân đôi node.
- Giao diện demo nội bộ và gold set để đo.

Chưa làm trong đồ án:

- Cắt đoạn và embedding toàn bộ đoạn văn, liên kết mã node hàng loạt.
- Edge đồng thuận hoặc mâu thuẫn giữa hai nguồn.
- Chatbot, câu hỏi gợi mở, thử trên lớp.

Đầu vào của đồ án là văn bản sử liệu tiếng Việt. Không cần OCR.

Kho thí điểm là các sử liệu đã được gắn nhãn về một sự kiện lịch sử, lấy từ nhiều nguồn.

## 5. Tính mới và đóng góp

Đồ án đóng góp một cách lưu trữ theo chủ thể, và một pipeline trích xuất bám nguồn.

Cách lưu trữ:

- Lưu theo từng chủ thể thay vì lưu theo từng file sách.
- Một chủ thể chỉ có một định danh trong database. Nhiều tên gọi vẫn là một chủ thể.
- Nếu nhiều đoạn sử liệu khác nhau cùng gắn vào chủ thể. Mỗi đoạn vẫn được giữ nguyên vẹn cùng với nguồn của mình thay vì gộp nội dung.

Pipeline trích xuất:

- Chỉ lưu trữ thông tin nguồn có viết, và lưu kèm câu gốc.
- Xác định các đoạn sử liệu cùng chủ thể và gộp về chung một định danh.
- Hai nguồn không bị trộn thành một câu. Tránh việc gây ra ảo giác AI.

## 6. Từ 5W1H sang hệ thống chủ thể và từ khóa

5W1H là cách buộc một sự kiện đủ thành phần trước khi kể lại: việc gì, ai, ở đâu, khi nào, vì sao, diễn ra thế nào. Sáu câu này là một mạch, không phải sáu trường tra cứu rời.

Mỗi câu hỏi trỏ tới một loại thực thể khác nhau, và mỗi loại cần được mô tả bằng thông tin riêng. Vì vậy schema của đồ án không phải một phiếu cố định cho sự kiện, mà là một hệ thống chủ thể và từ khóa. Tám chủ thể đã cố định:


| Câu hỏi       | Chủ thể             | Label       |
| ------------- | ------------------- | ----------- |
| Who           | Con người           | Person      |
| Who, by whom  | Tổ chức, thể chế    | Group       |
| What, how     | Sự kiện             | Event       |
| Where         | Không gian, địa lý  | Place       |
| When          | Thời gian, niên đại | TimeSpan    |
| What, means   | Hiện vật, di sản    | Artifact    |
| Why, strategy | Kế sách, tư tưởng   | Concept     |
| Evidence      | Nguồn sử liệu       | Source      |


Chuẩn CIDOC CRM chỉ được mượn ý mô tả quá khứ bằng thực thể và quan hệ. Đồ án không dựng đủ mọi lớp của chuẩn đó.

## 7. Từ khóa, quan hệ và ràng buộc

Mỗi chủ thể có một bộ từ khóa, tức các thuộc tính để mô tả và tra cứu. Ví dụ: con người có tên chính, các danh xưng khác, vai trò, năm sinh và năm mất; sự kiện có tên, loại, mốc đầu và mốc cuối, tóm tắt diễn biến, kết quả và ý nghĩa nếu nguồn có viết; địa danh có tên lịch sử và tên ngày nay; nguồn có tác giả, thời điểm biên soạn, góc nhìn và đoạn trích. Bộ từ khóa có thể thay đổi khi làm dữ liệu thật. Vì vậy đồ án gọi chung là hệ thống chủ thể và từ khóa, không cố định số lượng từ khóa.

Kết quả trích xuất của một đoạn văn gồm hai phần: các bản ghi chủ thể mà đoạn chữ có nói tới, và các quan hệ giữa chúng. Từ khóa nào nguồn không nói thì để null. Không điền cho đủ. Từ khóa có giá trị và mỗi quan hệ đều phải kèm đoạn trích.

Ba quy chuẩn đi kèm:

- Mã định danh mờ. PostgreSQL cấp mã, không ghép tên hay năm vào mã. Ví dụ minh họa `P00001`, `EV00001`. Quy chuẩn ở `Note/thiet-ke-dinh-danh.md`.
- Danh mục phân loại đóng. Mỗi chủ thể có một trường phân loại, như loại sự kiện hay vai trò của một người. Trường này chỉ nhận giá trị trong danh mục. Mô hình trả nhãn ngoài danh mục thì kết quả bị từ chối.
- Linked open data. Node có trường cho mã Wikidata, GeoNames hoặc VIAF. Các trường này được phép trống, và chỉ điền khi đã tự tra mã.

Các nhóm quan hệ chính: người với sự kiện (chỉ huy, tham gia, ở phía đối địch), người với tổ chức (đứng đầu, phụng sự, chống đối), sự kiện với nơi, với thời gian, với kế sách, với hiện vật, và mọi chủ thể với nguồn. Mỗi quan hệ chỉ nối đúng cặp chủ thể của nó. Quan hệ nối sai cặp thì bị từ chối.

Ràng buộc để giữ tính chân thực sử học:


| Ràng buộc                                                        | Trong đồ án                                                       |
| ---------------------------------------------------------------- | ----------------------------------------------------------------- |
| Một người không tham gia sự kiện trước khi sinh hoặc sau khi mất | Kiểm khi nạp. Vi phạm thì `FLAGGED`                       |
| Địa danh lịch sử đi kèm tên ngày nay                             | Có trường modern_name, điền tay trong danh mục địa danh thí điểm  |
| Mọi khẳng định gắn với ít nhất một nguồn                         | Có. Thiếu đoạn trích thì `DRAFT`                          |
| Một người nhiều tên vẫn là một node                              | Có, qua module khử trùng lặp danh xưng                            |
| Hai nguồn kể khác nhau thì giữ cả hai                            | Chưa. Thuộc cuối Phase 1                                          |


Đồ án khai báo đủ tám chủ thể trong schema, và nạp những chủ thể mà đoạn chữ thí điểm có nói tới. Đơn vị đo độ khớp F1 là từ khóa của từng bản ghi chủ thể và từng quan hệ.

## 8. Bốn tầng lưu trữ

Neo4j là graph database, giữ quan hệ. Đây là tầng đồ án bắt buộc nạp. Câu trả lời sau này chỉ được dùng edge đã có trong graph.

ChromaDB là vector database, giữ các đoạn văn đã cắt và mã node liên quan. Đồ án tạo collection và schema. Embedding hàng loạt nằm ở phần sau của Phase 1.

PostgreSQL là master registry: cấp mã mờ, giữ danh xưng, nguồn và log (`dim_entities`, `entity_aliases`). Neo4j và ChromaDB dùng đúng các mã này.

Tầng agent nhận câu hỏi, truy vấn graph và vector, rồi sinh câu trả lời. Tầng này thuộc Phase 2.

Công cụ đã chốt cho đồ án: Python, FastAPI, Pydantic, Neo4j, ChromaDB, PostgreSQL, Docker, Streamlit.

## 9. Pipeline

Thứ tự xử lý:

1. Nhận một đoạn văn bản đã làm sạch. PostgreSQL lưu nguồn.
2. LLM trích xuất JSON gồm bản ghi chủ thể và quan hệ, chưa cấp mã cuối. Sai schema, nhãn phân loại ngoài danh mục hoặc quan hệ nối sai cặp chủ thể thì không nạp.
3. Tra `entity_aliases` trên PostgreSQL. Khớp thì lấy mã cũ. Không chắc thì `FLAGGED`. Thực thể mới do sequence cấp mã.
4. Kiểm ràng buộc niên đại. Năm sự kiện nằm ngoài năm sinh và năm mất của người tham gia thì `FLAGGED`.
5. Ghi Cypher vào Neo4j bằng MERGE trên mã đã cấp. Cùng mã thì cập nhật.

Mỗi từ khóa và mỗi quan hệ đưa vào graph như bản đã xác nhận phải trỏ được về một đoạn chữ. Không có đoạn trích thì bản ghi ở trạng thái `DRAFT`.

Khử trùng lặp danh xưng chạy trước lệnh tạo node Person. Trước tuần 8 có thể nạp với danh xưng đã chuẩn hóa tay. Tuần 8 mới bật khử trùng lặp danh xưng tự động.

API của đồ án:


| Endpoint                | Việc                                                       |
| ----------------------- | ---------------------------------------------------------- |
| /extract-5w1h           | Văn bản vào, JSON bản ghi chủ thể và quan hệ ra            |
| /resolve-entity         | Danh xưng vào, mã trong master registry hoặc trạng thái FLAGGED |
| /ingest-graph           | JSON đã qua khử trùng lặp danh xưng, nạp vào Neo4j         |
| /entities/{entity_id}   | Một chủ thể và các edge một bước, phục vụ demo             |




## 10. Demo

Demo khoảng ba phút, trên giao diện nội bộ, không phải lớp học:

1. Mở graph đã có sẵn một số node Person.
2. Dán một đoạn chữ mới, chưa nằm trong kho.
3. Trích xuất và xem các bản ghi chủ thể cùng quan hệ, mỗi giá trị kèm đoạn trích.
4. Nạp graph: danh xưng đã biết đi vào node cũ, chủ thể mới và quan hệ mới thành nhánh mới.
5. Chỉ số độ khớp F1 theo từ khóa, theo quan hệ, và precision trên test set của gold set.



## 11. Lộ trình

Đồ án làm trong 12 tuần:

| Tuần | Việc | Xong khi |
| --- | --- | --- |
| 1–3 | Schema, mã mờ, master registry, ba database | Sequence cấp được mã; bản ghi mẫu trên Neo4j |
| 4–6 | Bốn API, gold set, họp giữa kỳ | Bốn endpoint gọi được; schema đóng để đo |
| 7–9 | Nạp graph, khử trùng lặp danh xưng, demo, đo | Danh xưng đã có về đúng mã cũ; có bảng số đo |
| 10–12 | Luận văn và slide | Bản thảo và slide nộp được |

Phần còn lại của dự án, không thuộc cam kết của đồ án. Dự án dài 18 tháng.

| Mốc | Việc | Thuộc |
| --- | --- | --- |
| Tháng 5–8 | Cắt đoạn, embedding hàng loạt, dị bản, nghiệm thu Phase 1 | Phase 1, sau đồ án |
| Tháng 9–18 | Agent, scaffolding, thử trên lớp, báo cáo cả dự án | Phase 2 |


Ba việc scaffolding của Phase 2 là kiểm nguồn, đặt sự kiện vào đúng thời và nơi, đối chiếu hai nguồn. Đồ án chưa làm ba việc đó. Đồ án tạo dữ liệu để làm được.

## 12. Bàn giao và chỉ số của đồ án

Bàn giao:

- Mã nguồn FastAPI, chạy bằng Docker.
- Neo4j đã nạp kho thí điểm.
- PostgreSQL giữ master registry, nguồn và log.
- Streamlit cho ba bước demo.
- Gold set khoảng 150 đến 200 đoạn sử liệu có nhãn chủ thể, từ khóa và quan hệ.
- Báo cáo số đo và tài liệu API.

Chỉ số mang ra hội đồng là chỉ số của đồ án, không lấy chỉ số của dự án:


| Chỉ số                  | Mốc                         |
| ----------------------- | --------------------------- |
| Độ khớp F1 theo từ khóa | 85% đến 90%                 |
| Độ khớp F1 theo quan hệ | 75% đến 85%                 |
| Precision khử trùng lặp danh xưng | 90% đến 95%             |
| Thời gian trích xuất    | Dưới 3 đến 5 giây mỗi trang |


Các mốc trên là đích đặt ra, chưa phải kết quả đã đo.

Gold set do người gắn nhãn chủ thể, từ khóa và quan hệ, không nhìn kết quả mô hình. Tập này tách thành dev set và test set. Threshold và prompt chỉ tinh chỉnh trên dev set. Test set chỉ dùng một lần để ra số báo cáo.

Độ khớp F1 theo từ khóa tính trên từng từ khóa có giá trị. Khớp khi cùng chủ thể, cùng từ khóa, cùng giá trị và có đúng đoạn trích. Giá trị thừa, giá trị bị bỏ sót, và ô null ở cả hai bên được tính riêng. Báo riêng từng chủ thể.

Độ khớp F1 theo quan hệ chỉ khớp khi đủ bốn điều kiện: đúng mã đầu, đúng loại quan hệ, đúng mã cuối, và có đoạn trích.

Precision của bước khử trùng lặp danh xưng chỉ tính ca hệ thống tự gắn danh xưng vào một mã đã có. Ca FLAGGED không đưa vào mẫu số. Gắn đúng mã thì tính đúng. Gắn nhầm sang chủ thể khác thì tính sai.

Thời gian trích xuất là trung bình trên test set, từ lúc nhận đoạn chữ đến lúc có JSON đúng schema. Bản ghi thiếu đoạn trích ở trạng thái DRAFT và không được tính là khớp. Nếu thấp hơn đích, báo cáo vẫn hợp lệ khi có bảng lỗi theo chủ thể và theo loại quan hệ.

## 13. Chỉ số của các giai đoạn sau trong dự án

Không đưa các mốc này vào cam kết bảo vệ đồ án.

Hết Phase 1, proposal dự án đặt độ khớp F1 từ 90%, precision khử trùng lặp danh xưng từ 95%, hybrid search (truy vấn kết hợp graph và vector) dưới 1,5 đến 2 giây. Mọi khẳng định đưa vào phần dị bản phải có source_id.

Phase 2, proposal dự án đặt tỷ lệ câu trả lời truy được về node hoặc đoạn văn, tỷ lệ giữ đúng biên thời gian và địa điểm, và tỷ lệ đánh giá tích cực của giáo viên cùng học sinh. Các tỷ lệ đó chỉ có nghĩa sau khi có tập câu hỏi và phiếu khảo sát.

---



# Phần ví dụ

Các ví dụ dưới đây chỉ để hình dung dữ liệu và demo. Chúng không phải kết quả đã đo.

## Ví dụ A. Trận Bạch Đằng 1288 nhìn theo 5W1H

Sự kiện thí điểm là trận trên sông Bạch Đằng năm 1288. Mỗi dòng dưới đây sẽ thành một hoặc nhiều bản ghi chủ thể ở ví dụ B.


| Câu hỏi | Nội dung minh họa                                       |
| ------- | ------------------------------------------------------- |
| What    | Trận thủy chiến trên sông Bạch Đằng                     |
| Who     | Trần Quốc Tuấn, vua Trần Nhân Tông; tướng nhà Nguyên    |
| Where   | Sông Bạch Đằng, vùng Quảng Ninh và Hải Phòng            |
| When    | Năm 1288, trong kháng chiến lần thứ ba                  |
| Why     | Thế trận, lương thảo và đường rút, chỉ khi nguồn có nói |
| How     | Cọc gỗ, thủy triều, nhử thuyền                          |


Mã sự kiện minh họa: `EV00001`.

## Ví dụ B. Tám chủ thể quanh trận Bạch Đằng 1288

Mã và nhãn phân loại dưới đây minh họa cách đặt mã, không phải dữ liệu đã nạp.


| Chủ thể    | Mã minh họa                                 | Phân loại                            |
| ---------- | ------------------------------------------- | ------------------------------------ |
| Con người  | `P00001`                | `MilitaryCommander`                  |
| Tổ chức    | `GRP0001`, `GRP0002`         | `Dynasty`, `MilitaryForce`           |
| Sự kiện    | `EV00001`                         | `MilitaryBattle`                     |
| Không gian | `LOC0001`                        | `Battlefield`                        |
| Thời gian  | `TIM0001`                          | `SpecificYear`                       |
| Hiện vật   | `ART0001`                     | `WeaponEquipment`                    |
| Kế sách    | `CON0001`                 | `MilitaryTactic`                     |
| Nguồn      | `SRC0001`, `SRC0002` | `DomesticOfficial`, `ForeignHostile` |


Mỗi node chỉ được nạp như đã xác nhận khi đoạn chữ thí điểm có nói tới nó và chỉ được câu trích.

## Ví dụ C. Danh xưng và trùng tên

Các chuỗi sau phải cùng một node `P00001`:

- Trần Quốc Tuấn
- Trần Hưng Đạo
- Hưng Đạo Vương
- Hưng Đạo Đại Vương
- Tiết chế Quốc công

Nếu đoạn mới chỉ viết "Hưng Đạo Vương", pipeline không được tạo node Person thứ hai.

Chiều ngược lại: cùng một địa danh nhưng khác năm là ba sự kiện, ví dụ `EV00002`, `EV00003`, `EV00001`. Năm không nằm trong mã. Đoạn nói về năm 938 không được gắn vào sự kiện năm 1288.

## Ví dụ D. Bản ghi trên graph

```cypher
MERGE (p:Person {id:'P00001'})
  SET p.canonical_name = 'Trần Quốc Tuấn',
      p.aliases = ['Trần Hưng Đạo', 'Hưng Đạo Vương', 'Hưng Đạo Đại Vương']
MERGE (e:Event {id:'EV00001'})
  SET e.event_name = 'Trận Bạch Đằng năm 1288', e.event_type = 'MilitaryBattle'
MERGE (l:Place {id:'LOC0001'})
  SET l.historical_name = 'Sông Bạch Đằng'
MERGE (c:Concept {id:'CON0001'})
  SET c.concept_category = 'MilitaryTactic'
MERGE (s:Source {id:'SRC0001'})
MERGE (p)-[:COMMANDED]->(e)
MERGE (e)-[:TOOK_PLACE_AT]->(l)
MERGE (e)-[:EMPLOYED_STRATEGY]->(c)
MERGE (s)-[:SUPPORTS {quote:'Đoạn trích trong nguồn'}]->(e)
```

Tìm theo danh xưng:

```cypher
MATCH (p:Person)-[r]->(e:Event)
WHERE p.canonical_name = 'Trần Quốc Tuấn'
   OR 'Hưng Đạo Đại Vương' IN p.aliases
RETURN p, r, e
```



## Ví dụ E. Đoạn văn gắn mã node

Việc này thuộc phần sau của Phase 1, không phải điều kiện của demo đồ án. Cấu trúc cần nhớ:

```json
{
  "id": "vec_chunk_1088",
  "document": "Đoạn chữ trong nguồn về cọc và thủy triều.",
  "metadata": {
    "linked_entity_ids": ["P00001", "EV00001", "LOC0001"],
    "event_type": "MilitaryBattle",
    "source_id": "SRC0001",
    "page": "58"
  }
}
```

Không có `linked_entity_ids` thì đoạn đó không được dùng để khẳng định một quan hệ. Metadata filter theo mã giúp thu hẹp các đoạn được dùng, nhưng không bảo đảm câu trả lời đúng tuyệt đối.

## Ví dụ F. Hai nguồn không nói giống nhau

Việc này thuộc cuối Phase 1. Hai khẳng định cùng được lưu. Pipeline không chọn một câu làm sự thật duy nhất.

```text
Nguồn Đại Việt sử ký khẳng định: cắm cọc, dụ theo thủy triều.
Nguồn Nguyên sử khẳng định: rút vì lương và địa hình.
Hai khẳng định mâu thuẫn ở khía cạnh nguyên nhân.
```



## Ví dụ G. Câu hỏi của Phase 2

Chưa làm trong đồ án. Giữ để khỏi xây nhầm chatbot.

Câu "Hưng Đạo đại vương là ai?" là hỏi một người và các edge một bước, không phải hỏi toàn bộ một trận.

Câu "Cách đánh nào trên sông Bạch Đằng năm 1288?" phải khóa năm 1288 và mã `LOC0001`. Không kéo tiểu sử sau năm 1288 vào câu trả lời.

Câu "Các trận trên sông Bạch Đằng có gì kế thừa nhau?" mới được đi qua cả ba mã `EV00002`, `EV00003`, `EV00001`.

Câu gợi mở chỉ được hỏi một quan hệ đã có trên graph, ví dụ một người khác đã có edge với sự kiện đó.