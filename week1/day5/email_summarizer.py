import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass

import requests

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

ALLOWED_PRIORITY = {"low", "medium", "high"}


class SummarizerError(Exception):
    pass


def read_email_input(args: argparse.Namespace) -> str:
    if args.input and args.text:
        raise SummarizerError("Use --input or --text, not both.")

    if args.input:
        if not os.path.exists(args.input):
            raise SummarizerError(f"Input file not found: {args.input}")
        with open(args.input, "r", encoding="utf-8") as handle:
            return handle.read().strip()

    if args.text:
        return args.text.strip()

    if not sys.stdin.isatty():
        return sys.stdin.read().strip()

    raise SummarizerError("No input provided. Use --input, --text, or stdin.")


def build_messages(email_text: str) -> Dict[str, str]:
    system_prompt = (
        "You are an assistant that summarizes emails. "
        "Return ONLY valid JSON with keys: summary, action_items, priority, people. "
        "Summary must be 3-5 sentences. "
        "priority must be one of: low, medium, high. "
        "action_items and people are arrays of strings."
    )
    user_prompt = f"Email:\n{email_text}"
    return {"system": system_prompt, "user": user_prompt}


def call_gemini(
    messages: Dict[str, str],
    model: str,
    temperature: float,
    max_tokens: int,
    timeout: int,
) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise SummarizerError("Missing GEMINI_API_KEY. Set it in .env or env vars.")

    payload = {
        "system_instruction": {"parts": [{"text": messages["system"]}]},
        "contents": [
            {
                "role": "user",
                "parts": [{"text": messages["user"]}],
            }
        ],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": max_tokens,
        },
    }

    response = requests.post(
        API_URL.format(model=model),
        params={"key": api_key},
        json=payload,
        timeout=timeout,
    )
    if response.status_code != 200:
        raise SummarizerError(
            f"API error {response.status_code}: {response.text.strip()}"
        )

    data = response.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError) as exc:
        raise SummarizerError("Unexpected API response format.") from exc


def extract_json(text: str) -> Dict[str, Any]:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    for match in re.finditer(r"\{.*\}", text, re.DOTALL):
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            continue

    raise SummarizerError("Response is not valid JSON.")


def normalize_response(data: Dict[str, Any]) -> Dict[str, Any]:
    summary = data.get("summary", "")
    if isinstance(summary, list):
        summary = " ".join([str(item).strip() for item in summary if str(item).strip()])
    summary = str(summary).strip()

    action_items = data.get("action_items", [])
    if not isinstance(action_items, list):
        action_items = [str(action_items)]
    action_items = [str(item).strip() for item in action_items if str(item).strip()]

    people = data.get("people", [])
    if not isinstance(people, list):
        people = [str(people)]
    people = [str(item).strip() for item in people if str(item).strip()]

    priority = str(data.get("priority", "medium")).strip().lower()
    if priority not in ALLOWED_PRIORITY:
        priority = "medium"

    return {
        "summary": summary,
        "action_items": action_items,
        "priority": priority,
        "people": people,
    }


def write_output(result: Dict[str, Any], output_path: str | None) -> None:
    payload = json.dumps(result, indent=2, ensure_ascii=False)
    if output_path:
        with open(output_path, "w", encoding="utf-8") as handle:
            handle.write(payload + "\n")
        return
    print(payload)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI Email Summarizer")
    parser.add_argument("--input", help="Path to email text file")
    parser.add_argument("--text", help="Raw email text")
    parser.add_argument("--output", help="Path to output JSON file")
    parser.add_argument(
        "--model", default=os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    )
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-tokens", type=int, default=500)
    parser.add_argument("--timeout", type=int, default=30)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        email_text = read_email_input(args)
        if not email_text:
            raise SummarizerError("Email text is empty.")

        messages = build_messages(email_text)
        raw_response = call_gemini(
            messages=messages,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            timeout=args.timeout,
        )
        parsed = extract_json(raw_response)
        normalized = normalize_response(parsed)
        write_output(normalized, args.output)
        return 0
    except SummarizerError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
