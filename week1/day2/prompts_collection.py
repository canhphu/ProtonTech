import json
from typing import Any, Dict, Iterable, List, Optional


def build_prompt(
	role: str,
	instruction: str,
	context: str,
	constraints: Iterable[str],
	output_format: Optional[str] = None,
) -> str:
	"""Render a structured prompt with clear sections."""
	parts = [
		f"Role: {role}",
		f"Instruction: {instruction}",
		f"Context: {context}",
		"Constraints:",
	]
	parts.extend([f"- {c}" for c in constraints])
	if output_format:
		parts.append("Output Format:")
		parts.append(output_format)
	return "\n".join(parts)


def json_only_constraints() -> List[str]:
	return [
		"Return valid JSON only.",
		"Do not wrap the JSON in markdown or code fences.",
		"Use double quotes for all JSON keys and string values.",
	]


def validate_json_response(response_text: str, required_keys: Iterable[str]) -> Dict[str, Any]:
	"""Parse JSON response and ensure required keys exist."""
	data = json.loads(response_text)
	missing = [k for k in required_keys if k not in data]
	if missing:
		raise KeyError(f"Missing keys: {', '.join(missing)}")
	return data


def prompt_summarize(text: str, max_words: int = 120, style: str = "bullet") -> str:
	role = "You are a concise summarization assistant."
	instruction = "Summarize the input text with the requested style."
	context = f"Text to summarize:\n{text}"
	constraints = [
		f"Maximum {max_words} words.",
		f"Style: {style}.",
		"Keep key facts and omit minor details.",
	]
	return build_prompt(role, instruction, context, constraints)


def prompt_classify_email(email_text: str, labels: Iterable[str]) -> str:
	role = "You are an email triage classifier."
	instruction = "Classify the email into exactly one label."
	context = f"Email:\n{email_text}"
	constraints = [
		f"Labels: {', '.join(labels)}.",
		"Choose the best single label.",
	]
	output_format = "JSON object with keys: label, confidence (0-1), rationale."
	return build_prompt(role, instruction, context, constraints + json_only_constraints(), output_format)


def prompt_extract_fields(text: str, fields: Iterable[str]) -> str:
	role = "You extract structured fields from text."
	instruction = "Extract the requested fields with best-effort values."
	context = f"Input text:\n{text}"
	constraints = [
		"If a field is missing, set its value to null.",
		"Do not invent facts that are not in the text.",
		f"Fields: {', '.join(fields)}.",
	]
	output_format = "JSON object with exactly the requested fields."
	return build_prompt(role, instruction, context, constraints + json_only_constraints(), output_format)


def prompt_translate(text: str, source_lang: str, target_lang: str) -> str:
	role = "You are a professional translator."
	instruction = "Translate the text accurately and naturally."
	context = f"Source ({source_lang}) text:\n{text}"
	constraints = [
		f"Translate to {target_lang}.",
		"Preserve proper nouns and numbers.",
		"Keep original formatting where possible.",
	]
	return build_prompt(role, instruction, context, constraints)


def prompt_generate_content(product: str, audience: str, tone: str, length: str) -> str:
	role = "You are a marketing copywriter."
	instruction = "Create persuasive content for the product."
	context = f"Product: {product}\nAudience: {audience}"
	constraints = [
		f"Tone: {tone}.",
		f"Length: {length}.",
		"Include a clear call-to-action.",
	]
	return build_prompt(role, instruction, context, constraints)


def prompt_sentiment(text: str) -> str:
	role = "You are a sentiment analysis model."
	instruction = "Classify sentiment and provide a brief reason."
	context = f"Text:\n{text}"
	constraints = [
		"Sentiment must be one of: positive, neutral, negative.",
	]
	output_format = "JSON object with keys: sentiment, confidence (0-1), reason."
	return build_prompt(role, instruction, context, constraints + json_only_constraints(), output_format)


def prompt_intent(text: str, intents: Iterable[str]) -> str:
	role = "You are an intent classification assistant."
	instruction = "Pick the most likely intent."
	context = f"User message:\n{text}"
	constraints = [
		f"Intents: {', '.join(intents)}.",
		"Pick exactly one intent.",
	]
	output_format = "JSON object with keys: intent, confidence (0-1), rationale."
	return build_prompt(role, instruction, context, constraints + json_only_constraints(), output_format)


def prompt_faq(text: str, max_questions: int = 5) -> str:
	role = "You generate FAQs from product or policy text."
	instruction = "Create concise Q&A pairs that cover key topics."
	context = f"Source text:\n{text}"
	constraints = [
		f"Create up to {max_questions} questions.",
		"Answers must be grounded in the text.",
	]
	output_format = "JSON object with key: faqs (array of {question, answer})."
	return build_prompt(role, instruction, context, constraints + json_only_constraints(), output_format)


def prompt_rewrite(text: str, goal: str, constraints_list: Iterable[str]) -> str:
	role = "You are a rewriting assistant."
	instruction = "Rewrite the text to meet the goal."
	context = f"Original text:\n{text}"
	constraints = [f"Goal: {goal}."] + list(constraints_list)
	return build_prompt(role, instruction, context, constraints)


def prompt_keywords(text: str, max_keywords: int = 8) -> str:
	role = "You extract keywords from text."
	instruction = "Return the most relevant keywords and phrases."
	context = f"Text:\n{text}"
	constraints = [
		f"Return up to {max_keywords} keywords.",
		"Prefer noun phrases when possible.",
	]
	output_format = "JSON object with key: keywords (array of strings)."
	return build_prompt(role, instruction, context, constraints + json_only_constraints(), output_format)


__all__ = [
	"build_prompt",
	"json_only_constraints",
	"validate_json_response",
	"prompt_summarize",
	"prompt_classify_email",
	"prompt_extract_fields",
	"prompt_translate",
	"prompt_generate_content",
	"prompt_sentiment",
	"prompt_intent",
	"prompt_faq",
	"prompt_rewrite",
	"prompt_keywords",
]
