"""Integration checks for the PostgreSQL schema and catalog queries.

Set DATABASE_URL to an expendable PostgreSQL database before running these tests.
"""

import os

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import inspect, text
from sqlalchemy.exc import IntegrityError

pytestmark = pytest.mark.skipif(
    not os.environ.get('TEST_DATABASE_URL'),
    reason='Set TEST_DATABASE_URL to an expendable PostgreSQL database',
)


@pytest.fixture(scope='module')
def database():
    os.environ['DATABASE_URL'] = os.environ['TEST_DATABASE_URL']
    from telegram_ecommerce.database.models import engine

    command.upgrade(Config('alembic.ini'), 'head')
    yield engine
    engine.dispose()


@pytest.fixture(autouse=True)
def empty_tables(database):
    with database.begin() as connection:
        connection.execute(text('TRUNCATE orders, products, category, photo, customers RESTART IDENTITY CASCADE'))


def test_migration_creates_search_index_and_payment_fields(database):
    inspector = inspect(database)
    assert {'ix_products_search', 'ix_products_category_id'} <= {
        index['name'] for index in inspector.get_indexes('products')
    }
    columns = {column['name']: column for column in inspector.get_columns('orders')}
    assert columns['status']['nullable'] is False
    assert 'paid_at' in columns
    with database.connect() as connection:
        assert connection.scalar(text('SELECT version_num FROM alembic_version')) == '8e7b9b86f86c'


def test_search_only_returns_available_products_and_respects_limit(database):
    from telegram_ecommerce.database import models, query

    with models.Session.begin() as session:
        category = models.Category(name='Books', description='Books')
        session.add(category)
        session.flush()
        products = [
            models.Product(name='Blue Book', description='Guide to blue things', price='5.00', quantity_in_stock=1,
                           quantity_purchased=0, category_id=category.id),
            models.Product(name='Another Book', description='Blue reference', price='6.00', quantity_in_stock=1,
                           quantity_purchased=0, category_id=category.id),
            models.Product(name='Old Book', description='Blue archive', price='4.00', quantity_in_stock=0,
                           quantity_purchased=1, category_id=category.id),
        ]
        session.add_all(products)
        session.flush()
        available_id, second_id, sold_out_id = (product.id for product in products)

    assert len(query.search_products('blue', limit=1)) == 1
    assert {product.id for product in query.search_products('blue')} == {available_id, second_id}
    assert query.search_products('   ') == []
    assert query.get_available_product(available_id).id == available_id
    assert query.get_available_product(sold_out_id) is None


@pytest.mark.parametrize('price,stock,purchased', [('-1.00', 1, 0), ('1.00', -1, 0), ('1.00', 1, -1)])
def test_product_constraints_reject_invalid_values(database, price, stock, purchased):
    with database.begin() as connection:
        category_id = connection.scalar(text("INSERT INTO category (name, description) VALUES ('Books', 'Books') RETURNING id"))
    with pytest.raises(IntegrityError):
        with database.begin() as connection:
            connection.execute(text('''INSERT INTO products
                (name, description, price, quantity_in_stock, quantity_purchased, category_id)
                VALUES ('Book', 'Description', :price, :stock, :purchased, :category_id)'''),
                {'price': price, 'stock': stock, 'purchased': purchased, 'category_id': category_id})


def test_order_rating_and_status_constraints(database):
    from telegram_ecommerce.database import models

    with models.Session.begin() as session:
        customer = models.Customer(id=10_000_000_000, username='buyer', password_hash='')
        category = models.Category(name='Books', description='Books')
        session.add_all([customer, category])
        session.flush()
        product = models.Product(name='Book', description='Blue book', price='5.00', quantity_in_stock=1,
                                 quantity_purchased=0, category_id=category.id)
        session.add(product)
        session.flush()
        product_id = product.id

    with pytest.raises(IntegrityError):
        with database.begin() as connection:
            connection.execute(text('''INSERT INTO orders (id, price, user_id, product_id, rating)
                VALUES ('invalid-rating', 5, 10000000000, :product_id, 3)'''), {'product_id': product_id})
    with pytest.raises(IntegrityError):
        with database.begin() as connection:
            connection.execute(text('''INSERT INTO orders (id, price, user_id, product_id, status)
                VALUES ('invalid-status', 5, 10000000000, :product_id, 'unknown')'''), {'product_id': product_id})
