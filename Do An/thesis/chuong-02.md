# CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ NGHIÊN CỨU LIÊN QUAN

## 2.1 Tổng quan nghiên cứu liên quan

Phần này chỉ xét bốn nhóm việc mà pipeline phải xử lý trước khi một câu sử liệu thành bản ghi: lịch pháp, đơn vị đo cổ, đại từ, và provenance của khẳng định. Các nhóm khác của chương sẽ được bổ sung sau.

Lịch âm-dương Đông Á tính tháng theo sóc và đặt tháng nhuận theo trung khí. Aslaksen chỉ ra rằng quy tắc này đã đổi nhiều lần, và nhiều sách vẫn mô tả quy tắc của một lần cải lịch đã cũ [1]. Lịch Việt Nam hiện hành cũng là lịch thiên văn, tháng bắt đầu ở ngày chứa sóc, đông chí nằm ở tháng mười một, và phép tính lấy kinh tuyến 105 độ đông [2]. Vì múi giờ và mốc cải lịch khác nhau, không được lấy ngày Tết Trung Hoa làm ngày Tết Việt. Niên hiệu lại là một lớp nữa: cùng một năm dương lịch có thể được gọi bằng can chi và bằng niên hiệu của vua. Muốn tra "năm 1288" thì phải giữ cả chuỗi gốc lẫn khoảng năm dương lịch.

Đơn vị đo trong sử Việt không có một bảng duy nhất. Nguyễn Tùng tập hợp các cách ghi dặm, lý và thước trong từ điển và hội điển: cùng một tên đơn vị được các nguồn gán các độ dài khác nhau, và dặm không trùng lý [7]. Vì vậy một hệ số SI gắn vào "dặm" hoặc "mẫu" chỉ là hệ số tham chiếu theo triều và theo vùng.

Tiếng Việt có bài toán giải đại từ riêng. Tran và Nguyen mô hình hóa đại từ liên câu bằng đặc điểm ngữ pháp và tiêu điểm của đoạn [4]. Tran, Nguyen và Nguyen sau đó lập dữ liệu coreference trên văn kể và thử LLM. Kết quả lệch nhau giữa các mô hình, nên không có cơ sở để xem mọi đại từ là đã giải đúng [3]. VnCoreNLP tách từ, gán nhãn từ loại, nhận thực thể có tên và phân tích phụ thuộc, nhưng không có bước giải đại từ [5]. Sử liệu còn thêm tước hiệu và từ chỉ "bấy giờ", "nơi đây", vốn không nằm trong các tập tin tức mà các bài trên dùng.

Provenance, theo PROV-DM, là thông tin về thực thể, hoạt động và tác nhân đã tạo ra một dữ liệu, để người đọc xét độ tin cậy [6]. Trên knowledge graph, một quan hệ là một khẳng định. Khẳng định đó cần trỏ về đoạn nguồn đã sinh ra nó. Xóa quan hệ chỉ vì một đoạn sai sẽ mất các đoạn khác vẫn đang củng cố cùng quan hệ đó.

## 2.2 Cơ sở lý thuyết và công nghệ cốt lõi

Đồ án tách việc lưu khỏi việc lập luận. Tầng lưu trữ giữ chuỗi gốc và, khi quy đổi được, giữ thêm giá trị chuẩn hóa. Tầng truy xuất, thuộc Phase 2, mới đối chiếu các giá trị lệch nhau và mới diễn giải cho người dùng.

Với thời gian, đơn vị lưu là một chủ thể `:TimeSpan` có mã mờ. Can chi và niên hiệu nằm ở bảng tra cứu và ở thuộc tính, không nằm trong mã. Ngày dương lịch đầy đủ chỉ được điền khi phép đổi đã kiểm. Chỉ biết năm thì lưu khoảng năm.

Với số đo, đơn vị lưu là thuộc tính của sự kiện hoặc tổ chức, gồm biểu thức gốc, đơn vị gốc và giá trị SI nếu có hệ số. Không tạo thêm một loại chủ thể cho "dặm" hay "hộc".

Với đại từ, pipeline nhận span, tìm tiền đề trong cửa sổ câu, rồi mới đối danh xưng với kho mã. Quan hệ trên graph chỉ nối mã. Span không có tiền đề đủ chắc thì không thành cạnh.

Với nguồn, mỗi cạnh giữ danh sách đoạn minh chứng. Đó là dạng provenance mức khẳng định, tương ứng ý "một thực thể dữ liệu được dẫn xuất từ thực thể khác" trong PROV-DM [6], thu hẹp vào đoạn sử liệu và quan hệ. Bản tái bản không ghi đè bản cũ. Trạng thái tài liệu `ACTIVE` hoặc `SUPERSEDED` khác với trạng thái kiểm của bản ghi trích xuất.

## 2.3 Khoảng trống nghiên cứu

Các công cụ tiếng Việt hiện có nhận được thực thể có tên, nhưng chưa nhận chuỗi niên hiệu và số đo cổ như một thuộc tính có nguồn, và chưa giải tước hiệu theo mốc của đoạn sử [5]. Các phép đổi lịch và các bảng đơn vị đo lại không gắn với một mã chủ thể ổn định: cùng một người nhiều tên, cùng một năm nhiều cách gọi, vẫn cần một mã không chứa năm. Khoảng trống của đồ án là giữ đồng thời chuỗi sử liệu gốc và giá trị chuẩn hóa dưới mã mờ đó, đồng thời không biến một đại từ chưa giải thành một node.
