# Hướng dẫn 3.11 và 3.12

## 3.11. Guardrails cơ bản (validation)
File [week1/day3/guardrails.py](week1/day3/guardrails.py) cung cấp các hàm:
- validate_json_output(text, required_keys): kiểm tra JSON hợp lệ và đầy đủ trường bắt buộc.
- check_length(text, min_chars, max_chars): kiểm tra độ dài output.
- filter_content(text, banned_phrases): lọc nội dung cấm (từ khóa/chuỗi).

### Ví dụ sử dụng
```python
from week1.day3.guardrails import (
    validate_json_output,
    check_length,
    filter_content,
)

text = '{"label": "billing", "confidence": 0.92}'
result, data = validate_json_output(text, ["label", "confidence"])
print(result.ok, result.reason, data)

print(check_length(text, max_chars=200))
print(filter_content(text, ["password", "credit card"]))
```

## 3.12. Pipeline prompt -> call -> validate -> retry
Mục tiêu: Nếu output không đạt, hệ thống sẽ tự retry tới khi hợp lệ hoặc hết số lần thử.

### Các bước
1. Tạo prompt rõ ràng.
2. Gọi hàm LLM (mock hoặc API).
3. Chạy các validator.
4. Nếu fail, retry đến khi pass hoặc vượt max_retries.

### Ví dụ pipeline
```python
from week1.day3.guardrails import (
    run_with_retry,
    check_length,
    filter_content,
    ValidationResult,
)


def fake_llm_call(prompt: str) -> str:
    return "Tra loi mau cho prompt: " + prompt


def not_empty(text: str) -> ValidationResult:
    return check_length(text, min_chars=10)

prompt = "Hay tom tat doan van sau trong 100 tu."
validators = [
    not_empty,
    lambda t: filter_content(t, ["password", "credit card"]),
]

output, attempts, errors = run_with_retry(
    prompt=prompt,
    llm_call=fake_llm_call,
    validators=validators,
    max_retries=2,
)

print(output)
print("attempts:", attempts)
print("errors:", errors)
```

### Ví dụ gọi Gemini API trong pipeline
```python
import os

import google.generativeai as genai

from week1.day3.guardrails import (
    run_with_retry,
    check_length,
    filter_content,
    ValidationResult,
)


def gemini_llm_call(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY in environment")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text or ""


def not_empty(text: str) -> ValidationResult:
    return check_length(text, min_chars=10)


prompt = "Hãy tóm tắt đoạn văn sau trong 100 từ."
validators = [
    not_empty,
    lambda t: filter_content(t, ["password", "credit card"]),
]

output, attempts, errors = run_with_retry(
    prompt=prompt,
    llm_call=gemini_llm_call,
    validators=validators,
    max_retries=2,
)

print(output)
print("attempts:", attempts)
print("errors:", errors)
```

### Lưu ý khi dùng Gemini
- Cài thư viện: `pip install google-generativeai`.
- Nếu bạn đang dùng biến môi trường khác trong .env, hãy đổi `GEMINI_API_KEY` cho đúng tên.

### Ghi chú
- Với JSON output, nên dùng validate_json_output trong danh sách validators.
- Nếu dùng API LLM thật, thay fake_llm_call bằng hàm gọi API thực tế.
- Nên lưu log lỗi để phân tích các lần retry thất bại.
