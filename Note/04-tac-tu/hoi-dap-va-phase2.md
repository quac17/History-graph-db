# Agent hỏi đáp và Phase 2

Người thực hiện: Trần Việt Hoàng. MSSV: 25MSA13219.

Phase 2 là giai đoạn sau của dự án. Đồ án không làm các mục này. File này để khi code Phase 1 không lỡ xây chatbot.

## Luồng một câu hỏi

Câu mẫu: "Hưng Đạo đại vương là ai?"

1. Nhận câu, chuẩn hóa tiếng Việt.
2. ToolPlanner gán ý định (intent). Câu này là tiểu sử và quan hệ của một người, không phải hỏi một trận.
3. Graph: tra master registry (PostgreSQL cấp mã mờ, giữ danh xưng, nguồn và log) theo danh xưng để lấy mã mờ, rồi trả sự kiện, tác phẩm, chức danh kề một bước.
4. Vector: lấy đoạn văn có `linked_entity_ids` chứa node đó.
5. Hợp nhất. Bỏ đoạn văn không cùng mã node.
6. Sinh câu theo 5W1H chỉ bằng các trường có nguồn.
7. Gợi một câu tiếp theo còn trong graph, ví dụ chiến thuật Bạch Đằng, hoặc quan hệ với Trần Nhân Tông nếu edge đó đã có.

Câu mẫu thứ hai: "Đã dùng cách đánh nào trên sông Bạch Đằng năm 1288, và vì sao có trận đó?"

Tách Who, Where, When, How. Lọc `year = 1288` và `place = LOC0001`. Không kéo tiểu sử sau năm 1288 vào câu trả lời. Không trộn `EV00002` hay `EV00003` vào câu trả lời, trừ khi câu hỏi đòi so sánh các trận cùng nơi.

## Kiểm soát lệch khi duyệt graph

Proposal Phase 2 ghi hai cơ chế:

- Lọc thời gian và địa điểm trước khi đi nhiều bước.
- Mỗi bước nhảy nhân hệ số suy giảm gamma = 0.5. Dưới threshold tau = 0.2 thì cắt nhánh.

Hai số này là tham số thiết kế, chưa phải kết quả đo. Phase 2 phải thử trên tập câu hỏi rồi mới giữ.

Intent cần phân loại tối thiểu: `event`, `person`, `compare_sources`. Loại thứ ba mới được đọc edge `CONTRADICTS`.

## Scaffolding sư phạm

Agent không thay giáo viên và không chấm bài. Việc của nó:

- Hiện nguồn nào nói câu nào.
- Nhắc người học kiểm tác giả và thời điểm của nguồn.
- Đặt sự kiện vào năm và nơi đã lọc.
- Nếu có hai assertion mâu thuẫn, hiện cả hai, không san thành một đáp án.
- Gợi một câu hỏi 5W1H còn thiếu trong kho.

Ba kỹ năng proposal muốn rèn: sourcing, contextualization, corroboration.

## Ngoài phạm vi cả hai phase của nguyên mẫu

Không làm bảo tàng thực tế ảo, không làm không gian chế tác, không đủ ontology cho triết, văn, địa, chính trị. Các môn đó chỉ là bản đồ đổi node ở `02-kien-truc/mo-rong-khxh.md`.
