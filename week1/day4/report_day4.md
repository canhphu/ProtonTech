# Báo cáo Day 4 - Kết quả đạt được

## Tài liệu và script đã hoàn thành
- Script CSV: week1/day4/csv_tool.py
- Unit tests: week1/day4/test_csv_tool.py
- Debug journal: week1/day4/debug_journal.md
- Ghi chú quá trình AI-assisted: week1/day4/ai_assisted_script_notes.md

## Kết quả chạy script CSV
Lệnh:
```
python csv_tool.py data.csv --filter-column city --contains hanoi --stats-column age
```
Kết quả:
```
Stats:
{'count': 2, 'min': 28.0, 'max': 30.0, 'mean': 29.0}
```

## Kết quả chạy unit tests
Lệnh:
```
python -m unittest test_csv_tool.py
```
Kết quả:
```
....
----------------------------------------------------------------------
Ran 4 tests in 0.012s

OK
```

## Ghi chú
- Script xử lý CSV hoạt động đúng với dữ liệu mẫu.
- Unit tests chạy pass toàn bộ.
- Debug journal đã ghi lại các lỗi và cách AI hỗ trợ sửa.
