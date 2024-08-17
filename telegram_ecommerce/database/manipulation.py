
from telegram_ecommerce.database import models
from telegram_ecommerce.database.models import Session
from telegram_ecommerce.utils.utils import hash_password
from telegram_ecommerce.database.query import (
    get_password,
    user_in_credentials_file)


def create_account(user):
    user_id = user.id
    username = user.username
    user_is_admin = user_in_credentials_file(username)
    with Session() as session:
        session.add(models.Customer(id=user_id, username=username, password_hash="", is_admin=user_is_admin))
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

def add_rating_to_an_order(order_id, rating):
    with Session() as session:
        order = session.get(models.Order, order_id)
        order.rating = rating
        session.commit()

