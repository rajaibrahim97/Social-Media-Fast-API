"""create content column in post

Revision ID: 6130b4848b58
Revises: f53b4e944f95
Create Date: 2025-02-26 09:01:53.085762

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6130b4848b58'
down_revision: Union[str, None] = 'f53b4e944f95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')