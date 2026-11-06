"""Focused checks for payment recording and admin command authorization."""

import os
import unittest
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

os.environ.setdefault("DB_USER", "test")
os.environ.setdefault("DB_PASSWORD", "test")
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_NAME", "test")
os.environ.setdefault("BOT_TOKEN", "123:test")

from telegram_ecommerce.database import manipulation
from telegram_ecommerce.filters.decorators import execute_if_admin


Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    price = Column(Numeric(12, 2), nullable=False)
    quantity_in_stock = Column(Integer, nullable=False)
    quantity_purchased = Column(Integer, nullable=False)


class Order(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True)
    price = Column(Numeric(12, 2), nullable=False)
    user_id = Column(ForeignKey("customers.id"), nullable=False)
    product_id = Column(ForeignKey("products.id"), nullable=False)
    status = Column(String, nullable=False)
    paid_at = Column(DateTime(timezone=True))


class PaymentTests(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite+pysqlite:///:memory:")
        Base.metadata.create_all(engine)
        self.session_factory = sessionmaker(engine)
        self.session_patch = patch.object(manipulation, "Session", self.session_factory)
        self.models_patch = patch.object(
            manipulation, "models", SimpleNamespace(Customer=Customer, Product=Product, Order=Order)
        )
        self.session_patch.start()
        self.models_patch.start()
        with self.session_factory.begin() as session:
            session.add(Customer(id=7))
            session.add(Product(id=3, price=Decimal("12.50"), quantity_in_stock=1, quantity_purchased=0))
        self.addCleanup(self.session_patch.stop)
        self.addCleanup(self.models_patch.stop)
        self.addCleanup(engine.dispose)

    def test_checkout_checks_price_currency_stock_and_customer(self):
        self.assertTrue(manipulation.validate_checkout(3, 7, 1250, "USD", "USD"))
        self.assertFalse(manipulation.validate_checkout(3, 7, 1300, "USD", "USD"))
        self.assertFalse(manipulation.validate_checkout(3, 7, 1250, "EUR", "USD"))
        self.assertFalse(manipulation.validate_checkout(3, 8, 1250, "USD", "USD"))

    def test_paid_callback_is_idempotent_and_oversold_payment_is_recorded(self):
        complete = manipulation.complete_paid_order
        self.assertEqual(complete("charge-1", 3, 7, 1250, "USD", "USD"), "paid")
        self.assertEqual(complete("charge-1", 3, 7, 1250, "USD", "USD"), "paid")
        self.assertEqual(complete("charge-2", 3, 7, 1250, "USD", "USD"), "needs_review")
        with self.session_factory() as session:
            product = session.get(Product, 3)
            self.assertEqual(product.quantity_in_stock, 0)
            self.assertEqual(product.quantity_purchased, 1)
            self.assertEqual(session.query(Order).count(), 2)


class AuthorizationTests(unittest.IsolatedAsyncioTestCase):
    async def test_non_admin_cannot_enter_admin_flow(self):
        handler = AsyncMock(return_value=42)
        message = SimpleNamespace(reply_text=AsyncMock())
        update = SimpleNamespace(effective_user=SimpleNamespace(id=9), effective_message=message)
        with patch("telegram_ecommerce.filters.decorators.admins", set()), patch(
            "telegram_ecommerce.filters.decorators.user_exist", return_value=True
        ):
            result = await execute_if_admin(handler)(update, SimpleNamespace(user_data={}))
        self.assertEqual(result, -1)
        handler.assert_not_awaited()
        message.reply_text.assert_awaited_once()

    async def test_configured_registered_admin_can_enter_flow(self):
        handler = AsyncMock(return_value=42)
        message = SimpleNamespace(reply_text=AsyncMock())
        update = SimpleNamespace(effective_user=SimpleNamespace(id=9), effective_message=message)
        with patch("telegram_ecommerce.filters.decorators.admins", {9}), patch(
            "telegram_ecommerce.filters.decorators.user_exist", return_value=True
        ):
            result = await execute_if_admin(handler)(update, SimpleNamespace(user_data={}))
        self.assertEqual(result, 42)
        handler.assert_awaited_once()
        message.reply_text.assert_not_awaited()


if __name__ == "__main__":
    unittest.main()
