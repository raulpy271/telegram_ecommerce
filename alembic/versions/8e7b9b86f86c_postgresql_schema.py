"""Use PostgreSQL types, constraints, and full-text search.

Revision ID: 8e7b9b86f86c
Revises: d4e4c097ad8d
"""

from alembic import op
import sqlalchemy as sa

revision = '8e7b9b86f86c'
down_revision = 'd4e4c097ad8d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_index('products_fulltext_idx', table_name='products')
    op.drop_index('name', table_name='products')

    op.alter_column('customers', 'id', type_=sa.BigInteger())
    op.alter_column('orders', 'user_id', type_=sa.BigInteger())
    op.alter_column('customers', 'is_admin', server_default=sa.text('false'))
    op.alter_column('products', 'price', type_=sa.Numeric(12, 2))
    op.alter_column('orders', 'price', type_=sa.Numeric(12, 2))
    op.add_column('orders', sa.Column('status', sa.String(20), nullable=False, server_default='paid'))
    op.add_column('orders', sa.Column('paid_at', sa.DateTime(timezone=True), nullable=True))

    op.create_check_constraint('ck_products_price_nonnegative', 'products', 'price >= 0')
    op.create_check_constraint('ck_products_stock_nonnegative', 'products', 'quantity_in_stock >= 0')
    op.create_check_constraint('ck_products_purchased_nonnegative', 'products', 'quantity_purchased >= 0')
    op.create_check_constraint('ck_orders_price_nonnegative', 'orders', 'price >= 0')
    op.create_check_constraint('ck_orders_rating_values', 'orders', 'rating IN (0, 5, 10)')
    op.create_check_constraint('ck_orders_status_values', 'orders', "status IN ('paid', 'needs_review')")

    op.execute(
        "CREATE INDEX ix_products_search ON products USING gin "
        "(to_tsvector('simple', name || ' ' || description))"
    )


def downgrade() -> None:
    op.drop_index('ix_products_search', table_name='products')
    op.drop_constraint('ck_orders_status_values', 'orders', type_='check')
    op.drop_constraint('ck_orders_rating_values', 'orders', type_='check')
    op.drop_constraint('ck_orders_price_nonnegative', 'orders', type_='check')
    op.drop_constraint('ck_products_purchased_nonnegative', 'products', type_='check')
    op.drop_constraint('ck_products_stock_nonnegative', 'products', type_='check')
    op.drop_constraint('ck_products_price_nonnegative', 'products', type_='check')
    op.drop_column('orders', 'paid_at')
    op.drop_column('orders', 'status')
    op.alter_column('orders', 'price', type_=sa.Float())
    op.alter_column('products', 'price', type_=sa.Float())
    op.alter_column('customers', 'is_admin', server_default=sa.text("'0'"))
    op.alter_column('orders', 'user_id', type_=sa.Integer())
    op.alter_column('customers', 'id', type_=sa.Integer())
    op.create_index('name', 'products', ['name', 'description'])
    op.create_index('products_fulltext_idx', 'products', ['name', 'description'])
