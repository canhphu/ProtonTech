"""
Day 6: Chatbot Basics - reference implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
import os
import re
from typing import List, Dict, Optional
from urllib import request
from dotenv import load_dotenv


@dataclass
class Chatbot:
    """Simple chatbot memory manager for CLI usage."""

    window_size: int = 20
    summary_trigger_tokens: int = 800
    token_warning_threshold: int = 1000
    history: List[Dict[str, str]] = field(default_factory=list)
    summary: Optional[str] = None

    def add_message(self, role: str, content: str) -> None:
        self.history.append({"role": role, "content": content})
        self._apply_sliding_window()
        self._summarize_if_needed()

    def get_context(self) -> str:
        """Return a combined context string (summary + recent messages)."""
        parts: List[str] = []
        if self.summary:
            parts.append("[Summary of earlier conversation]\n" + self.summary)
        for msg in self.history:
            parts.append(f"{msg['role']}: {msg['content']}")
        return "\n".join(parts)

    def count_tokens(self) -> int:
        """Approximate token count using word-like segments."""
        text = self.get_context()
        return len(re.findall(r"\w+", text))

    def token_warning(self) -> Optional[str]:
        tokens = self.count_tokens()
        if tokens >= self.token_warning_threshold:
            return (
                f"Warning: context is large ({tokens} tokens). "
                "Consider summarizing or trimming history."
            )
        return None

    def _apply_sliding_window(self) -> None:
        """Keep only the most recent N messages."""
        if len(self.history) > self.window_size:
            self.history = self.history[-self.window_size :]

    def _summarize_if_needed(self) -> None:
        """Summarize older conversation if token budget is exceeded."""
        if self.count_tokens() < self.summary_trigger_tokens:
            return

        # Summarize current window into a compact summary and reset history.
        compact = []
        for msg in self.history:
            role = msg["role"].capitalize()
            text = msg["content"].strip().replace("\n", " ")
            compact.append(f"- {role}: {text[:120]}")
        new_summary = "\n".join(compact)

        if self.summary:
            self.summary = self.summary + "\n" + new_summary
        else:
            self.summary = new_summary

        self.history = []


def _load_env() -> None:
    """Load simple KEY=VALUE pairs from .env if present."""
    # Try python-dotenv first (supports parent lookup if given a path).
    env_path = _find_env_path()
    if env_path and os.path.isfile(env_path):
        load_dotenv(env_path)

    if not env_path or not os.path.isfile(env_path):
        return

    with open(env_path, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def _find_env_path() -> Optional[str]:
    """Find a .env file by walking up from this file and cwd."""
    candidates = []
    cwd = os.getcwd()
    file_dir = os.path.dirname(os.path.abspath(__file__))
    for base in {cwd, file_dir}:
        current = base
        for _ in range(5):
            candidates.append(os.path.join(current, ".env"))
            parent = os.path.dirname(current)
            if parent == current:
                break
            current = parent

    for path in candidates:
        if os.path.isfile(path):
            return path
    return None
                
def _generate_reply(bot: Chatbot) -> str:
    """Generate a reply using Gemini if available, otherwise fallback."""
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash").strip()
    if not api_key:
        return "(demo response) I received your message and stored context."

    contents = _build_contents(bot)
    payload = json.dumps({"contents": contents}).encode("utf-8")
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={api_key}"
    )

    req = request.Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")

    try:
        with request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return "(demo response) I received your message and stored context."

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception:
        return "(demo response) I received your message and stored context."


def _build_contents(bot: Chatbot) -> List[Dict[str, object]]:
    """Convert summary and history into Gemini content format."""
    contents: List[Dict[str, object]] = []
    if bot.summary:
        contents.append(
            {
                "role": "user",
                "parts": [{"text": "Context summary:\n" + bot.summary}],
            }
        )

    for msg in bot.history:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})

    return contents

def run_chat() -> None:
    _load_env()
    bot = Chatbot()
    print("Chatbot CLI. Type 'exit' to quit.")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break

        bot.add_message("user", user_input)

        reply = _generate_reply(bot)
        bot.add_message("assistant", reply)
        print("Bot:", reply)

        warning = bot.token_warning()
        if warning:
            print(warning)


if __name__ == "__main__":
    run_chat()