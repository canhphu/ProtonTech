import unittest

from email_summarizer import extract_json, normalize_response


class TestEmailSummarizer(unittest.TestCase):
    def test_extract_json(self) -> None:
        text = '{"summary": "A. B. C.", "action_items": ["Reply"], "priority": "high", "people": ["Alice"]}'
        data = extract_json(text)
        self.assertEqual(data["priority"], "high")

    def test_normalize_response(self) -> None:
        data = {
            "summary": ["One.", "Two.", "Three."],
            "action_items": "Follow up",
            "priority": "High",
            "people": "Bob",
        }
        result = normalize_response(data)
        self.assertEqual(result["priority"], "high")
        self.assertEqual(result["action_items"], ["Follow up"])
        self.assertEqual(result["people"], ["Bob"])


if __name__ == "__main__":
    unittest.main()
