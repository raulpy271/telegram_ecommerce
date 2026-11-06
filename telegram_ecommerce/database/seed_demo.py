"""Add a small, clearly labeled catalog for local testing (safe to repeat)."""

from decimal import Decimal

from sqlalchemy import select

from telegram_ecommerce.database.models import Category, Product, Session


def seed_demo():
    added = 0
    with Session.begin() as session:
        category = session.scalar(select(Category).where(Category.name == "Demo stationery"))
        if category is None:
            category = Category(name="Demo stationery", description="Sample items for local testing.")
            session.add(category)
            session.flush()
        for name, description, price in (
            ("Demo Notebook", "A5 dotted notebook. Sample item for local testing.", "9.99"),
            ("Demo Pen", "Blue ink pen. Sample item for local testing.", "2.50"),
        ):
            exists = session.scalar(select(Product.id).where(
                Product.category_id == category.id, Product.name == name,
            ))
            if exists is None:
                session.add(Product(
                    name=name, description=description, price=Decimal(price),
                    category_id=category.id, quantity_in_stock=10, quantity_purchased=0,
                ))
                added += 1
    return added


if __name__ == "__main__":
    print(f"Added {seed_demo()} demo products.")
