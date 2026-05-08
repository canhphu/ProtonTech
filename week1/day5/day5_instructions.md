# Day 5 - Mini Project 1: AI Email Summarizer

## 5.1 Gioi thieu project
- Muc tieu: tom tat email dau vao va tra ve output JSON co cau truc.
- Tieu chi danh gia: dung yeu cau output, prompt ro rang, co xu ly loi, CLI de chay.
- Timeline: sang huong dan + code phan 1, chieu hoan thien + demo.

## 5.2 Thiet ke
- Input: email text (file hoac stdin).
- Output: JSON gom `summary`, `action_items`, `priority`, `people`.
- Prompt strategy: he thong + nguoi dung, rang buoc output JSON, nhan manh 3-5 cau.
- Error cases: thieu API key, file khong ton tai, response khong phai JSON.

## 5.3 Code - Phan 1
- Doc email input, xay dung prompt, goi API.
- File chinh: [week1/day5/email_summarizer.py](week1/day5/email_summarizer.py)

## 5.4 Code - Phan 2
- Xu ly response, structured output, error handling.
- Kiem tra du lieu tra ve va normalize.

## 5.5 Code - Phan 3
- CLI interface, test voi nhieu loai email.
- Vi du input: [week1/day5/samples/email_1.txt](week1/day5/samples/email_1.txt), [week1/day5/samples/email_2.txt](week1/day5/samples/email_2.txt)

## 5.6 README
- Huong dan cai dat, cau hinh `.env`, cach chay.
- File: [week1/day5/README.md](week1/day5/README.md)

## 5.7 Demo
- Trinh bay 3 phut: input -> output, giai thich prompt, error handling.

## San pham cuoi ngay
- AI Email Summarizer hoan chinh.
- Output JSON co cau truc.
- Co error handling co ban.
- Repo GitHub co README day du.
