# Chuẩn hóa lịch pháp cổ và đơn vị đo lường sử liệu

Phân định việc của tầng lưu trữ (Phase 1) và tầng truy xuất (Phase 2).

PostgreSQL là master registry: cấp mã mờ, giữ danh xưng, nguồn và log. Mã chủ thể không chứa năm hay tên. Bảng niên hiệu, can chi và đơn vị đo là bảng tra cứu, không cấp `entity_id`.

## Nguyên tắc

Niên hiệu, can chi và đơn vị cổ (dặm, lý, trượng, cân, lạng, hộc, mẫu) đổi theo triều đại. Tầng lưu trữ không hòa giải các cách ghi lệch nhau.

Trong Phase 1:

- Giữ nguyên chuỗi gốc, ví dụ "ngày Mậu Tuất tháng 3 năm Mậu Tý, niên hiệu Trọng Hưng thứ 4" hoặc "3 vạn quân".
- Ghi song song năm dương lịch và giá trị SI khi quy đổi được. Hệ số là giá trị tham chiếu theo bối cảnh, không phải một số đúng duy nhất.
- Không suy diễn dị bản ở tầng này.

Trong Phase 2:

- Đối chiếu các mốc và các số đo mâu thuẫn.
- Mở rộng câu hỏi của người dùng, ví dụ "năm 1288" hoặc "30.000 quân", sang niên hiệu, can chi và đơn vị cổ.
- Diễn giải cho người dùng. Đồ án chưa làm phần này.

## Lịch pháp

Ba kiểu mốc:

- Tuyệt đối theo niên hiệu hoặc can chi: "năm Mậu Tý", "niên hiệu Hồng Đức thứ 10". Năm dương lịch đi kèm là thuộc tính, không nằm trong mã.
- Tương đối: "sau trận Bạch Đằng", "đầu thế kỷ XIII", "thời nhà Trần".
- Chưa chốt: "khoảng năm 1228–1231". Khoảng này lưu bằng `solar_year_start` và `solar_year_end`, không gộp thành một năm.

Hai bảng tra cứu trên PostgreSQL:

```sql
CREATE TABLE ref_historical_eras (
    era_id VARCHAR(20) PRIMARY KEY,       -- ERA0001, khóa danh mục, không phải entity_id
    dynasty_name VARCHAR(100) NOT NULL,
    king_name VARCHAR(100),
    era_name VARCHAR(100) NOT NULL,       -- Trọng Hưng
    start_year_solar INT,
    end_year_solar INT
);

CREATE TABLE ref_ganzhi_cycles (
    ganzhi_name VARCHAR(50) PRIMARY KEY,  -- Mậu Tý
    stem_vi VARCHAR(20),                  -- Mậu
    branch_vi VARCHAR(20)                 -- Tý
);
```

`ref_ganzhi_cycles` chỉ có 60 tên can chi. Đó là danh mục đóng, không phải mã `:TimeSpan`.

Chủ thể thời gian vẫn là `:TimeSpan`, mã `TIM` + 4 số, ví dụ `TIM0001`. Năm 1288 nằm ở thuộc tính.

```sql
CREATE TABLE dim_time_entities (
    time_id VARCHAR(20) PRIMARY KEY,          -- TIM0001
    raw_text VARCHAR(255) NOT NULL,
    lunar_day INT,
    lunar_month INT,
    lunar_year_ganzhi VARCHAR(50),
    era_id VARCHAR(20),                       -- trỏ ref_historical_eras, được phép trống
    era_year INT,
    solar_year_start INT,
    solar_year_end INT,
    solar_date_iso_start DATE,                -- chỉ điền khi đã quy đổi và có nguồn phép tính
    solar_date_iso_end DATE,
    time_granularity VARCHAR(20) DEFAULT 'YEAR'
);
```

`time_granularity` nhận `DAY`, `MONTH`, `YEAR`, `CENTURY`, `ERA`, khớp danh mục `temporal_granularity` của hệ thống chủ thể. Ngày ISO để trống nếu chỉ biết năm hoặc nếu phép đổi lịch chưa được kiểm. Không điền một ngày dương lịch chỉ để cho đủ cột.

Trên Neo4j, node thời gian dùng cùng mã:

```cypher
(:TimeSpan {
  id: 'TIM0001',
  raw_text: 'Năm Mậu Tý, niên hiệu Trọng Hưng thứ 4',
  solar_year_start: 1288,
  solar_year_end: 1288
})
```

Quan hệ sự kiện với thời gian là `OCCURRED_DURING`, không tạo kiểu edge mới cho cùng việc đó.

## Đơn vị đo

Bảng dưới là hệ số tham chiếu, không phải định mức duy nhất của mọi triều. Các sách không thống nhất về dặm, thước và mẫu. Khi nạp, ghi `historical_context`. Nếu đoạn chữ không đủ để chọn một hệ số thì lưu biểu thức gốc và để giá trị SI trống, không bịa một con số.

| Nhóm | Đơn vị gốc | Hệ số tham chiếu | Bối cảnh |
| --- | --- | --- | --- |
| Độ dài | Dặm, lý | Khoảng 444 m đến 576 m tùy nguồn | Không gộp dặm và lý thành một hệ số |
| Độ dài | Trượng | Khoảng 4 m; một số ghi thời Nguyễn khoảng 4,25 m | 1 trượng thường được hiểu là 10 thước |
| Độ dài | Thước, xích | Khoảng 0,40 m đến 0,47 m | Thước đo đất khác thước đo vải |
| Khối lượng | Cân | Khoảng 0,6 kg | 1 cân = 16 lạng trong cách đếm phổ biến |
| Khối lượng | Lạng | Khoảng 37,8 g | 1 lạng = 10 tiền |
| Khối lượng | Yến, tạ | 1 yến = 10 cân, 1 tạ = 100 cân, theo cùng hệ số cân đang chọn | Ghi rõ hệ số cân đã dùng |
| Dung tích | Hộc | Không quy ra kilogam nếu nguồn không nói đó là thóc hay gạo | Để SI trống khi không rõ chất được đong |
| Diện tích | Mẫu, sào, thước | Mẫu Bắc Bộ thường nhớ là 3.600 m2, mẫu Trung Bộ khác | Phụ thuộc vùng và triều |
| Quân số | Vạn | 10.000 trong cách đếm thập phân | "3 vạn" thành 30.000 chỉ khi ngữ cảnh là số người |
| Biên chế | Cơ, vệ, đội | Không có một sĩ số cho mọi triều | Không nhân một hệ số cố định |

```sql
CREATE TABLE ref_measurement_units (
    unit_id VARCHAR(30) PRIMARY KEY,       -- UNIT0001, khóa danh mục, không phải entity_id
    raw_unit_name VARCHAR(50) NOT NULL,
    category VARCHAR(30) NOT NULL,         -- LENGTH, WEIGHT, VOLUME, AREA, TROOP
    si_unit VARCHAR(20),
    conversion_factor NUMERIC(12, 4),      -- được phép trống
    historical_context VARCHAR(255) NOT NULL
);
```

Một câu như "30 vạn quân và 50 vạn hộc lương" tách thành từng số đo. Giá trị SI của hộc để trống cho đến khi có nguồn nói rõ cách đong.

```json
{
  "entity_id": "EV00001",
  "measurements": [
    {
      "raw_expression": "30 vạn quân",
      "quantity_raw": 30,
      "unit_raw": "vạn",
      "target_type": "TROOP_SIZE",
      "normalized_value_si": 300000,
      "si_unit": "person",
      "conversion_note": "tham chiếu thập phân, 1 vạn = 10000"
    },
    {
      "raw_expression": "50 vạn hộc lương",
      "quantity_raw": 50,
      "unit_raw": "vạn hộc",
      "target_type": "SUPPLY_VOLUME",
      "normalized_value_si": null,
      "si_unit": null,
      "conversion_note": "nguồn không nói hộc tương đương bao nhiêu"
    }
  ]
}
```

Số đo gắn với chủ thể mà câu nói tới, thường là `:Event` hoặc `:Group`. Không tạo chủ thể thứ chín cho đơn vị đo.

## Việc của từng tầng

| Việc | Phase 1, tầng lưu trữ | Phase 2, tầng truy xuất |
| --- | --- | --- |
| Lịch | Trích xuất và lưu `raw_text` cùng khoảng dương lịch, can chi, niên hiệu | Mở rộng câu hỏi "năm 1288" sang niên hiệu và can chi |
| Số đo | Lưu biểu thức gốc và giá trị SI nếu hệ số đã chọn được | Tìm theo khoảng giá trị, so sánh quân số giữa các trận |
| Dị bản | Giữ các bản ghi có nguồn dù chúng lệch nhau. Không chọn một câu làm sự thật | Đối chiếu và trình bày nhiều góc nhìn |
| Đại từ | Giải về mã mờ trong pipeline trích xuất. Chưa chắc thì `FLAGGED`, không tạo edge | Đọc graph theo mã đã có |
| Tái bản | Giữ bản cũ, đặt `doc_status = SUPERSEDED`. Bản mới là `ACTIVE` | Lọc bản mới làm mặc định. Mở bản cũ khi người dùng hỏi lịch sử đính chính |

Đồ án làm phần lưu trữ ở cột Phase 1 ở mức kho thí điểm: chuỗi gốc, khoảng năm, số đo tách được, và đại từ đã giải. Mở rộng câu hỏi, so sánh khoảng số, đối chiếu dị bản và lọc tái bản cho người dùng thuộc Phase 2 hoặc phần sau của Phase 1. Nạp embedding hàng loạt không thuộc đồ án.
