# Triển khai hệ thống CSDL đồ thị tri thức và thiết kế pipeline trích xuất mạng lưới thực thể lịch sử 5W1H bằng LLM

**Trường Đại học FPT**

**FPT University**

**Capstone Project Proposal**

*Implementing a Knowledge Graph Database System and Designing an LLM Pipeline to Extract a 5W1H Network of Historical Entities*

- Người thực hiện: Trần Việt Hoàng
- MSSV: 25MSA13219
- Giảng viên hướng dẫn: TS Bùi Trung Hiếu
- Phạm vi: phần mở đầu Phase 1 của dự án
- Hà Nội, tháng 10 năm 2026

*Cùng đề tài, cùng phạm vi và cùng các mục với bản Do An/capstone-proposal-q1-q2-chi-tiet.docx. Bản này viết bằng lời thường, để người không làm kỹ thuật vẫn đọc được từng chương. Thuật ngữ IT thông dụng giữ nguyên tiếng Anh và được giải thích ở lần đầu xuất hiện.*

# Tóm tắt

Đồ án làm một việc hẹp và trọn. Một đoạn sử liệu tiếng Việt đã có sẵn chữ được trích xuất theo hệ thống chủ thể và từ khóa. Hệ thống có tám chủ thể cố định: con người, tổ chức, sự kiện, nơi chốn, thời gian, hiện vật, kế sách hoặc tư tưởng, và nguồn sử liệu. Mỗi chủ thể được mô tả bằng một bộ từ khóa, ví dụ một người có tên chính, các danh xưng khác, năm sinh và năm mất. Kết quả trích xuất của một đoạn gồm các bản ghi chủ thể mà đoạn chữ có nói tới, cùng các quan hệ giữa chúng: ai chỉ huy trận nào, trận diễn ra ở đâu, vào lúc nào, dùng kế sách gì, nguồn nào ghi lại. Các bản ghi và quan hệ đó được nạp vào một knowledge graph, tức một mạng các node (điểm dữ liệu) nối với nhau bằng quan hệ. Nhiều cách gọi của cùng một người, chẳng hạn Trần Quốc Tuấn và Hưng Đạo Vương, được gộp về một node; bước này gọi là khử trùng lặp danh xưng, hay loại bỏ trùng lặp danh xưng. Từ khóa nào đoạn chữ không nói thì để trống. Nếu hệ thống không chỉ ra được câu nào trong nguồn thì bản ghi hoặc quan hệ đó ở trạng thái draft (nháp), chưa được xem là đã kiểm.

Đồ án là phần mở đầu của dự án. Dự án muốn để người học hỏi trên mạng lưới thực thể đó và đối chiếu nguồn. Đồ án chưa làm chatbot cho học sinh, chưa mang vào một lớp học, và chưa ghi cạnh nhau hai bộ sử khi chúng kể lệch nhau. Những việc đó cần một kho đã đo được trước. Người dùng trực tiếp của đồ án là người xây kho và người xem demo. Học sinh và giáo viên là người mà các giai đoạn sau của dự án sẽ phục vụ.

# Mục lục

1. Introduction

1.1. Problem Description

1.2. Research objectives

1.3. Scope of the Project

2. Background and Related Work

2.1. Tư duy lịch sử và 5W1H

2.2. Thực trạng tại Việt Nam

2.3. Hướng kỹ thuật liên quan

3. Proposed Solution

3.1. Solution Description

3.2. Software Architecture

3.3. Technology and Tools Used

4. Project Plan

4.1. Main development stages

4.2. Expected schedule

4.3. Feasibility Assessment

5. Evaluation Plan

5.1. Expected Results

5.2. Evaluation method

References

# 1. Introduction

Đồ án là phần có thể bảo vệ được của dự án. Về lộ trình, dự án kéo dài khoảng mười tám tháng. Tám tháng đầu dành cho kho tư liệu. Mười tháng sau dành cho việc người học đặt câu hỏi trên kho đó, được nhắc xem nguồn, và được thấy khi hai sách không nói giống nhau. Đồ án lấy bốn tháng đầu: chốt schema của hệ thống chủ thể và từ khóa, dựng các database, trích xuất văn bản thành bản ghi chủ thể và quan hệ, khử trùng lặp danh xưng, và nạp kết quả vào graph.

Lý do của cả việc này nằm ở môn Lịch sử, không nằm ở một phần mềm có sẵn. Chương trình giáo dục phổ thông môn Lịch sử, ban hành kèm Thông tư số 32/2018/TT-BGDĐT, đặt ba năng lực: tìm hiểu lịch sử, nhận thức và tư duy lịch sử, rồi vận dụng những gì đã học [1]. Người học cần nêu được sự kiện có thời và nơi, chỉ ra tư liệu mình dựa vào, và nói được quan hệ giữa nguyên nhân với diễn biến. Tài liệu tập huấn của Trường Đại học Sư phạm Hà Nội cũng hướng dẫn luyện tập tư duy đó trên lớp [2]. Đồ án lấy các năng lực này làm chỗ đứng. Hệ thống chỉ làm phần thư ký: ghi những gì đoạn chữ đã nói, để các giai đoạn sau của dự án mới dùng cho việc hỏi và học.

Sử học làm việc với lời kể có nguồn. Cùng một trận, hai bộ sử có thể nhấn hai điều khác nhau. Giữ được từng lời và ghi rõ lời nào thuộc sách nào thì mới sát cách làm của ngành. Một câu trả lời trôi, đọc thì suôn mà không chỉ được dòng nào trong sách, chưa phải sản phẩm của giờ Sử. Vì vậy đơn vị của đồ án là thực thể và quan hệ kèm đoạn trích, không phải một file máy tính và cũng không phải một câu trả lời hay.

Đồ án không ngồi thay giáo viên và không trả lời hộ học sinh. Đồ án tạo lớp dữ liệu mà các giai đoạn sau của dự án mới dùng để hỏi đáp. Ranh giới này được nhắc lại ở mục tiêu, ở phạm vi, ở kiến trúc và ở kế hoạch, để người đọc thấy đồ án kết thúc ở một mạng lưới thực thể đo được.

## 1.1. Problem Description

Bài toán của đồ án, nói bằng lời thường, là thế này. Có một đoạn sử liệu tiếng Việt đã gõ sẵn. Hệ thống nhận ra trong đoạn đó những người, tổ chức, sự kiện, nơi chốn, mốc thời gian, hiện vật, kế sách và nguồn được nhắc tới. Mỗi thứ thành một bản ghi chủ thể, mang mã và các từ khóa mà đoạn chữ có nói. Hệ thống cũng ghi các quan hệ giữa chúng, như người chỉ huy trận hay trận diễn ra tại sông. Tất cả phải theo schema đã chốt. Schema là khuôn dữ liệu cố định: bản ghi sai chủ thể, từ khóa sai kiểu, nhãn phân loại ngoài danh mục, hoặc quan hệ nối sai cặp chủ thể thì không hợp lệ. Nếu đoạn chữ gọi một người bằng tên khác mà người đó đã có trong kho, bản ghi gắn vào đúng node cũ. Kết quả hợp lệ thì được nạp vào graph. Bản ghi hoặc quan hệ không chỉ ra được câu nguồn thì không được xem là đã xác nhận.

Bối cảnh là dạy và học lịch sử ở Việt Nam, trong một việc nhân văn số nhỏ, làm vừa một kỳ tốt nghiệp. Người trực tiếp dùng và xem là người xây kho. Học sinh chưa phải người dùng của đồ án.

Nguyên nhân của bài toán là chỗ môn học, thói quen trên lớp và các công cụ đang có chưa gặp nhau. Có năm điểm nghẽn. Bốn điểm thuộc việc đồ án phải làm. Điểm thứ năm được ghi ra để khỏi hiểu sai hướng, và được để lại cho giai đoạn sau của dự án.

Thứ nhất, yêu cầu của môn học và công cụ trên lớp chưa gặp nhau. Chương trình đã đòi hỏi tìm tư liệu, đặt sự kiện đúng thời, và suy từ nguyên nhân tới diễn biến [1], [2]. Trên lớp, cách hỏi quen vẫn là sáu câu: việc gì, ai, ở đâu, khi nào, vì sao, và như thế nào. Giáo viên cho học sinh điền phiếu hoặc vẽ sơ đồ. Cách này đúng tinh thần môn học. Sản phẩm ở lại trong vở của từng lớp. Sang bài khác, không ai hỏi tiếp trên chính mạng sự kiện đó, và cũng không có cách đo xem phiếu có bám đúng đoạn chữ hay không.

Thứ hai, thư viện số và phần mềm quản lý trích dẫn dừng ở thông tin bìa của cuốn sách. Mục lục điện tử, kho học liệu và phần mềm trích dẫn giúp tìm lại một tệp khi biết tên sách, tên tác giả hoặc năm in. Đó là việc cần, vì bản gốc phải còn. Nó không trả lời được câu bên trong tệp. Ví dụ: trong các đoạn đang lưu, ai có mặt ở trận Bạch Đằng năm 1288, đoạn nào nói về cọc gỗ, đoạn nào nói về thủy triều. Người đọc vẫn phải mở từng tệp và tự nối.

Thứ ba, các mô hình ngôn ngữ lớn (LLM), như ChatGPT, trả lời được câu hỏi đời thường, nhưng câu trả lời không buộc phải bám một kho dữ liệu đã kiểm. Lewis và cộng sự đã chỉ ra rằng khi tri thức chỉ nằm trong tham số của mô hình thì khó truy đúng nguồn và khó sửa khi sách được cập nhật [3]. Với sử, rủi ro cụ thể là mô hình thêm năm, thêm người, hoặc kể chi tiết không có trong đoạn vừa đưa. Nguyên nhân không phải mô hình “kém văn”. Nguyên nhân là mô hình sinh câu theo xác suất của ngôn ngữ, trong khi giờ Sử cần một người dẫn đúng dòng.

Thứ tư, một người, một nơi, một trận trong sử liệu Việt Nam thường có nhiều cách viết. Trần Quốc Tuấn, Hưng Đạo Vương và Hưng Đạo Đại Vương là một người. Nếu mỗi cách viết thành một node riêng, graph bị đứt: trận gắn với tên này, chiếu gắn với tên kia, người xem tưởng là hai nhân vật. Nếu thấy hai chuỗi gần giống nhau là gộp làm một, lại có thể gộp nhầm hai người khác nhau. Khử trùng lặp danh xưng vì thế phải có một threshold (ngưỡng tin cậy), và khi chưa đủ tin thì phải dừng để người duyệt quyết, không được lặng lẽ tạo thêm một node mới.

Điểm nghẽn thứ năm là hai nguồn không kể giống nhau. Đại Việt sử ký và Nguyên sử có thể nhấn khác nhau về cùng một trận. Cách làm đúng với sử học là giữ cả hai lời và ghi rõ mỗi lời thuộc sách nào. Việc đó có chỗ trong dự án, ở giai đoạn sau khi kho đã ổn. Đồ án chỉ chuẩn bị: mỗi bản ghi đã xác nhận phải gắn với một nguồn. Chưa tạo quan hệ “hai nguồn đồng thuận” hay “hai nguồn mâu thuẫn”.

Khoảng trống của riêng đồ án, sau khi đặt cạnh những việc người khác đã làm, là một pipeline đo được: từ văn bản tiếng Việt, tới bản ghi chủ thể và quan hệ theo một hệ thống chủ thể và từ khóa, tới một mã duy nhất cho mỗi người, tới knowledge graph, với một gold set, tức tập đoạn văn do người đọc gắn nhãn trước để so. Trung tâm Thư viện và Tri thức số của Đại học Quốc gia Hà Nội đang tính một hạ tầng tri thức cho nhiều ngành trong toàn trường, giai đoạn 2026–2035 [5]. Hướng đó đúng với một thư viện lớn. Nó chưa được cắt riêng cho một tiết Sử. Một công trình khác đã dựng knowledge graph từ chính sách giáo khoa Lịch sử tiếng Việt theo chương trình 2018, bám bố cục sách và giúp tìm đoạn trong sách tốt hơn cách chỉ so câu giống nhau [4]. Việc còn trống là ghi người, sự kiện, nơi, thời gian và nguồn theo các câu hỏi của giờ Sử, nối chúng bằng quan hệ có đoạn trích, và gộp nhiều cách gọi của cùng một người về một node.

## 1.2. Research objectives

Mục tiêu chung: xây dựng và đo một pipeline, trong đó sử liệu tiếng Việt đã có chữ được trích xuất thành bản ghi chủ thể và quan hệ, các danh xưng của cùng một người được gộp lại, và kết quả được nạp vào knowledge graph. Tất cả nằm trong phạm vi đồ án.

Mục tiêu theo từng khối tuần, nói bằng việc phải xong:

- O1, tuần 1 đến tuần 4. Chốt schema của hệ thống chủ thể và từ khóa: tám chủ thể, bộ từ khóa của từng chủ thể, cách đặt mã, các danh mục phân loại, các kiểu quan hệ, và luật mỗi người, mỗi sự kiện, mỗi nơi chỉ có một mã. Mỗi bản ghi dùng trong demo phải gắn với ít nhất một nguồn.

- O2, tuần 5 đến tuần 8. Lập gold set khoảng 150 đến 200 đoạn sử liệu do người đọc gắn nhãn trước: chủ thể nào có mặt, từ khóa nào có giá trị, quan hệ nào nối chúng. Tách riêng phần dùng để tinh chỉnh và phần để đo lần cuối. Dựng bốn API cố định: trích xuất, khử trùng lặp danh xưng, nạp graph, và xem lại một chủ thể cùng các quan hệ của nó. Có tài liệu API để người khác gọi đúng.

- O3, tuần 9 đến tuần 12. Bước trích xuất trả bản ghi chủ thể và quan hệ đúng schema. Kết quả sai schema bị từ chối, không được nạp. Đo độ khớp F1 sơ bộ trên phần dùng để tinh chỉnh.

- O4, tuần 13 đến tuần 16. Khử trùng lặp danh xưng: đủ tin thì gắn vào mã cũ; chưa đủ thì gắn cờ FLAGGED để chờ người duyệt, và lần nạp đã xác nhận không tạo thêm node người mới. Nạp graph theo batch (theo lô). Nạp lại cùng một mã thì cập nhật bản cũ. Giao diện demo cho phép dán chữ, xem kết quả trích xuất, và nạp vào graph.

Các mốc số dưới đây là đích đồ án tự đặt, chưa phải kết quả đã đo. Độ khớp F1 theo từ khóa, so với gold set, từ 85% đến 90%. Độ khớp F1 theo quan hệ, so với gold set, từ 75% đến 85%. Độ khớp F1 là chỉ số gộp hai mặt: giá trị hệ thống trích ra có đúng không, và giá trị đáng có có bị bỏ sót không. Precision của bước khử trùng lặp danh xưng, tức tỷ lệ đúng trong những lần hệ thống tự gộp một danh xưng vào một người, từ 90% đến 95%. Việc trích xuất một trang chữ xong trong khoảng dưới 3 đến 5 giây, trên cấu hình máy được ghi rõ trong báo cáo.

Ba câu hỏi mà báo cáo phải trả lời:

- RQ1. Cách nhà trường đang quản lý sử liệu, và các cách trích xuất sự kiện hiện có, có gì thuận và gì vướng, nhất là với tiếng Việt và với môn Lịch sử phổ thông? Trả lời ở chương 2.

- RQ2. Trong phạm vi đồ án, cách làm nào vừa sức để trích xuất bản ghi chủ thể và quan hệ theo hệ thống chủ thể và từ khóa, khử trùng lặp danh xưng và nạp vào graph? Trả lời ở chương 3 và chương 4.

- RQ3. Đo chất lượng trích xuất và chất lượng khử trùng lặp danh xưng bằng cách nào, để mô hình không tự chấm bài của chính nó? Trả lời ở chương 5.

## 1.3. Scope of the Project

Đồ án nằm trong lộ trình của dự án như bảng sau. Cột cuối nói việc đó có thuộc đồ án hay không.

| Phần | Thời gian | Việc | Thuộc đồ án |
| --- | --- | --- | --- |
| Nửa đầu của kho tư liệu | Tháng 1–4 | Schema chủ thể và từ khóa, ba database, trích xuất, khử trùng lặp danh xưng, nạp graph, demo | Có |
| Nửa sau của kho tư liệu | Tháng 5–8 | Cắt đoạn, semantic search, gắn mã hàng loạt, ghi hai lời kể lệch, hoàn thiện API | Không |
| Phần người học hỏi | Tháng 9–18 | Chatbot hỏi đáp có dẫn nguồn, lọc theo năm và nơi, scaffolding cho người học, thử trên lớp | Không |

Đồ án làm những việc sau.

- Nhận văn bản tiếng Việt đã có sẵn chữ. Nhận dạng chữ trong ảnh (OCR) không thuộc đồ án.

- Kho thí điểm là cụm kháng chiến chống quân Mông - Nguyên, lấy trận Bạch Đằng năm 1288 làm mạch chính, cùng các đoạn sách giáo khoa hoặc sử liệu được phép dùng.

- Dữ liệu theo hệ thống chủ thể và từ khóa, gồm tám chủ thể: con người, tổ chức, sự kiện, nơi chốn, thời gian, hiện vật, kế sách hoặc tư tưởng, và nguồn sử liệu. Các quan hệ chính: chỉ huy, tham gia, ở phía đối địch, diễn ra tại, nằm trong khoảng thời gian, dùng kế sách, để lại di sản, và nguồn nâng đỡ sự kiện (SUPPORTS). Mỗi chủ thể có bộ từ khóa riêng. Đồ án khai báo đủ tám chủ thể, và nạp vào graph những chủ thể mà đoạn chữ thí điểm có nói tới.

- Neo4j, database lưu graph, bắt buộc có dữ liệu demo. ChromaDB, vector database dùng cho semantic search, được dựng sẵn schema và vài bản ghi mẫu, chưa nạp đầy. PostgreSQL là master registry: cấp mã mờ, giữ danh xưng, nguồn và log (`dim_entities`, `entity_aliases`, các lần trích xuất). Neo4j và ChromaDB dùng đúng các mã này.

- Bốn API cố định, gồm các endpoint /extract-5w1h, /resolve-entity, /ingest-graph và /entities/{entity\_id}: trích xuất bản ghi chủ thể và quan hệ, khử trùng lặp danh xưng, nạp graph, xem lại một chủ thể cùng các quan hệ một bước.

- Một giao diện demo đơn giản bằng Streamlit cho người vận hành: dán chữ, xem bảng, nạp vào graph.

Các việc sau thuộc dự án, nhưng không thuộc đồ án.

- Chatbot cho học sinh, ToolPlanner (bộ chọn loại truy vấn cho chatbot), câu hỏi gợi mở, và khảo sát trên lớp thuộc Phase 2 của dự án.

- Cắt đoạn toàn bộ kho và semantic search thuộc phần sau của Phase 1. Mốc thời gian truy vấn dưới hai giây cũng thuộc phần đó.

- Việc tạo quan hệ đồng thuận hoặc mâu thuẫn giữa hai nguồn thuộc cuối Phase 1. Đồ án có node nguồn và quan hệ SUPPORTS, như phần chuẩn bị.

- Đồ án mượn một nguyên tắc của CIDOC CRM, chuẩn mô tả dữ liệu bảo tàng và di sản, là mô tả quá khứ bằng thực thể và quan hệ giữa chúng. Đồ án không dựng đủ chuẩn đó.

- Hệ thống chủ thể và từ khóa không được đổi sang triết, văn, địa hay chính trị trong đồ án.

- Mọi từ khóa và quan hệ do mô hình trích ra chưa được xem là đã đúng. Thiếu đoạn trích thì bản ghi hoặc quan hệ đó ở trạng thái draft.

# 2. Background and Related Work

Chương này trả lời câu hỏi thứ nhất. Nó nói vì sao dữ liệu phải theo cách hỏi của giờ Sử, vì sao thực trạng ở Việt Nam chưa có đúng loại kho mà đồ án làm, và vì sao đồ án chỉ nhận một lát của bài toán lớn.

## 2.1. Tư duy lịch sử và cách chuyển 5W1H thành dữ liệu

Van Drie và van Boxtel mô tả tư duy lịch sử là việc người học sắp thông tin về quá khứ để mô tả, để so sánh, hoặc để giải thích. Việc đó gồm đặt câu hỏi, dùng nguồn, đặt sự kiện vào bối cảnh của nó, lập luận, và dùng khái niệm của ngành [6], [7]. Các công trình sau đó về học tập bằng tìm tòi trong môn Sử cũng nhấn cùng mạch: người học không nhận một bài kể đã xong, mà làm việc với tư liệu [8]. Đây là cơ sở khoa học xã hội của đồ án. Nếu bỏ phần này, hệ thống chỉ còn là một cách cất file.

Cách hỏi quen để một sự kiện đủ thành phần là sáu câu, thường viết tắt 5W1H: cái gì, ai, ở đâu, khi nào, vì sao, và như thế nào. Câu khi nào và ở đâu giữ người kể khỏi kéo sự kiện ra ngoài thời của nó. Câu vì sao và như thế nào nối nguyên nhân với diễn biến. Riêng câu vì sao trong sử cần giữ đúng mức. Đó thường là cách người viết sử giải thích, không phải một ô trống để mô hình tự điền cho đủ. Đồ án chỉ ghi hệ quả khi chính nguồn đã viết hệ quả đó.

Sáu câu chưa đủ để thành một schema ổn định. Mỗi câu hỏi trỏ tới một loại thực thể khác nhau, và mỗi loại cần được mô tả bằng những thông tin riêng. Câu "ai" trỏ tới con người và tổ chức. Câu "việc gì, thế nào" trỏ tới sự kiện. Câu "ở đâu" trỏ tới nơi chốn, câu "khi nào" trỏ tới thời gian. Câu "bằng gì" trỏ tới hiện vật, câu "vì sao, kế gì" trỏ tới kế sách hoặc tư tưởng. Giờ Sử còn hỏi thêm "dựa vào đâu", trỏ tới nguồn sử liệu. Vì vậy đồ án dùng tám chủ thể, mỗi chủ thể có một bộ từ khóa, và nối các chủ thể bằng quan hệ. Từ khóa nào đoạn chữ không nói thì để trống. Để trống là trung thực hơn là viết thêm.

Đã có một hệ thống tên Giveme5W1H, của Hamborg, Breitinger và Gipp, trích xuất sự kiện chính từ tin tức theo các câu hỏi này [9]. Công trình đó cho thấy cách hỏi của phóng viên có thể thành đầu ra có cấu trúc, không chỉ là một đoạn văn. Tin tức và sử liệu không giống nhau. Tin có một bài, một sự kiện nổi, và thời gian gần. Sử có nhiều tên cho một người, thời gian cách xa, và hai sách có thể kể lệch. Đồ án mượn ý “đầu ra có cấu trúc cố định”, không chép hệ thống tin tức tiếng Anh sang sử Việt.

Ví dụ xuyên suốt, chỉ để thiết kế, là trận Bạch Đằng năm 1288. Việc xảy ra là một trận thủy chiến. Người gắn với trận, trong cách thiết kế, gồm Trần Quốc Tuấn và phe đối diện. Nơi là sông Bạch Đằng. Thời là năm 1288. Phần “như thế nào” chỉ lấy những câu nguồn nói, ví dụ đoạn viết về cọc hoặc về thủy triều nếu đoạn đó có. Nếu một đoạn mới chỉ viết “Hưng Đạo Vương”, bản ghi người vẫn phải trỏ về cùng node với “Trần Quốc Tuấn”. Trong thiết kế, người này mang mã P00001. Đó là ví dụ để kiểm, chưa phải kết quả hệ thống đã chạy.

## 2.2. Thực trạng giải pháp tại Việt Nam

Thực trạng được xếp thành bốn nhóm đang có ở Việt Nam. Mỗi nhóm làm đúng một việc. Không nhóm nào làm đúng việc của đồ án.

Nhóm một là phiếu và sơ đồ trên lớp. Ưu điểm là đúng chương trình, ít tốn kém, và giáo viên chọn được đoạn tư liệu đưa cho học sinh. Hạn chế là sản phẩm không dùng lại được sang tiết sau, không đi được nhiều bước quan hệ trong một cuộc kháng chiến dài, và không để lại vết để đo phiếu có bám chữ hay không.

Nhóm hai là thư viện số và phần mềm quản lý tài liệu. Ưu điểm là giữ được tệp gốc và thư mục, tìm lại được cuốn sách. Hạn chế là đơn vị để tra là cuốn hoặc tệp, không phải sự kiện. Học sinh không bắt đầu từ mã kệ sách. Học sinh bắt đầu từ một trận, một người, một năm.

Nhóm ba là hạ tầng tri thức cấp trường. Trung tâm Thư viện và Tri thức số, Đại học Quốc gia Hà Nội, công bố hướng xây một “bộ não số” giai đoạn 2026–2035: cắt đoạn học liệu, semantic search, và dựng knowledge graph để nhiều ngành trong trường cùng tra cứu [5]. Đây là việc của một thư viện lớn, phục vụ cả trường. Đơn vị của họ là đoạn học liệu và mối liên hệ giữa tài liệu. Đơn vị của một tiết Sử là trận, người, năm và nơi. Hai việc có thể nối với nhau sau này. Đồ án không nhận làm hạ tầng cả trường.

Nhóm bốn là knowledge graph dựng từ sách giáo khoa. Một công trình năm 2026 dựng knowledge graph dạng cây từ sách Lịch sử tiếng Việt theo chương trình 2018, khoảng 400 trang, khoảng 750 node và hơn 4.000 quan hệ, và cho thấy truy xuất theo graph này tốt hơn cách chỉ so câu giống nhau [4]. Tín hiệu đáng kể là tiếng Việt và sách sử phổ thông đã được mang vào thử nghiệm. Graph đó bám bố cục sách. Đồ án cần dữ liệu bám câu hỏi của giờ Sử, và cần bước khử trùng lặp danh xưng mà công trình kia không lấy làm việc chính.

Bảng dưới đặt bốn cách cạnh nhau, theo đúng những chỗ thực trạng đang hở.

| Tiêu chí | Phiếu trên lớp | Thư viện số | Knowledge graph từ sách | Đồ án |
| --- | --- | --- | --- | --- |
| Đơn vị ghi | Bảng học sinh điền | Tệp và thông tin bìa sách | Node theo bài hoặc theo cuốn sách | Tám chủ thể có từ khóa, nối bằng quan hệ |
| Nhiều tên một người | Giáo viên hiểu nhờ ngữ cảnh | Không xử lý | Tùy từng cách làm | Có khử trùng lặp danh xưng, và có cờ FLAGGED chờ người duyệt |
| Đo được không | Không có thước đo phiếu | Không sinh ra sự kiện | Có thử nghiệm truy xuất đoạn | Độ khớp F1 theo từ khóa và theo quan hệ, precision của bước khử trùng lặp danh xưng |
| Học sinh hỏi hệ thống | Hỏi tại lớp, với giáo viên | Không phải việc của thư viện | Không phải đích của công trình kia | Thuộc giai đoạn sau của dự án, không làm trong đồ án |

## 2.3. Hướng kỹ thuật và lựa chọn cho đồ án

Phần này giải thích, bằng lời thường, vì sao vài hướng kỹ thuật phổ biến chưa phải sản phẩm của đồ án.

Keyword search, tức tìm theo đúng một chuỗi chữ, thì ổn khi người dùng biết sẵn chữ đó viết thế nào trong sách. Sử liệu có tên cổ, địa danh đổi cách gọi, và câu hỏi của học sinh không phải một từ khóa. Đồ án vẫn giữ nguyên chuỗi gốc để đối chiếu. Việc gộp “Hưng Đạo Vương” về “Trần Quốc Tuấn” không thể trông vào keyword search.

Một hướng khác là semantic search: tìm đoạn văn gần nghĩa với câu hỏi, rồi để LLM viết câu trả lời dựa trên đoạn tìm được. Hướng này gọi là RAG (Retrieval-Augmented Generation) [3]. Một bước xa hơn là GraphRAG: dựng knowledge graph, tóm tắt từng cụm, rồi mới sinh câu trả lời [10]. Cả hai đều có ích khi người học bắt đầu hỏi. Chúng thuộc nửa sau của kho tư liệu và thuộc phần hỏi đáp. Làm chúng trong đồ án thì chưa biết câu trả lời sai vì mô hình tự thêm, hay vì dữ liệu trong kho đã sai từ đầu.

PhoBERT là một mô hình ngôn ngữ đã huấn luyện sẵn cho tiếng Việt [11]. Nó tạo được embedding cho câu và tên người, tức biểu diễn chữ thành một dãy số để so độ gần nghĩa. Đồ án có thể dùng loại mô hình này ở bước xem hai danh xưng có gần nhau không. Nó không phải nơi lưu dữ kiện. Dữ kiện nằm ở bản ghi chủ thể và quan hệ trên graph, kèm đoạn trích.

Khử trùng lặp danh xưng trong đồ án bắt đầu bằng master registry. Bước một, tra bảng `entity_aliases` trên PostgreSQL, có chỉ mục tên và trigram. Khớp chắc thì lấy mã đã cấp. Bước hai, với ứng viên chưa chắc, đo string similarity, tức độ giống nhau giữa hai chuỗi chữ. Threshold khởi điểm là khoảng 82%. Con số này là giả định để bắt đầu, chưa phải hằng số đã chứng minh, và sẽ được tinh chỉnh trên gold set. Bước ba, so embedding của danh xưng cùng một câu ngữ cảnh để xếp hạng. Dưới threshold thì gắn FLAGGED chờ người duyệt, không tự tạo mã mới. Các ca này không bị tính là gộp sai, vì hệ thống đã không tự quyết.

Vì sao đồ án chưa làm chatbot cho học sinh. Chatbot cần các node trên graph đã ổn, và cần các đoạn chữ đã gắn mã. Nếu mở chatbot trước khi đo được bước trích xuất, một câu trả lời sai không tách được hai nguyên nhân: mô hình tự thêm, hoặc bản ghi và quan hệ nạp vào kho đã sai. Đồ án chọn đo kho trước.

# 3. Proposed Solution

Giải pháp là một backend, tên làm việc là HistoryDistill, làm nhiệm vụ trích xuất sử liệu theo hệ thống chủ thể và từ khóa rồi nạp vào graph. Người chạy demo dán một đoạn chữ, xem các bản ghi chủ thể và quan hệ vừa trích ra, rồi nạp vào graph. Không có tài khoản học sinh trong đồ án.

## 3.1. Solution Description

Giải pháp dựa trên một hệ thống chủ thể và từ khóa. Hệ thống này nói trong một đoạn sử liệu cần nhận ra những loại thực thể nào, mỗi loại được mô tả bằng những thông tin nào, và các thực thể nối với nhau bằng quan hệ gì. Tám chủ thể đã cố định:

| Câu hỏi | Chủ thể | Ví dụ trong trận Bạch Đằng | Mã ví dụ |
| --- | --- | --- | --- |
| Ai | Con người | Trần Quốc Tuấn | P00001 |
| Ai, phe nào | Tổ chức, thể chế | Triều Trần, quân Nguyên | GRP\_TRIEU\_TRAN, GRP\_QUAN\_NGUYEN |
| Việc gì, thế nào | Sự kiện | Trận Bạch Đằng năm 1288 | EV00001 |
| Ở đâu | Nơi chốn | Sông Bạch Đằng | LOC\_SONG\_BACH\_DANG |
| Khi nào | Thời gian | Năm 1288, năm Mậu Tý | TIME\_1288\_MAU\_TY |
| Bằng gì | Hiện vật, di sản | Bãi cọc Yên Giang | ART\_BAI\_COC\_YEN\_GIANG |
| Vì sao, kế gì | Kế sách, tư tưởng | Cọc ngầm kết hợp thủy triều | STRAT\_COC\_NGAM\_THUY\_TRIEU |
| Dựa vào đâu | Nguồn sử liệu | Toàn thư, Nguyên sử | SRC\_TOAN\_THU\_NGO\_SI\_LIEN, SRC\_NGUYEN\_SU |

Mỗi chủ thể có một bộ từ khóa, tức các thuộc tính dùng để mô tả và tra cứu. Một người có tên chính, các danh xưng khác, vai trò, năm sinh và năm mất. Một sự kiện có tên, loại, mốc đầu và mốc cuối, tóm tắt diễn biến, kết quả và ý nghĩa nếu nguồn có viết. Một địa danh có tên thời xưa và tên ngày nay. Một nguồn có tác giả, thời điểm biên soạn, góc nhìn và đoạn trích. Bộ từ khóa có thể đổi khi làm dữ liệu thật, nên đồ án không cố định số lượng từ khóa. Tám chủ thể thì giữ nguyên.

Hệ thống đi kèm ba quy chuẩn. Thứ nhất, mã là khóa mờ do PostgreSQL cấp qua sequence: `P` và `EV` kèm năm chữ số, các chủ thể còn lại kèm bốn chữ số. Mã không chứa tên, danh xưng hay năm. Năm sinh và năm sự kiện là thuộc tính, vì các nguồn có thể ghi lệch. Thứ hai, mỗi chủ thể có một danh mục phân loại đóng, chẳng hạn loại sự kiện hay vai trò của một người. Mô hình trả một nhãn nằm ngoài danh mục thì kết quả bị từ chối. Thứ ba, mỗi node có trường để ghi mã ở các kho tri thức mở như Wikidata, GeoNames hoặc VIAF. Các trường này được phép trống, và chỉ được điền khi người làm đã tự tra. Mô hình không được đoán mã và không được tự đặt mã định danh.

Các chủ thể nối với nhau bằng một danh sách quan hệ đã chốt: chỉ huy (COMMANDED), tham gia (PARTICIPATED\_IN), ở phía đối địch (OPPOSED\_IN), diễn ra tại (TOOK\_PLACE\_AT), nằm trong khoảng thời gian (OCCURRED\_DURING), dùng kế sách (EMPLOYED\_STRATEGY), để lại di sản (LEFT\_HERITAGE), và nguồn nâng đỡ (SUPPORTS). Mỗi quan hệ chỉ nối đúng cặp chủ thể của nó, ví dụ chỉ huy đi từ một người tới một sự kiện. Quan hệ nối sai cặp chủ thể thì bị từ chối.

Đồ án giữ bốn ràng buộc để graph không đi ngược sử học. Một người không thể tham gia một sự kiện trước khi sinh hoặc sau khi mất; gặp trường hợp này thì quan hệ đó bị gắn cờ FLAGGED. Mỗi địa danh thời xưa có trường tên ngày nay, do người làm điền tay. Mọi bản ghi đã xác nhận phải có ít nhất một nguồn. Một người nhiều tên vẫn chỉ là một node. Việc giữ cạnh nhau hai lời kể lệch nhau thuộc cuối Phase 1, không làm trong đồ án.

Pipeline chính có bốn bước. Mỗi bước tương ứng một mục tiêu đã nêu.

- Tiếp nhận. Người dùng đưa vào một đoạn chữ tiếng Việt, kèm mã của nguồn (source\_id) và tên tệp. PostgreSQL lưu bản gốc và một mã hash của văn bản, để lần sau đưa lại đúng đoạn đó thì không tạo thêm một nguồn trùng.

- Trích xuất. LLM trả về hai danh sách theo schema: các bản ghi chủ thể mà đoạn chữ có nói tới, và các quan hệ giữa chúng. Mỗi từ khóa của một bản ghi hoặc có giá trị, hoặc để trống. Với từ khóa có giá trị và với mỗi quan hệ, mô hình phải chỉ ra đoạn trích và vị trí đoạn đó trong bản gốc, tính bằng thứ tự ký tự. Kết quả sai schema bị từ chối, không được nạp vào graph. Bước này chưa cấp mã cuối.

- Khử trùng lặp danh xưng. Hệ thống tra bảng `entity_aliases` trên PostgreSQL, có chỉ mục trigram. Khớp thì dùng mã đã có. Chưa đủ chắc thì gắn `FLAGGED`, và lần nạp đã xác nhận sẽ không tạo thêm node người hoặc nơi mới. Thực thể mới chỉ nhận mã do sequence cấp. Embedding chỉ để xếp hạng ứng viên. Người chạy demo có thể xác nhận tay trước khi nạp.

- Nạp graph. Bản ghi và quan hệ đã có mã được nạp theo batch. Cùng một mã thì bản ghi cũ được cập nhật, không sinh thêm một node trùng. Bản ghi hoặc quan hệ thiếu đoạn trích được nạp ở trạng thái draft và không có quan hệ SUPPORTS. Bản ghi đã xác nhận phải có quan hệ đó tới ít nhất một nguồn.

Bốn bước này khóa bốn mục tiêu. Schema của hệ thống chủ thể và từ khóa khóa O1. Gold set và bốn API khung khóa O2. Bước trích xuất khóa O3. Khử trùng lặp danh xưng, cách nạp không nhân đôi, và giao diện demo khóa O4.

Ví dụ dưới đây chỉ để thấy hình dạng kết quả trích xuất của một đoạn về trận Bạch Đằng năm 1288. Các giá trị là thiết kế, không phải kết quả mô hình đã chạy.

| Chủ thể | Mã | Một số từ khóa có giá trị |
| --- | --- | --- |
| Sự kiện | EV00001 | Tên: Trận Bạch Đằng năm 1288. Loại: MilitaryBattle. Mốc đầu: năm 1288. Mốc cuối: để trống nếu đoạn chữ không nói |
| Con người | P00001 | Tên chính: Trần Quốc Tuấn. Danh xưng gặp trong đoạn: Hưng Đạo Vương |
| Tổ chức | GRP\_QUAN\_NGUYEN | Tên: quân Nguyên. Loại: MilitaryForce |
| Nơi chốn | LOC\_SONG\_BACH\_DANG | Tên lịch sử: sông Bạch Đằng. Loại: Battlefield |
| Kế sách | STRAT\_COC\_NGAM\_THUY\_TRIEU | Tên: cọc ngầm kết hợp thủy triều, chỉ khi đoạn chữ có nói |
| Nguồn | SRC\_TOAN\_THU\_NGO\_SI\_LIEN | Tên: Đại Việt sử ký toàn thư. Đoạn trích và vị trí |

| Quan hệ | Từ | Tới |
| --- | --- | --- |
| COMMANDED | P00001 | EV00001 |
| OPPOSED\_IN | GRP\_QUAN\_NGUYEN | EV00001 |
| TOOK\_PLACE\_AT | EV00001 | LOC\_SONG\_BACH\_DANG |
| EMPLOYED\_STRATEGY | EV00001 | STRAT\_COC\_NGAM\_THUY\_TRIEU |
| SUPPORTS | SRC\_TOAN\_THU\_NGO\_SI\_LIEN | EV00001 |

Quy tắc đọc hai bảng này: mô hình không được điền kết quả hay ý nghĩa của trận nếu đoạn chữ không viết. Hệ thống không được tạo một node người thứ hai chỉ vì gặp tên Hưng Đạo Vương. Từ khóa hoặc quan hệ nào không chỉ được câu nguồn thì ở trạng thái DRAFT.

## 3.2. Software Architecture

Kiến trúc vừa sức một người làm trong đồ án. Cả hệ thống là một ứng dụng monolith, tức một khối chương trình duy nhất có ranh giới rõ giữa các module, không tách thành nhiều microservice.

Người vận hành dùng giao diện demo Streamlit. Phía sau là lớp API viết bằng FastAPI, với đúng bốn endpoint đã nêu. Phần xử lý gồm ba bước nối tiếp: trích xuất, khử trùng lặp danh xưng, nạp graph. Phần dữ liệu gồm ba database. Neo4j lưu knowledge graph, bắt buộc có dữ liệu demo, khóa node lấy từ master registry. PostgreSQL cấp mã, giữ nguồn, bản chữ gốc, các lần chạy, `dim_entities`, `entity_aliases` và log. ChromaDB là vector database, chỉ dựng sẵn cùng vài bản ghi mẫu. Ba database chạy cùng nhau bằng Docker Compose, để máy khác chạy lại được khi bảo vệ.

Trong demo, dữ liệu đi một chiều: vào PostgreSQL, qua bước trích xuất, qua khử trùng lặp danh xưng, rồi nạp vào Neo4j. Giao diện đọc lại các chủ thể vừa nạp để người xem thấy các quan hệ. ChromaDB không nằm trên đường đi bắt buộc của demo. Nhờ vậy demo vẫn chạy khi vector database còn trống.

Mỗi lần trích xuất và mỗi lần nạp đều ghi log: tên mô hình đã dùng, thời điểm, đường dẫn tệp kết quả và trạng thái thành công hay lỗi. Báo cáo nhờ đó nói được số đo thuộc lần chạy nào. Nếu giữa chừng đổi mô hình, các lần chạy không bị trộn vào một con số.

## 3.3. Technology and Tools Used

Bảng dưới ghi công nghệ sẽ dùng. Cột cuối nói vai trò bằng lời thường. Người đọc không cần biết cách cài. Tên công nghệ giữ lại để hội đồng và người thực hiện dùng chung một danh sách với bản kỹ thuật.

| Việc trong đồ án | Công nghệ | Vai trò |
| --- | --- | --- |
| Backend, API và schema | Python 3.12, FastAPI, Pydantic | Phiếu sai schema bị từ chối. Có tài liệu API. |
| Graph database | Neo4j 5 | Mỗi mã chỉ một node. Nạp lại thì cập nhật, không nhân đôi. Xem trực quan được. |
| Vector database | ChromaDB | Dựng trong đồ án, chưa nạp đầy. |
| Sổ đăng bạ, nguồn và log | PostgreSQL 16 | Cấp mã mờ, tra danh xưng, giữ bản gốc và các lần chạy. |
| Trích xuất | LLM có structured output (đầu ra theo schema) | Có thể đổi mô hình vì schema không đổi. Tên mô hình ghi trong báo cáo. |
| So danh xưng | Embedding model tiếng Việt | Chỉ để xếp hạng ứng viên trong khử trùng lặp danh xưng, không dùng để điền từ khóa. |
| Giao diện demo | Streamlit | Đủ ba thao tác: dán chữ, xem kết quả trích xuất, nạp graph. |
| Triển khai và quản lý mã | Docker Compose, Git | Ba database chạy cùng nhau. Source code có lịch sử thay đổi. |

Dữ liệu có hai phần, tách khỏi nhau. Phần kho thí điểm là các đoạn về cụm Bạch Đằng và kháng chiến chống quân Mông - Nguyên, văn bản đã làm sạch, nguồn ghi trong PostgreSQL. Phần gold set khoảng 150 đến 200 đoạn sử liệu do người đọc gắn nhãn trước, không phải do mô hình tự gán nhãn cho chính nó. Gold set lại tách đôi: dev set để tinh chỉnh threshold, và test set để đo lần cuối. Test set không được dùng để tinh chỉnh.

Ràng buộc trên graph được tạo trong bốn tuần đầu. Mã của mọi chủ thể là duy nhất và theo cách đặt mã đã nêu ở mục 3.1. Loại sự kiện thuộc một danh mục đóng gồm bảy loại: trận đánh (MilitaryBattle), cải cách chính trị (PoliticalReform), ngoại giao (Diplomacy), văn hóa và tôn giáo (CulturalReligious), khởi nghĩa và nổi dậy (UprisingRebellion), mốc trong đời một người (PersonalMilestone), kinh tế và xã hội (SocioEconomicEvent). Các chủ thể khác cũng có danh mục phân loại riêng, như vai trò của một người hay loại nơi chốn. Có thể bổ sung giá trị vào các danh mục trước tuần 8 nếu kho thí điểm cần. Sau tuần 8 các danh mục đóng, để các lần đo nói về cùng một schema.

PostgreSQL tối thiểu có các bảng: `dim_entities`, `entity_aliases` (kèm chỉ mục trigram), `source_documents`, bản chữ gốc, lần trích xuất, và log nạp. Trạng thái kiểm duyệt là `DRAFT`, `VERIFIED`, `FLAGGED`. Bảng người dùng và bảng log học tập thuộc phần hỏi đáp, không tạo trong đồ án.

# 4. Project Plan

Đồ án chia tám sprint, mỗi sprint hai tuần, tổng mười sáu tuần. Ưu tiên có một pipeline chạy được từ đầu đến cuối ở cuối tháng thứ ba. Tháng thứ tư mới đo và siết khử trùng lặp danh xưng. Chatbot cho học sinh không được mở khi bước trích xuất chưa đo.

## 4.1. Main development stages

| Sprint | Tuần | Việc chính | Xong khi |
| --- | --- | --- | --- |
| 1–2 | 1–4 | Chốt schema của hệ thống chủ thể và từ khóa, danh mục phân loại, kiểu quan hệ, dựng ba database | Schema chạy, và ràng buộc mã duy nhất trên graph chạy |
| 3–4 | 5–8 | Gold set, bốn API khung, tài liệu API | Có tệp nhãn và bốn endpoint gọi được |
| 5–6 | 9–12 | Trích xuất và nạp graph không nhân đôi | Một đoạn thành các node chủ thể và edge trên graph. Nạp lại không sinh thêm node |
| 7–8 | 13–16 | Khử trùng lặp danh xưng tự động, giao diện demo, đo trên test set | Demo chạy, và có bảng độ khớp F1 cùng precision |

Tháng thứ ba được phép nạp graph với tên đã chuẩn hóa bằng tay, nếu khử trùng lặp danh xưng tự động chưa ổn. Tháng thứ tư mới bật chế độ tự động. Không tạo hàng loạt node trùng rồi mới gộp sau, vì khi đó precision không còn đo trên cùng một cách làm với demo. Khử trùng lặp danh xưng phải chạy trước lệnh tạo node người mới.

Bốn khối việc tương ứng bốn cặp sprint: schema và database; gold set và API; trích xuất và nạp graph; khử trùng lặp danh xưng và đo.

## 4.2. Expected schedule

Bốn mốc. Hết tuần 4, schema đóng ở mức đủ demo. Hết tuần 8, dev set của gold set đã có. Hết tuần 12, demo nội bộ chạy được với tên chuẩn hóa tay. Hết tuần 16, demo trước hội đồng và báo cáo số đo.

| Hạng mục | Tuần 1–4 | Tuần 5–8 | Tuần 9–12 | Tuần 13–16 |
| --- | --- | --- | --- | --- |
| Schema và database | Làm | Chốt nốt |  |  |
| Gold set và API |  | Làm | Dùng để tinh chỉnh |  |
| Trích xuất và nạp graph |  |  | Làm | Siết |
| Khử trùng lặp danh xưng và đo |  |  | Chuẩn bị | Làm |

Các tháng từ tháng 5 đến tháng 18 không có việc trong lịch của đồ án. Chúng được ghi ở chương 1 để thấy kho này sẽ nối vào đâu. Đó không phải cam kết bàn giao của đồ án.

## 4.3. Feasibility Assessment

Việc làm được trong mười sáu tuần vì các công nghệ graph database, API và kiểm schema đã ổn định, và vì kho thí điểm nhỏ: một cụm sự kiện, không phải toàn bộ chính sử. Một người làm được nếu giữ đúng phạm vi đồ án và không mở chatbot.

Rủi ro và cách giảm:

| Mã | Rủi ro | Mức | Cách xử lý |
| --- | --- | --- | --- |
| R1 | Mô hình bỏ sót thực thể, từ khóa hoặc quan hệ đáng có, hoặc trích ra những thứ không có trong chữ | Cao | Kết quả sai schema bị từ chối. Từ khóa hoặc quan hệ không có đoạn trích thì ở trạng thái draft. |
| R2 | Gộp nhầm hai người thành một | Cao | Threshold tinh chỉnh trên dev set. Dưới threshold thì gắn cờ FLAGGED. |
| R3 | Thiếu đoạn chữ được phép dùng | Trung bình | Kho thí điểm nhỏ. Gold set ưu tiên sách giáo khoa và đoạn đã có quyền sử dụng. |
| R4 | Phạm vi phình sang chatbot | Trung bình | Demo chỉ có ba bước. Giao diện không có ô chat. |
| R5 | Đổi mô hình giữa chừng khiến các số không so được | Trung bình | Mỗi lần chạy ghi tên mô hình vào log. Báo cáo cuối chỉ dùng một cấu hình. |

Về phần cứng: cần đủ RAM để Neo4j và PostgreSQL chạy cùng lúc. Nếu LLM được gọi qua API bên ngoài, API key không được đưa vào repository công khai. Không cần GPU nếu bước so danh xưng chỉ dùng embedding model nhỏ.

# 5. Evaluation Plan

Cách đánh giá trả lời câu hỏi thứ ba. Có ba chỉ số chính và một chỉ số thời gian. Không có chỉ số hài lòng của học sinh, vì đồ án chưa có người học dùng hệ thống.

## 5.1. Expected Results

Những gì bàn giao khi hết tuần 16:

- Source code, bốn API, cấu hình Docker Compose cho ba database, và hướng dẫn chạy.

- Neo4j đã nạp cụm thí điểm, xem được các quan hệ một bước.

- PostgreSQL đã có master registry, danh xưng, nguồn và log.

- Giao diện demo: dán chữ, xem kết quả trích xuất, nạp graph, và thấy một danh xưng đã biết đi vào đúng node cũ.

- Gold set khoảng 150 đến 200 đoạn sử liệu do người gắn nhãn, cùng báo cáo độ khớp F1, precision và thời gian.

- Tài liệu API cho bốn endpoint.

Đích số trên test set, không dùng tập này để tinh chỉnh threshold:

| Chỉ số | Cách tính bằng lời thường | Đích |
| --- | --- | --- |
| Độ khớp F1 theo từ khóa | So từng từ khóa của từng bản ghi chủ thể với gold set. Từ khóa có giá trị phải kèm đoạn trích đúng. Báo cáo riêng từng chủ thể, rồi lấy trung bình. | 85% đến 90% |
| Độ khớp F1 theo quan hệ | So từng quan hệ, gồm mã đầu, loại quan hệ và mã cuối, với gold set. Quan hệ phải kèm đoạn trích đúng. | 75% đến 85% |
| Precision của bước khử trùng lặp danh xưng | Chỉ tính những danh xưng hệ thống tự gắn vào một mã, và mã đó đúng. | 90% đến 95% |
| Thời gian trích xuất | Từ lúc nhận chữ tới lúc có kết quả trích xuất đúng schema. | Dưới 3 đến 5 giây mỗi trang |

Nếu độ khớp F1 thấp hơn đích, báo cáo vẫn hợp lệ khi có bảng lỗi theo từng chủ thể, từng loại quan hệ, và phần phân tích nguyên nhân. Đích là mốc phấn đấu trong đề cương, không phải điều kiện để được phép nộp số thật.

Ca demo bắt buộc: một đoạn mới có cách gọi Hưng Đạo Vương phải trỏ đúng node đã có của Trần Quốc Tuấn, P00001, không sinh thêm node người thứ hai. Nạp lại cùng một đoạn thì số node trên graph không tăng.

## 5.2. Evaluation method

Gold set do người gắn nhãn trước lần đo cuối. Người gắn nhãn đọc đoạn chữ và ghi ra các chủ thể có mặt, mã của từng chủ thể, các từ khóa có giá trị, và các quan hệ giữa chúng. Khi gắn nhãn cho test set, người gắn không nhìn kết quả do mô hình vừa trích xuất. Bộ từ khóa dùng để đo được chốt cùng các danh mục phân loại sau tuần 8, để mọi lần đo nói về cùng một schema.

Độ khớp F1 theo từ khóa tính trên từng cặp gồm một bản ghi chủ thể và một từ khóa của nó. Từ khóa để trống đúng ở cả nhãn và kết quả mô hình thì không tính vào phép đo. Mô hình trích ra giá trị trong khi nhãn để trống thì tính là thừa. Nhãn có giá trị mà mô hình để trống, hoặc bỏ sót cả bản ghi, thì tính là sót. Một giá trị đúng ý nhưng không kèm đoạn trích không được tính là khớp. Số đo được báo cáo riêng cho từng chủ thể, để thấy chủ thể nào khó trích nhất.

Độ khớp F1 theo quan hệ tính trên từng quan hệ. Một quan hệ khớp khi đúng mã đầu, đúng loại quan hệ, đúng mã cuối, và có đoạn trích đúng. Vì mã đầu và mã cuối phải đúng, chỉ số này chịu ảnh hưởng của cả bước khử trùng lặp danh xưng. Bản ghi và quan hệ ở trạng thái draft không được trình như dữ liệu đã kiểm.

Precision của bước khử trùng lặp danh xưng chỉ tính trên các danh xưng hệ thống tự gắn. Các ca FLAGGED không tính vào mẫu số, vì hệ thống đã không tự quyết. Recall, tức tỷ lệ danh xưng đáng gộp mà hệ thống gộp được, được báo cáo thêm và không nằm trong đích bắt buộc. Bỏ sót rồi nhờ người duyệt vẫn an toàn hơn là gộp nhầm.

Thời gian đo trên các trang có độ dài ghi rõ, cùng một cấu hình mô hình, chạy ít nhất một vòng. Báo cáo lấy giá trị trung vị (median), không lấy trang ngắn nhất.

Đồ án không chấm chất lượng câu trả lời của chatbot cho học sinh, vì đồ án không làm chatbot.

# References

[1] Bộ Giáo dục và Đào tạo, Chương trình giáo dục phổ thông môn Lịch sử, ban hành kèm Thông tư số 32/2018/TT-BGDĐT ngày 26 tháng 12 năm 2018.

[2] Tài liệu tập huấn môn Lịch sử trong Chương trình giáo dục phổ thông 2018, Trường Đại học Sư phạm Hà Nội.

[3] P. Lewis et al., “Retrieval-augmented generation for knowledge-intensive NLP tasks,” Advances in Neural Information Processing Systems, 2020.

[4] Automated tree knowledge graph construction using ontology expansion and retrieval from Vietnamese history textbooks, arXiv:2609.00763, 2026.

[5] Trung tâm Thư viện và Tri thức số, Đại học Quốc gia Hà Nội, “VNU-LIC AI Digital Brain: nền tảng tri thức của đại học tinh hoa VNU 2026–2035.”

[6] J. van Drie and C. van Boxtel, “Historical reasoning: Towards a framework for analyzing students’ reasoning about the past,” Educational Psychology Review, vol. 20, no. 2, pp. 87–110, 2008.

[7] C. van Boxtel and J. van Drie, “Historical reasoning: Conceptualizations and educational applications,” in The Wiley International Handbook of History Teaching and Learning, 2018.

[8] C. van Boxtel, M. Voet, and G. Stoel, “Inquiry learning in history,” in International Handbook of Inquiry and Learning, Routledge, 2021.

[9] F. Hamborg, C. Breitinger, and B. Gipp, “Giveme5W1H: A universal system for extracting main events from news articles,” arXiv:1909.02766, 2019.

[10] D. Edge et al., “From local to global: A GraphRAG approach to query-focused summarization,” arXiv:2404.16130, 2024.

[11] D. Q. Nguyen and A. T. Nguyen, “PhoBERT: Pre-trained language models for Vietnamese,” Findings of EMNLP, 2020, pp. 1037–1042.
