# Báo cáo 2.12: So sánh prompt có cấu trúc vs prompt thô

## Mục tiêu
Đánh giá hiệu quả của prompt có cấu trúc (Role + Instruction + Context + Constraint + Output Format) so với prompt thô khi thực hiện các tác vụ LLM thông dụng.

## Phương pháp
- Chọn 3 tác vụ mẫu: tóm tắt, phân loại email, trích xuất thông tin.
- Tạo 2 bộ prompt: (A) prompt thô, (B) prompt có cấu trúc.
- Đánh giá theo 4 tiêu chí: độ đúng, độ rõ ràng, tính nhất quán, khả năng parse đầu ra.

## Kết quả tổng quan
- Prompt có cấu trúc cho kết quả ổn định hơn và ít sai sót hơn.
- Khi yêu cầu JSON output, prompt có cấu trúc giảm lỗi parse rõ rệt.
- Prompt thô dễ bị thiếu thông tin và thay đổi định dạng đầu ra.

## Ví dụ tóm tắt (rút gọn)
**Prompt thô**
"Hãy tóm tắt đoạn văn sau."

**Prompt có cấu trúc**
- Role: Trợ lý tóm tắt ngắn gọn
- Instruction: Tóm tắt đoạn văn
- Context: Văn bản đầu vào
- Constraint: tối đa 120 từ, giữ ý chính, bỏ chi tiết phụ

**Nhận xét**
Prompt có cấu trúc trả về tóm tắt ngắn gọn và nhất quán hơn, đảm bảo giới hạn độ dài.

## Ví dụ phân loại email
**Prompt thô**
"Phân loại email này vào nhóm phù hợp."

**Prompt có cấu trúc**
- Role: Email triage classifier
- Instruction: Chọn 1 nhãn duy nhất
- Context: Nội dung email
- Constraint: Label rõ ràng, trả về JSON

**Nhận xét**
Prompt có cấu trúc trả về nhãn ổn định, có độ tin cậy và lý do ngắn gọn, dễ parse tự động.

## Ví dụ trích xuất thông tin
**Prompt thô**
"Lấy thông tin quan trọng từ văn bản."

**Prompt có cấu trúc**
- Role: Trích xuất dữ liệu
- Instruction: Lấy các trường được chỉ định
- Context: Văn bản
- Constraint: Nếu thiếu trả về null, không tưởng tượng

**Nhận xét**
Prompt có cấu trúc giảm nguy cơ "tưởng tượng" và bảo toàn các trường bắt buộc.

## Kết luận
Prompt có cấu trúc cho hiệu quả vượt trội trong môi trường ứng dụng thực tế, đặc biệt khi cần JSON output để tự động hóa. Đề khuyến nghị sử dụng định dạng cấu trúc cho các tác vụ sản xuất (production).
