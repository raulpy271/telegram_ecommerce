
from sqlalchemy import select
from sqlalchemy.dialects.mysql import match

from telegram_ecommerce.database.db_wrapper import db
from telegram_ecommerce.utils.consts import credentials
from telegram_ecommerce.database import models
from telegram_ecommerce.database.models import Session
from telegram_ecommerce.utils.utils import (
    write_file,
    extract_value_from_a_query,
    hash_password)


def user_exist(user_id):
    with Session() as session:
        return bool(session.get(models.Customer, user_id))

def is_admin(user_id):
    with Session() as session:
        user = session.get(models.Customer, user_id)
        return user.is_admin if user else False

def get_password(user_id):
    with Session() as session:
        user = session.get(models.Customer, user_id)
        return user.password_hash

def check_password(user_id, password):
    return hash_password(password) == get_password(user_id)


def user_in_credentials_file(username):
    admins = credentials["admins_username"]
    return username in admins


def extract_blob(photo_id):
    command = "SELECT image_blob FROM photo WHERE id = %s"
    blob = bytes(
        extract_value_from_a_query(
        db.execute_a_query(command, (photo_id,)))
        )
    return blob


def save_photo_in_file(photo_id, file_path):
    blob = extract_blob(photo_id)
    write_file(blob, file_path)


def get_name_of_all_categories():
    with Session() as session:
        return session.scalars(select(models.Category.name)).all()

def get_category_id_from_name(name):
    with Session() as session:
        stmt = select(models.Category.id).where(models.Category.name == name)
        return session.scalars(stmt).first()


def get_all_available_by_category_id(category_id):
    command = """ SELECT * FROM products 
        WHERE category_id = %s AND quantity_in_stock > 0"""
    products_with_category_id = db.execute_a_query(
        command, (category_id,))
    return products_with_category_id


def get_all_available_by_category_name(name):
    category_id = get_category_id_from_name(name)
    return get_all_available_by_category_id(category_id)


def get_quantity_in_stock(product_id):
    command = "SELECT quantity_in_stock FROM products WHERE id = %s"
    quantity_in_stock = db.execute_a_query(command, (product_id,))
    return extract_value_from_a_query(quantity_in_stock)


def get_quantity_purchased(product_id):
    command = "SELECT quantity_purchased FROM products WHERE id = %s"
    quantity_purchased = db.execute_a_query(command, (product_id,))
    return extract_value_from_a_query(quantity_purchased)


def get_ratings_of_a_product(product_id):
    with Session() as session:
        stmt = (
            select(models.Order.rating)
            .where(models.Order.product_id == product_id)
            .where(models.Order.rating != None)
        )
        return session.scalars(stmt).all()

def count_occurrence_of_specified_rating(product_id, rating):
    all_ratings = get_ratings_of_a_product(product_id)
    return all_ratings.count(rating)

def search_products(string_to_search):
    with Session() as session:
        stmt = select(models.Product).where(
            match(models.Product.name, models.Product.description, against=string_to_search)
        )
        return session.scalars(stmt).all()

