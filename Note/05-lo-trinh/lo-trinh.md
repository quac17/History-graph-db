# Lộ trình

Người thực hiện: Trần Việt Hoàng. MSSV: 25MSA13219.

Có hai lịch trong `Project tong`. Lịch đang dùng là bản 18 tháng. Lịch 24 tháng giữ ở cuối file để khỏi mất, không dùng để xếp sprint đồ án.

## Dự án — 18 tháng, 36 sprint

Mỗi sprint 2 tuần. Phase 1 là tháng 1–8. Phase 2 là tháng 9–18.

| Mốc | Sprint | Việc |
| --- | --- | --- |
| Tháng 1–2 | 1–4 | Schema 5W1H, ontology hướng sự kiện, dựng Neo4j, ChromaDB, PostgreSQL |
| Tháng 3–4 | 5–8 | Gold set, extractor, nạp graph, khử trùng lặp danh xưng |
| Tháng 5–6 | 9–12 | Cắt đoạn, embedding, liên kết hai chiều giữa đoạn văn và node, ingestor ổn định |
| Tháng 7–8 | 13–16 | Dị bản, hoàn thiện API, nghiệm thu Phase 1 |
| Tháng 9–10 | 17–20 | ToolPlanner, lọc thời gian và địa điểm |
| Tháng 11–12 | 21–24 | Hệ số suy giảm theo bước nhảy, score fusion |
| Tháng 13–14 | 25–28 | Agent và scaffolding sourcing, contextualization, corroboration |
| Tháng 15–16 | 29–32 | Web học tập, nối end-to-end |
| Tháng 17–18 | 33–36 | Thử trên lớp, KPI, báo cáo |

File gốc: `Project tong/master-proposal-18-thang.docx`.

## Đồ án — 4 tháng, 8 sprint

Là tháng 1–4 ở bảng trên. Không gồm chatbot, không gồm liên kết hàng loạt giữa đoạn văn và node, không gồm dị bản.

| Tháng | Sprint | Việc | Xong khi |
| --- | --- | --- | --- |
| 1 | 1–2 | Hệ thống chủ thể và từ khóa, mã định danh mờ, master registry (PostgreSQL cấp mã mờ, giữ danh xưng, nguồn và log), danh mục phân loại, edge, ba database trong Docker | Schema Pydantic và sequence cấp mã chạy |
| 2 | 3–4 | Gold set 150–200 sự kiện, API khung | Có tệp nhãn và OpenAPI |
| 3 | 5–6 | Extractor và nạp Neo4j | Một đoạn chữ thành node, chạy lại không nhân đôi |
| 4 | 7–8 | Khử trùng lặp danh xưng, Streamlit, đo độ khớp F1 và precision | Demo ba phút và bảng số |

Bản đang dùng: `Do An/proposal/proposal.md`. Thesis proposal theo form mới: `Do An/thesis-proposal/muc-01.md` đến `muc-06.md`.

Thứ tự trong file đồ án đặt khử trùng lặp danh xưng ở tháng 4, sau nạp graph. Khi code, bước này phải chạy trước lệnh tạo node Person. Tháng 3 nạp được với tên đã chuẩn hóa tay. Tháng 4 mới bật khử trùng lặp tự động. Đừng tạo node trùng rồi mới gộp nếu chưa có thử nghiệm.

## Phương án 24 tháng — không dùng để xếp việc

`Project tong/de-xuat-de-tai-hoan-chinh demo1.docx` chia Phase 1 thành 12 tháng và Phase 2 thành 12 tháng. Note lộ trình cũ cũng chia Phase 1 thành 4 quý, 24 sprint. Nội dung kỹ thuật trùng bản 18 tháng, chỉ dài hơn ở quý vector và quý dị bản. Khi hai lịch lệch nhau, lấy bảng dự án 18 tháng và bảng đồ án ở trên.
