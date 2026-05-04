# test_setup.py
import os
from dotenv import load_dotenv

load_dotenv()

# Test OpenAI
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello"}],
    max_tokens=10
)
print(f"OpenAI OK: {response.choices[0].message.content}")

# Test Anthropic
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=10,
    messages=[{"role": "user", "content": "Hello"}]
)
print(f"Anthropic OK: {response.content[0].text}")