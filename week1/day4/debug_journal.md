# 4.11 - Debug journal

## Lỗi 1: Chia cho 0 trong average_score
- Triệu chứng: ZeroDivisionError khi danh sách rỗng.
- Nguyên nhân: hàm average_score chia len(rows) mà không check rỗng.
- Cách AI giúp: gợi ý thêm điều kiện if not rows: return 0.0 hoặc raise ValueError.
- Kết quả: bổ sung check rỗng (được demo trong quá trình học).

## Lỗi 2: Sai tên cột trong filter
- Triệu chứng: filter trả về rỗng khi dùng sai column.
- Nguyên nhân: input sai tên cột, không có trong row.
- Cách AI giúp: thêm cảnh báo nếu column không tồn tại.
- Kết quả: cập nhật hướng dẫn sử dụng, thông báo lỗi rõ ràng hơn.
