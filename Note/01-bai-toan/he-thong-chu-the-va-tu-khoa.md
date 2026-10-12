# Hệ thống chủ thể và từ khóa

Người thực hiện: Trần Việt Hoàng. MSSV: 25MSA13219.

File gốc, đọc khi cần bảng đầy đủ:

- `Note/thiet-ke-dinh-danh-va-bo-tri-csdl-da-mau.docx`, bản làm việc `Note/thiet-ke-dinh-danh.md`: mã định danh mờ và vai trò PostgreSQL, Neo4j, ChromaDB.
- `Note/danh-muc-tu-khoa-chu-the-lich-su-v2.docx`: danh mục phân loại đóng, thuộc tính từng chủ thể, JSON schema. Mã trong file này kiểu ghép tên và năm thì không dùng nữa.
- `Note/he-thong-chu-the-va-mang-luoi-quan-he-lich-su.docx`: mô tả bằng lời thường, nhóm quan hệ, ràng buộc.

Hệ thống có tám chủ thể. Tám chủ thể này đã cố định. Mỗi chủ thể đi kèm một bộ từ khóa, tức các thuộc tính dùng để mô tả và tra cứu. Bộ từ khóa có thể thêm hoặc bớt khi làm dữ liệu thật, nên note này gọi chung là hệ thống chủ thể và từ khóa, không ghi số lượng từ khóa.

## Tám chủ thể

| Câu hỏi | Chủ thể | Label | Mẫu mã | Trường phân loại |
| --- | --- | --- | --- | --- |
| Who | Con người | `:Person` | `P` + 5 số | `historical_role_class` |
| Who, by whom | Tổ chức, thể chế | `:Group` | `GRP` + 4 số | `group_type` |
| What, how | Sự kiện | `:Event` | `EV` + 5 số | `event_type` |
| Where | Không gian, địa lý | `:Place` | `LOC` + 4 số | `spatial_category` |
| When | Thời gian, niên đại | `:TimeSpan` | `TIM` + 4 số | `temporal_granularity` |
| What, means | Hiện vật, di sản | `:Artifact` | `ART` + 4 số | `artifact_type` |
| Why, strategy | Kế sách, tư tưởng | `:Concept` | `CON` + 4 số | `concept_category` |
| Evidence | Nguồn sử liệu | `:Source` | `SRC` + 4 số | `source_perspective` |

Label `:Strategy` ở các note cũ nay là `:Concept` với `concept_category = MilitaryTactic`. Node `:Assertion` dùng cho dị bản ở cuối Phase 1 là node phụ, không phải chủ thể thứ chín.

## Mã định danh

Mã là khóa mờ do PostgreSQL cấp, theo `Note/thiet-ke-dinh-danh.md`. Mã không chứa tên hay năm. Các file gốc có mã ghép tên và mốc thời gian thì không dùng khi code.

| Chủ thể | Mẫu | Ví dụ minh họa |
| --- | --- | --- |
| Con người | `P` + 5 số | `P00001` |
| Sự kiện | `EV` + 5 số | `EV00001` |
| Tổ chức | `GRP` + 4 số | `GRP0001` |
| Không gian | `LOC` + 4 số | `LOC0001` |
| Thời gian | `TIM` + 4 số | `TIM0001` |
| Hiện vật | `ART` + 4 số | `ART0001` |
| Kế sách, tư tưởng | `CON` + 4 số | `CON0001` |
| Nguồn | `SRC` + 4 số | `SRC0001` |

## Danh xưng và trùng tên

Một người nhiều tên cùng trỏ một mã. Các tên nằm ở `entity_aliases`, không thành node mới.

Một tên nhiều thực thể là nhiều mã. Ba trận cùng một địa danh ở ba năm là ba mã `EV` khác nhau. Năm nằm ở thuộc tính và ở quan hệ với `:TimeSpan`, không nằm trong mã.

Bước khử trùng lặp danh xưng tra `entity_aliases` trên PostgreSQL trước, dùng chỉ mục trigram. Chưa đủ chắc thì `FLAGGED`. Embedding chỉ xếp hạng ứng viên. Mã mới chỉ do sequence của PostgreSQL cấp.

## Linked open data

Node có sẵn trường cho mã ngoài: `external_wikidata_id`, `external_geonames_id` với địa danh, `external_viaf_id` với tác giả và danh nhân. Các trường này được phép trống. Chỉ điền khi đã tự tra và đối chiếu mã. Không để mô hình đoán mã. Đồ án không đo các trường này.

## Danh mục phân loại đóng

Trường phân loại chỉ nhận giá trị trong danh mục. Mô hình trả nhãn ngoài danh mục thì JSON bị từ chối. Danh mục được sửa bằng cách đổi phiên bản schema, không sửa ngầm trong lúc chạy. Trong đồ án, danh mục đóng băng sau tuần 8 để các lần đo cùng một schema.

| Trường | Giá trị |
| --- | --- |
| `event_type` | `MilitaryBattle`, `PoliticalReform`, `Diplomacy`, `CulturalReligious`, `UprisingRebellion`, `PersonalMilestone`, `SocioEconomicEvent` |
| `historical_role_class` | `Monarch`, `MilitaryCommander`, `ScholarOfficial`, `ReligiousFigure`, `CulturalCreator`, `CivilianWitness`, `Diplomat` |
| `group_type` | `Dynasty`, `ImperialCourt`, `MilitaryForce`, `SocialClass`, `ReligiousSect`, `InternationalOrg`, `RebelFaction` |
| `spatial_category` | `AdministrativeCenter`, `Battlefield`, `StrategicPass`, `WaterwayPort`, `CulturalSite`, `NaturalLandmark` |
| `temporal_granularity` | `ExactDay`, `MonthYear`, `SpecificYear`, `RegnalEra`, `DynasticPeriod`, `Century` |
| `artifact_type` | `WeaponEquipment`, `LiteraryWork`, `Epigraphy`, `MonumentArchitecture`, `SacredRelic`, `HistoricalDocument` |
| `concept_category` | `MilitaryTactic`, `GrandStrategy`, `GovernancePhilosophy`, `IdeologicalDoctrine`, `DiplomaticPrinciple` |
| `source_perspective` | `DomesticOfficial`, `ForeignHostile`, `PrivateScholarly`, `Archaeological`, `FolkTradition` |

JSON schema mẫu trong bản v2 chỉ liệt kê `ExactDay`, `MonthYear`, `SpecificYear`, `Century` cho `temporal_granularity`. Bảng phân loại của cùng file có thêm `RegnalEra` và `DynasticPeriod`. Khi viết Pydantic, lấy đủ danh mục ở bảng trên.

`event_type` cũ của đồ án là `battle`, `diplomacy`, `reform`, `text`. Từ nay dùng danh mục trên. Việc soạn một văn bản như hịch hoặc cáo đi vào `Artifact` loại `LiteraryWork`, kèm sự kiện nếu nguồn có nêu.

## Từ khóa theo chủ thể

Bảng dưới là các nhóm từ khóa chính. Tên trường đầy đủ, kiểu dữ liệu và ví dụ nằm ở mục IV của bản v2.

| Chủ thể | Nhóm từ khóa |
| --- | --- |
| Con người | Mã, tên chính, tên khai sinh, tên tự, hiệu và bút danh, tôn hiệu và tước phong, vai trò, năm sinh và năm mất, quê quán, dòng tộc, chức vụ, vị thế lịch sử |
| Sự kiện | Mã, tên, loại, mốc đầu và mốc cuối, độ chính xác niên đại, quy mô, kết quả tức thời, ý nghĩa lâu dài, tóm tắt diễn biến |
| Tổ chức | Mã, tên, loại, kinh đô hoặc đại bản doanh, năm lập và năm kết thúc, danh hiệu người đứng đầu, thành phần xã hội, tôn chỉ |
| Không gian | Mã, tên lịch sử, tên ngày nay, loại không gian, cấp hành chính, địa hình, tọa độ, giá trị chiến lược |
| Thời gian | Mã, năm dương lịch, năm can chi, niên hiệu, triều kỳ, thế kỷ, độ chính xác, đặc trưng thời đại |
| Hiện vật | Mã, tên, loại, chất liệu, thời điểm tạo, tác giả hoặc người tạo, tình trạng hiện nay, giá trị chứng tích |
| Kế sách, tư tưởng | Mã, tên, loại, người khởi xướng, nguyên lý, mục tiêu, tiền lệ |
| Nguồn | Mã, tên, tác giả hoặc người biên soạn, thời điểm biên soạn, góc nhìn, vị trí trích dẫn, đoạn trích gốc, độ tin cậy |

Các từ khóa đánh giá như vị thế lịch sử, ý nghĩa lâu dài, độ tin cậy chỉ được ghi khi có nguồn nói. Mô hình không tự viết lời bình vào các trường đó.

## Quan hệ giữa các chủ thể

| Cặp chủ thể | Quan hệ |
| --- | --- |
| Con người với sự kiện | Chỉ huy, tham gia, ở phía đối địch, chịu tác động, ghi chép làm nhân chứng |
| Con người với tổ chức | Sáng lập, đứng đầu, phụng sự, chống đối |
| Sự kiện với không gian | Diễn ra tại, xuất phát từ hoặc đi qua, rút về |
| Sự kiện với thời gian | Bắt đầu, kết thúc, thuộc niên đại hoặc triều đại |
| Sự kiện với kế sách, tư tưởng | Dùng kế sách, thể hiện tư tưởng |
| Sự kiện với hiện vật | Dùng hiện vật, sinh ra tác phẩm, để lại di tích |
| Mọi chủ thể với nguồn | Được ghi trong nguồn, hai nguồn tương đồng, hai nguồn mâu thuẫn |

Tên edge trong code chốt ở sprint 1–2. Các tên đã có: `COMMANDED`, `PARTICIPATED_IN`, `OPPOSED_IN`, `TOOK_PLACE_AT`, `OCCURRED_DURING`, `EMPLOYED_STRATEGY`, `LEFT_HERITAGE`, `SUPPORTS`. Note thứ hai dùng `RECORDS` cho quan hệ nguồn ghi sự kiện. Proposal đồ án dùng `SUPPORTS`, kèm đoạn trích, nên code giữ `SUPPORTS`.

## Ràng buộc

| Ràng buộc | Nội dung | Trong đồ án |
| --- | --- | --- |
| Niên đại sinh và mất | Một người không thể tham gia sự kiện trước khi sinh hoặc sau khi mất, trừ khi nguồn nói về việc hậu thế tôn vinh | Kiểm khi nạp. Vi phạm thì `FLAGGED`, không tự sửa năm |
| Địa danh xưa và nay | Địa danh lịch sử đi kèm tên hành chính ngày nay | Có trường `modern_name`. Danh mục địa danh thí điểm điền tay. Mô hình không đoán tên ngày nay |
| Nguồn bắt buộc | Mọi khẳng định và quan hệ gắn với ít nhất một nguồn | Có. Thiếu đoạn trích thì `draft` |
| Giữ dị bản | Hai bộ sử chép khác nhau thì giữ cả hai và nối bằng quan hệ đối chiếu | Không. Thuộc cuối Phase 1 |
| Đồng nhất thực thể | Một người nhiều tên vẫn là một node | Có, qua bước khử trùng lặp danh xưng |

## Graph và vector

Neo4j: mỗi chủ thể là một node có label riêng. Mã lưu ở `id`, có ràng buộc duy nhất cho từng label. Trường phân loại lưu dạng chuỗi trong danh mục.

ChromaDB: mỗi đoạn văn lưu `metadata.linked_entity_ids` là các mã chủ thể xuất hiện trong đoạn, kèm `metadata.event_type` để lọc. Đồ án tạo schema và vài bản ghi mẫu. Nạp hàng loạt thuộc phần sau của Phase 1.

Hybrid search: graph tìm mã, rồi dùng mã làm metadata filter cứng bên vector database. Cách này giới hạn tập đoạn văn được dùng. Nó không bảo đảm câu trả lời đúng 100% và không xóa hẳn ảo giác. Câu trả lời vẫn sai được nếu bản ghi nạp sai hoặc bước sinh câu viết thêm. Cách đo nằm ở `06-danh-gia`.

## Đồ án nhận phần nào

- Schema khai báo đủ tám chủ thể, tiền tố mã, ràng buộc duy nhất và danh mục phân loại đóng.
- Kết quả trích xuất của một đoạn là các bản ghi chủ thể kèm từ khóa, cùng các quan hệ giữa chúng. Không còn phiếu sự kiện mười trường. Hai đầu của mỗi quan hệ là mã chủ thể đã qua khử trùng lặp danh xưng, không phải chuỗi tên thô.
- Bộ từ khóa dùng để đo được chốt cùng danh mục phân loại sau tuần 8. Độ khớp F1 đo theo từ khóa và theo quan hệ.
- Kho thí điểm Bạch Đằng 1288 nạp các chủ thể mà đoạn chữ có nói tới: người, tổ chức, sự kiện, nơi, thời gian, kế sách, hiện vật, nguồn.
- Khử trùng lặp danh xưng làm cho người, tổ chức và địa danh.
- Mã linked open data, nạp vector hàng loạt và giữ dị bản để sau.
