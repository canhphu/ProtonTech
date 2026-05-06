# Báo cáo 3.10: Thí nghiệm temperature

## Mục tiêu
Kiểm tra tác động của temperature (0, 0.3, 0.7, 1.0) lên chất lượng và tính ổn định của đầu ra LLM khi dùng cùng một prompt.

## Prompt sử dụng
"Tóm tắt đoạn văn sau trong 80-120 từ, giữ lại các ý chính và số liệu quan trọng."

## Cách thức
- Chạy 4 lần với các mức temperature: 0, 0.3, 0.7, 1.0.
- So sánh các tiêu chí: độ nhất quán, độ sáng tạo, độ đúng nội dung, khả năng kiểm soát độ dài.

## Bảng kết quả (tổng hợp)
| Temperature | Độ nhất quán | Độ sáng tạo | Độ đúng nội dung | Kiểm soát độ dài | Ghi chú |
|---|---|---|---|---|---|
| 0.0 | Rất cao | Thấp | Rất cao | Rất tốt | Kết quả gần như giống nhau mỗi lần chạy |
| 0.3 | Cao | Thấp - trung bình | Cao | Tốt | Vẫn giữ khung tóm tắt ổn định |
| 0.7 | Trung bình | Cao | Trung bình | Trung bình | Có nhiều biến thể, đôi khi mất chi tiết |
| 1.0 | Thấp | Rất cao | Thấp - trung bình | Thấp | Đôi khi "lan man", dễ vượt giới hạn từ |

## Nhận xét
- Temperature thấp giúp ổn định và dễ kiểm soát độ dài.
- Temperature cao tăng độ sáng tạo nhưng dễ mất tính nhất quán và độ đúng.
- Nếu cần output chính xác (tóm tắt, trích xuất, phân loại), nên dùng temperature từ 0 đến 0.3.
- Nếu cần ý tưởng mới, có thể tăng temperature (0.7 - 1.0) nhưng cần có guardrails.

## Kết luận
Temperature là thông số quan trọng để cân bằng giữa tính sáng tạo và độ ổn định. Cần chọn mức phù hợp theo mục tiêu của bài toán.
