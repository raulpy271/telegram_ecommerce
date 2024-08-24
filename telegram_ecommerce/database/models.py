
from os import environ

from sqlalchemy import Column, Float, ForeignKey, Index, Integer, LargeBinary, String, Boolean, text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase



class Base(DeclarativeBase):
    pass

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)
    password_hash = Column(String(64))
    is_admin = Column(Boolean, nullable=False, server_default=text("'0'"))


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
        Index('name', 'name', 'description'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    description = Column(String(500), nullable=False)
    price = Column(Float, nullable=False)
    quantity_in_stock = Column(Integer, nullable=False)
    quantity_purchased = Column(Integer, nullable=False)
    category_id = Column(ForeignKey('category.id'), nullable=False, index=True)
    image_id = Column(ForeignKey('photo.id'), index=True)

    category = relationship('Category')
    image = relationship('Photo')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(String(150), primary_key=True)
    price = Column(Float, nullable=False)
    user_id = Column(ForeignKey('customers.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)
    product_id = Column(ForeignKey('products.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False, index=True)
    rating = Column(Integer)

    product = relationship('Product')
    user = relationship('Customer')

db_url = f"mysql+pymysql://{environ['DB_USER']}:{environ['DB_PASSWORD']}@{environ['DB_HOST']}/{environ['DB_NAME']}"
engine = create_engine(db_url)
Session = sessionmaker(engine)

