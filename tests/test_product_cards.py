import os
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock

os.environ.setdefault("BOT_TOKEN", "test-token")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_USER", "test")
os.environ.setdefault("DB_PASSWORD", "test")
os.environ.setdefault("DB_NAME", "test")

from telegram_ecommerce.tamplates.products import send_product_card


class ProductCardTests(unittest.IsolatedAsyncioTestCase):
    async def test_first_product_without_photo_is_text(self):
        message = SimpleNamespace(reply_text=AsyncMock(), reply_photo=AsyncMock())
        update = SimpleNamespace(effective_message=message, callback_query=None)
        await send_product_card(update, SimpleNamespace(image_id=None), "Demo Notebook", None)
        message.reply_text.assert_awaited_once_with("Demo Notebook", reply_markup=None)
        message.reply_photo.assert_not_awaited()

    async def test_switching_from_photo_to_text_removes_previous_buttons(self):
        message = SimpleNamespace(photo=[object()], edit_reply_markup=AsyncMock(), reply_text=AsyncMock())
        query = SimpleNamespace(answer=AsyncMock())
        update = SimpleNamespace(effective_message=message, callback_query=query)
        await send_product_card(update, SimpleNamespace(image_id=None), "Demo Pen", None)
        query.answer.assert_awaited_once()
        message.edit_reply_markup.assert_awaited_once_with(reply_markup=None)
        message.reply_text.assert_awaited_once_with("Demo Pen", reply_markup=None)

    async def test_revisiting_same_text_card_does_not_send_invalid_edit(self):
        message = SimpleNamespace(photo=[], text="Demo Pen", reply_markup=None, edit_text=AsyncMock())
        query = SimpleNamespace(answer=AsyncMock())
        update = SimpleNamespace(effective_message=message, callback_query=query)
        await send_product_card(update, SimpleNamespace(image_id=None), "Demo Pen", None)
        message.edit_text.assert_not_awaited()
