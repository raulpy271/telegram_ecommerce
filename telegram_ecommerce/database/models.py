
from os import environ

from sqlalchemy import BigInteger, CheckConstraint, Column, DateTime, ForeignKey, Index, Integer, LargeBinary, Numeric, String, Boolean, func, text
from sqlalchemy import create_engine
from sqlalchemy.engine import URL, make_url
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase



class Base(DeclarativeBase):
    pass

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(BigInteger, primary_key=True)
    username = Column(String(30), nullable=False)
    password_hash = Column(String(64))
    is_admin = Column(Boolean, nullable=False, server_default=text("false"))


class Photo(Base):
    __tablename__ = 'photo'

    id = Column(String(150), primary_key=True)
    image_blob = Column(LargeBinary)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    description = Column(String(500), nullable=False)
    tags = Column(String(100))
    image_id = Column(ForeignKey('photo.id'), index=True)

    image = relationship('Photo')


class Product(Base):
    __tablename__ = 'products'
    __table_args__ = (
        CheckConstraint('price >= 0', name='ck_products_price_nonnegative'),
        CheckConstraint('quantity_in_stock >= 0', name='ck_products_stock_nonnegative'),
        CheckConstraint('quantity_purchased >= 0', name='ck_products_purchased_nonnegative'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    description = Column(String(500), nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
    quantity_in_stock = Column(Integer, nullable=False)
    quantity_purchased = Column(Integer, nullable=False)
    category_id = Column(ForeignKey('category.id'), nullable=False, index=True)
    image_id = Column(ForeignKey('photo.id'), index=True)

    category = relationship('Category')
    image = relationship('Photo')

Index(
    'ix_products_search',
    func.to_tsvector('simple', Product.name + ' ' + Product.description),
    postgresql_using='gin',
)


class Order(Base):
    __tablename__ = 'orders'
    __table_args__ = (
        CheckConstraint('price >= 0', name='ck_orders_price_nonnegative'),
        CheckConstraint('rating IN (0, 5, 10)', name='ck_orders_rating_values'),
        CheckConstraint("status IN ('paid', 'needs_review')", name='ck_orders_status_values'),
    )

    id = Column(String(150), primary_key=True)
    price = Column(Numeric(12, 2), nullable=False)
    user_id = Column(ForeignKey('customers.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)
    product_id = Column(ForeignKey('products.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)
    rating = Column(Integer)
    status = Column(String(20), nullable=False, server_default=text("'paid'"))
    paid_at = Column(DateTime(timezone=True))

    product = relationship('Product')
    user = relationship('Customer')

db_url = (
    make_url(environ['DATABASE_URL'])
    if environ.get('DATABASE_URL')
    else URL.create(
        'postgresql+psycopg',
        username=environ['DB_USER'],
        password=environ['DB_PASSWORD'],
        host=environ['DB_HOST'],
        port=int(environ.get('DB_PORT', '5432')),
        database=environ['DB_NAME'],
    )
)
if db_url.get_backend_name() != 'postgresql':
    raise ValueError('DATABASE_URL must use PostgreSQL')
engine = create_engine(db_url, pool_pre_ping=True)
Session = sessionmaker(engine)

