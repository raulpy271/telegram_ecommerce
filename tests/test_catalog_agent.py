import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

os.environ.setdefault("BOT_TOKEN", "test-token")

from telegram_ecommerce.agent.catalog import (
    answer_catalog_question,
    execute_catalog_tool,
)


class FakeResponses:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.requests = []

    async def create(self, **kwargs):
        self.requests.append(kwargs)
        return next(self.responses)


def fake_response(identifier, output, text=""):
    return SimpleNamespace(id=identifier, output=output, output_text=text)


class CatalogAgentTests(unittest.IsolatedAsyncioTestCase):
    async def test_returns_answer_after_tool_result(self):
        responses = FakeResponses([
            fake_response("r1", [SimpleNamespace(
                type="function_call", name="list_categories", arguments="{}",
                call_id="c1")]),
            fake_response("r2", [], "We have books. Browse with /show_categories."),
        ])
        with patch("telegram_ecommerce.agent.catalog.execute_catalog_tool",
                   return_value={"categories": ["books"]}) as tool:
            answer = await answer_catalog_question(
                "What do you sell?", client=SimpleNamespace(responses=responses))
        self.assertIn("books", answer)
        tool.assert_called_once_with("list_categories", {})
        self.assertEqual(responses.requests[1]["previous_response_id"], "r1")
        self.assertEqual(responses.requests[1]["input"][0]["call_id"], "c1")

    async def test_rejects_oversized_message_before_api_call(self):
        with self.assertRaises(ValueError):
            await answer_catalog_question("x" * 1001, client=object())

    async def test_bounds_tool_rounds(self):
        calls = [SimpleNamespace(type="function_call", name="list_categories",
                                 arguments="{}", call_id=f"c{i}") for i in range(3)]
        responses = FakeResponses([
            fake_response("r1", calls), fake_response("r2", calls),
        ])
        with patch("telegram_ecommerce.agent.catalog.execute_catalog_tool",
                   return_value={"categories": []}):
            with self.assertRaisesRegex(RuntimeError, "tool budget"):
                await answer_catalog_question(
                    "Categories?", client=SimpleNamespace(responses=responses))


class CatalogToolTests(unittest.TestCase):
    def test_refuses_unlisted_actions(self):
        with self.assertRaises(ValueError):
            execute_catalog_tool("purchase_product", {"product_id": 1})


if __name__ == "__main__":
    unittest.main()
