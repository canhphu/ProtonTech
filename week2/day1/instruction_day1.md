# Huong dan su dung - Ngay 6 (Chatbot Basics)

## Muc tieu
Chay chatbot qua terminal, co co che luu lich su, sliding window, tom tat context, va canh bao token.

## Chay demo
1. Mo terminal tai thu muc week2/day1
2. Chay lenh:

```bash
python chatbot.py
```

3. Goi tin nhan, chatbot se tra loi mau va luu lich su.
4. Go `exit` de thoat.

## Mo ta hanh vi
- Luu lich su hoi thoai theo danh sach message (role + content).
- Sliding window: chi giu 20 message gan nhat.
- Tom tat context: khi vuot nguong, chatbot se tom tat lich su va reset window.
- Token warning: canh bao neu context gan gioi han.

## Cau hinh nhanh
Ban co the sua trong class `Chatbot`:
- `window_size`: so message gan nhat duoc giu.
- `summary_trigger_tokens`: nguong kich hoat tom tat.
- `token_warning_threshold`: nguong canh bao.
