import os
import dotenv 
import google.generativeai as genai

dotenv.load_dotenv()

from guardrails import (
    run_with_retry,
    check_length,
    filter_content,
    ValidationResult,
)


def select_generate_content_model(preferred: str) -> str:
    if preferred:
        return preferred

    available = []
    for model in genai.list_models():
        if "generateContent" in getattr(model, "supported_generation_methods", []):
            available.append(model.name)

    if not available:
        raise RuntimeError("No generateContent-compatible models available")

    for name in available:
        if "gemini-1.5" in name:
            return name

    return available[0]


def gemini_llm_call(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY in environment")

    genai.configure(api_key=api_key)
    preferred = os.getenv("GEMINI_MODEL", "")
    model_name = select_generate_content_model(preferred)
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text or ""


def not_empty(text: str) -> ValidationResult:
    return check_length(text, min_chars=10)


paragraph = input("Enter a paragraph to summarize: ").strip()
prompt = "Summarize the following paragraph in 100 words:\n\n" + paragraph
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

print("Result:\n", output)
print("attempts:", attempts)
print("errors:", errors)