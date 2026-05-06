import json
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple


@dataclass
class ValidationResult:
    ok: bool
    reason: str = ""


def validate_json_output(text: str, required_keys: Iterable[str]) -> Tuple[ValidationResult, Optional[Dict[str, Any]]]:
    """Validate JSON text and required keys."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return ValidationResult(False, f"Invalid JSON: {exc}"), None

    missing = [key for key in required_keys if key not in data]
    if missing:
        return ValidationResult(False, f"Missing keys: {', '.join(missing)}"), data

    return ValidationResult(True, ""), data


def check_length(text: str, min_chars: int = 0, max_chars: Optional[int] = None) -> ValidationResult:
    """Check output length in characters."""
    if len(text) < min_chars:
        return ValidationResult(False, "Output is shorter than minimum length")
    if max_chars is not None and len(text) > max_chars:
        return ValidationResult(False, "Output exceeds maximum length")
    return ValidationResult(True, "")


def filter_content(text: str, banned_phrases: Iterable[str]) -> ValidationResult:
    """Block outputs that contain banned phrases."""
    lowered = text.lower()
    for phrase in banned_phrases:
        if phrase.lower() in lowered:
            return ValidationResult(False, f"Blocked phrase detected: {phrase}")
    return ValidationResult(True, "")


def run_with_retry(
    prompt: str,
    llm_call: Callable[[str], str],
    validators: Iterable[Callable[[str], ValidationResult]],
    max_retries: int = 2,
) -> Tuple[str, int, List[str]]:
    """Run prompt through LLM, validate, and retry on failure."""
    errors: List[str] = []
    attempt = 0
    while True:
        attempt += 1
        output = llm_call(prompt)
        failed = False
        for validator in validators:
            result = validator(output)
            if not result.ok:
                errors.append(result.reason)
                failed = True
                break
        if not failed or attempt > max_retries:
            return output, attempt, errors
