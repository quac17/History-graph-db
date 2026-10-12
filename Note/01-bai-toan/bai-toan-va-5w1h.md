# Bài toán và schema 5W1H

Người thực hiện: Trần Việt Hoàng. MSSV: 25MSA13219.

## Bài toán

Cho một đoạn sử liệu tiếng Việt đã có chữ (không OCR trong đồ án) và một câu hỏi tự nhiên về sự kiện, hệ thống sau này phải trả lời bằng dữ kiện đã trích xuất, mở được đoạn nguồn, và không thêm nhân vật, năm, quan hệ không có trong kho.

Đồ án chỉ làm phần tạo kho đó: văn bản thô thành bản ghi chủ thể và quan hệ theo hệ thống chủ thể và từ khóa, khử trùng lặp danh xưng, nạp vào Neo4j. Hỏi đáp cho học sinh thuộc Phase 2.

Ba điểm nghẽn, đúng proposal đồ án và proposal dự án:

1. LLM thương mại hay lệch niên đại và nhân vật vì không có mỏ neo trong kho sử liệu.
2. Zotero, DSpace, Primo giữ metadata của cuốn tài liệu. Chúng không trả lời ai đánh trận nào, ở đâu, bằng cách nào.
3. Cùng một sự kiện có nhiều nguồn không nói giống nhau, ví dụ Đại Việt sử ký toàn thư và Nguyên sử về Bạch Đằng 1288. Database phẳng thường giữ một dòng và bỏ dòng kia.

Bối cảnh sư phạm là Chương trình giáo dục phổ thông 2018 môn Lịch sử, Thông tư 32/2018/TT-BGDĐT. Năng lực môn gồm tìm hiểu lịch sử, nhận thức và tư duy lịch sử, vận dụng. 5W1H trên lớp hiện nằm ở phiếu và slide, hệ thống không giữ mạng sự kiện để hỏi tiếp.

Ví dụ Zotero không làm được: trong các PDF đã lưu, ai tham gia trận Bạch Đằng 1288, cọc gỗ dùng thế nào, vì sao thủy quân đối phương bất lợi. Zotero không có thực thể bên trong tệp.

## 5W1H không phải sáu trường rời

| Câu hỏi | Trong sử học | Bạch Đằng 1288 |
| --- | --- | --- |
| What | Sự kiện là gì | Trận thủy chiến trên sông Bạch Đằng |
| Who | Ai chỉ huy, ai đối diện | Trần Quốc Tuấn, vua Trần Nhân Tông; tướng nhà Nguyên |
| Where | Diễn ra ở đâu | Sông Bạch Đằng, Quảng Ninh - Hải Phòng |
| When | Khung thời gian | Năm 1288, kháng chiến lần thứ ba |
| Why | Bối cảnh, nguyên nhân được nguồn nêu | Thế trận và vấn đề lương thảo, đường rút |
| How | Cách diễn ra và kết quả | Cọc gỗ, thủy triều, nhử thuyền |

When và Where giữ người học khỏi kể sự kiện ngoài thời của nó. Why và How nối nguyên nhân với diễn biến. Why là diễn giải có nguồn, không phải trường để mô hình tự viết.

Các thao tác người học cần, theo van Drie và van Boxtel: đặt câu hỏi, dùng nguồn, đặt vào bối cảnh, lập luận, dùng khái niệm nội dung. Ba thao tác proposal Phase 2 nhắc lại là sourcing, contextualization, corroboration. Đồ án chưa dạy các thao tác đó. Đồ án tạo dữ liệu để Phase 2 dạy được.

## Từ 5W1H sang chủ thể và từ khóa

Schema không còn là phiếu sự kiện mười trường. Mỗi câu hỏi 5W1H trỏ tới một hoặc vài chủ thể trong `he-thong-chu-the-va-tu-khoa.md`:

| Câu hỏi | Chủ thể | Label |
| --- | --- | --- |
| Who | Con người, tổ chức | `:Person`, `:Group` |
| What, How | Sự kiện | `:Event` |
| Where | Không gian | `:Place` |
| When | Thời gian | `:TimeSpan` |
| What, means | Hiện vật | `:Artifact` |
| Why, strategy | Kế sách, tư tưởng | `:Concept` |
| Evidence | Nguồn | `:Source` |

Kết quả trích xuất của một đoạn:

- `entities`: bản ghi chủ thể mà đoạn chữ có nói tới. Mỗi bản ghi có label, mã, trường phân loại và từ khóa của chủ thể đó. Ví dụ bản ghi `:Event` có tên, loại, mốc đầu và mốc cuối, độ chính xác niên đại, tóm tắt diễn biến, kết quả tức thời, ý nghĩa lâu dài.
- `relations`: quan hệ giữa các mã, theo danh sách edge ở mục dưới.

Từ khóa nguồn không nói thì null. Không điền cho đủ. Kết quả và ý nghĩa của sự kiện chỉ ghi khi nguồn có viết, không phải lời bình của mô hình. Mỗi từ khóa có giá trị và mỗi quan hệ phải kèm đoạn trích.

## Chủ thể và edge

Node theo hệ thống chủ thể và từ khóa ở `he-thong-chu-the-va-tu-khoa.md`. Tám chủ thể: `:Person`, `:Group`, `:Event`, `:Place`, `:TimeSpan`, `:Artifact`, `:Concept`, `:Source`. Node `:Assertion` là node phụ cho dị bản ở cuối Phase 1.

Edge dùng trong đồ án:

- `(:Person)-[:COMMANDED]->(:Event)`
- `(:Person)-[:PARTICIPATED_IN]->(:Event)`
- `(:Person)-[:OPPOSED_IN]->(:Event)`
- `(:Event)-[:TOOK_PLACE_AT]->(:Place)`
- `(:Event)-[:OCCURRED_DURING]->(:TimeSpan)`
- `(:Event)-[:EMPLOYED_STRATEGY]->(:Concept)`
- `(:Event)-[:LEFT_HERITAGE]->(:Artifact)`
- `(:Source)-[:SUPPORTS]->(:Event)` kèm thuộc tính đoạn trích và trang

Edge giữa người và tổ chức, như đứng đầu hoặc phụng sự, chốt tên ở sprint 1–2.

Edge của phần sau Phase 1, không bắt buộc trong đồ án:

- `(:Source)-[:ASSERTS]->(:Assertion)`
- `(:Assertion)-[:CORROBORATES]->(:Assertion)`
- `(:Assertion)-[:CONTRADICTS {aspect}]->(:Assertion)`

CIDOC CRM (ISO 21127) chỉ được mượn nguyên tắc mô tả quá khứ bằng thực thể và quan hệ. Đồ án không hiện thực đủ mọi lớp CIDOC.

## Kho thí điểm

Kháng chiến chống quân Mông - Nguyên, trọng tâm trận Bạch Đằng 1288. Văn bản đầu vào đã làm sạch, ưu tiên sách giáo khoa Lịch sử theo chương trình 2018 và đoạn sử liệu được phép dùng. Không nhận ảnh hay OCR trong đồ án.

Danh xưng phải gộp về một mã: `Trần Quốc Tuấn`, `Trần Hưng Đạo`, `Hưng Đạo Vương`, `Hưng Đạo Đại Vương`, `Tiết chế Quốc công` cùng trỏ `P00001`.
