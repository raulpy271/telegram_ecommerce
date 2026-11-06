import os
from importlib import import_module
import unittest
from hashlib import sha256
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

os.environ.setdefault("BOT_TOKEN", "test-token")
for name in ("DB_USER", "DB_PASSWORD", "DB_HOST", "DB_NAME"):
    os.environ.setdefault(name, "test")

from telegram_ecommerce.utils.utils import hash_password, verify_password
register_module = import_module("telegram_ecommerce.handlers.register")
query_module = import_module("telegram_ecommerce.database.query")
manipulation_module = import_module("telegram_ecommerce.database.manipulation")
from telegram_ecommerce.handlers.register import (
    PIN_KEY, PATTERN_TO_CATCH_THE_DIGITS, PATTERN_TO_CATCH_THE_RESPONSE_TO_SAVE_THE_PASSWORD,
    register_callback_query_number_in_numeric_keyboard, register_callback_query_step_3,
    register_callback_query_step_4,
)


class PasswordHashTests(unittest.TestCase):
    def test_salted_hashes_and_wrong_password(self):
        first = hash_password("1234")
        second = hash_password("1234")
        self.assertNotEqual(first, second)
        self.assertLessEqual(len(first), 255)
        self.assertEqual(verify_password("1234", first), (True, False))
        self.assertEqual(verify_password("wrong", first), (False, False))
        self.assertEqual(verify_password("1234", "pbkdf2_sha256$999999999$bad$bad"), (False, False))

    def test_legacy_sha256_can_be_upgraded_after_successful_check(self):
        legacy = sha256(b"1234").hexdigest()
        self.assertEqual(verify_password("1234", legacy), (True, True))
        self.assertEqual(verify_password("wrong", legacy), (False, False))



    def test_check_password_rehashes_legacy_value(self):
        user = SimpleNamespace(password_hash=sha256(b"1234").hexdigest())
        class FakeSession:
            committed = False
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
            def get(self, model, user_id):
                return user if user_id == 1 else None
            def commit(self):
                self.committed = True
        session = FakeSession()
        with patch.object(query_module, "Session", return_value=session):
            self.assertFalse(query_module.check_password(1, "wrong"))
            self.assertFalse(session.committed)
            self.assertTrue(query_module.check_password(1, "1234"))
            self.assertTrue(session.committed)
            self.assertEqual(verify_password("1234", user.password_hash), (True, False))
            self.assertFalse(query_module.check_password(2, "1234"))



    def test_create_account_stores_hash_and_handles_missing_username(self):
        class FakeSession:
            customer = None
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
            def add(self, customer):
                self.customer = customer
            def commit(self):
                pass
        session = FakeSession()
        with patch.object(manipulation_module, "Session", return_value=session):
            manipulation_module.create_account(SimpleNamespace(id=123, username=None), "123456")
        self.assertEqual(session.customer.username, "123")
        self.assertNotEqual(session.customer.password_hash, "123456")
        self.assertEqual(verify_password("123456", session.customer.password_hash), (True, False))


class RegistrationTests(unittest.IsolatedAsyncioTestCase):
    async def test_digits_are_masked_and_only_final_hash_is_stored(self):
        context = SimpleNamespace(user_data={PIN_KEY: ""})
        query = SimpleNamespace(
            data=PATTERN_TO_CATCH_THE_DIGITS + "digit_1",
            from_user=SimpleNamespace(id=1, username=None),
            edit_message_text=AsyncMock(),
        )
        update = SimpleNamespace(callback_query=query, message=None)
        with patch.object(register_module, "create_account") as create_account:
            await register_callback_query_number_in_numeric_keyboard(update, context)
            self.assertEqual(context.user_data[PIN_KEY], "1")
            self.assertIn("•", query.edit_message_text.call_args.args[0])
            self.assertNotIn("1", query.edit_message_text.call_args.args[0])
            create_account.assert_not_called()
            context.user_data[PIN_KEY] = "123456"
            query.data = PATTERN_TO_CATCH_THE_DIGITS + "end_numeric_keyboard"
            await register_callback_query_step_3(update, context)
            self.assertNotIn("123456", query.edit_message_text.call_args.args[0])
            query.data = PATTERN_TO_CATCH_THE_RESPONSE_TO_SAVE_THE_PASSWORD + "end_login_process"
            with patch.object(register_module, "user_exist", return_value=False):
                await register_callback_query_step_4(update, context)
            create_account.assert_called_once_with(query.from_user, "123456")
            self.assertNotIn(PIN_KEY, context.user_data)
            self.assertNotIn("123456", query.edit_message_text.call_args.args[0])

    async def test_too_short_pin_is_rejected(self):
        context = SimpleNamespace(user_data={PIN_KEY: "12"})
        query = SimpleNamespace(
            data=PATTERN_TO_CATCH_THE_DIGITS + "end_numeric_keyboard",
            edit_message_text=AsyncMock(),
        )
        update = SimpleNamespace(callback_query=query)
        result = await register_callback_query_step_3(update, context)
        self.assertEqual(result, 1)
        self.assertEqual(context.user_data[PIN_KEY], "12")


if __name__ == "__main__":
    unittest.main()
