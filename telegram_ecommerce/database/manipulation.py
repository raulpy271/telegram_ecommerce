
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy import select

from telegram_ecommerce.database import models
from telegram_ecommerce.database.models import Session
from telegram_ecommerce.utils.utils import hash_password
from telegram_ecommerce.utils.consts import admins
from telegram_ecommerce.database.query import get_password


def create_account(user):
    user_id = user.id
    username = user.username
    # Telegram usernames can be changed or claimed by another account.
    is_admin = user_id in admins
    with Session() as session:
        session.add(models.Customer(id=user_id, username=username, password_hash="", is_admin=is_admin))
        session.commit()

def delete_account(user_id):
    with Session() as session:
        user = session.get(models.Customer, user_id)
        if user:
            session.delete(user)
            session.commit()
            return True
        else: return False

def set_password(user_id, password):
    with Session() as session:
        user = session.get(models.Customer, user_id)
        user.password_hash = password
        session.commit()

def append_password(user_id, password):
    old_password = get_password(user_id)
    new_password = str(old_password) + str(password)
    set_password(user_id, new_password)


def hash_user_password(user_id):
    password = get_password(user_id)
    password_hash = hash_password(password)
    set_password(user_id, password_hash)


def add_photo(photo_id, bytes_of_photo):
    with Session() as session:
        session.add(models.Photo(id=photo_id, image_blob=bytes_of_photo))
        session.commit()

def add_category(name, description, tags=None, image_id=None):
    with Session() as session:
        session.add(models.Category(name=name, description=description, tags=tags, image_id=image_id))
        session.commit()

def add_product(
        name, 
        description,
        unit_price=0, 
        quantity_in_stock=0, 
        quantity_purchased=0,
        category_id=None, 
        image_id=None):
    with Session() as session:
        session.add(models.Product(
            name=name,
            description=description,
            price=unit_price,
            quantity_in_stock=quantity_in_stock,
            quantity_purchased=quantity_purchased,
            category_id=category_id,
            image_id=image_id
        ))
        session.commit()

def add_orders(order_id, price, user_id, product_id, rating = None):
    with Session() as session:
        session.add(models.Order(id=order_id, price=price, user_id=user_id, product_id=product_id, rating=rating))
        session.commit()

def product_has_purchased(product_id):
    with Session() as session:
        product = session.get(models.Product, product_id)
        product.quantity_in_stock -= 1
        product.quantity_purchased += 1
        session.commit()


def _amount_in_minor_units(amount):
    return int((Decimal(str(amount)) * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def validate_checkout(product_id, user_id, total_amount, currency, expected_currency):
    """Check the current catalog before Telegram charges the customer."""
    with Session() as session:
        product = session.get(models.Product, product_id)
        customer = session.get(models.Customer, user_id)
        return bool(
            customer
            and product
            and product.quantity_in_stock > 0
            and currency == expected_currency
            and _amount_in_minor_units(product.price) == total_amount
        )


def get_product_for_payment(product_id):
    with Session() as session:
        return session.get(models.Product, product_id)


def complete_paid_order(order_id, product_id, user_id, total_amount, currency, expected_currency):
    """Record a Telegram payment once, with an atomic stock change when possible.

    A payment may succeed after stock or price changed. Keep a record of it as
    needs_review so staff can fulfill or refund it rather than losing the charge.
    """
    with Session.begin() as session:
        existing = session.get(models.Order, order_id)
        if existing is not None:
            if existing.user_id != user_id or existing.product_id != product_id:
                raise ValueError("payment identifier conflicts with an existing order")
            return existing.status

        product = session.scalar(
            select(models.Product)
            .where(models.Product.id == product_id)
            .with_for_update()
        )
        if product is None:
            raise ValueError("paid product no longer exists")

        price_matches = (
            currency == expected_currency
            and _amount_in_minor_units(product.price) == total_amount
        )
        has_stock = product.quantity_in_stock > 0
        status = "paid" if price_matches and has_stock else "needs_review"
        if status == "paid":
            product.quantity_in_stock -= 1
            product.quantity_purchased += 1

        session.add(models.Order(
            id=order_id,
            price=Decimal(total_amount) / 100,
            user_id=user_id,
            product_id=product_id,
            status=status,
            paid_at=datetime.now(timezone.utc),
        ))
        return status

def add_rating_to_an_order(order_id, rating):
    with Session() as session:
        order = session.get(models.Order, order_id)
        order.rating = rating
        session.commit()

