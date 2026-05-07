# 4.10 - Script CSV với hỗ trợ AI (quá trình)

## Mục tiêu
Tạo 1 script xử lý CSV: đọc file, lọc theo điều kiện, thống kê cột số, ghi kết quả ra file.

## Bước thực hiện
1. Xác định yêu cầu: cần đọc CSV, filter theo contains/min/max, tính count/min/max/mean.
2. Thiết kế API hàm: read_csv, filter_rows, compute_stats, write_csv, main.
3. Viết CLI với argparse để dễ sử dụng và test.
4. Viết unit tests cho từng hàm quan trọng.
5. Chạy thử và chỉnh sửa logic.

## Ghi chú về AI
- AI giúp phác họa khung hàm và CLI.
- AI gợi ý cách xử lý numeric filter và thống kê.
- AI đề xuất unit tests đơn giản bằng unittest.
