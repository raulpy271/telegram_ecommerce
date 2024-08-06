"""Add fulltext index

Revision ID: d4e4c097ad8d
Revises: 1c9945279bf2
Create Date: 2024-08-05 22:33:31.417469

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4e4c097ad8d'
down_revision: Union[str, None] = '1c9945279bf2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
NAME_IDX = 'products_fulltext_idx'

def upgrade() -> None:
    op.create_index(NAME_IDX, 'products', ['name', 'description'], mysql_prefix='FULLTEXT')

def downgrade() -> None:
    op.drop_index(NAME_IDX, 'products')

