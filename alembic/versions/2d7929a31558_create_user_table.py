"""create user table

Revision ID: 2d7929a31558
Revises: 6130b4848b58
Create Date: 2025-02-26 09:03:05.766075

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d7929a31558'
down_revision: Union[str, None] = '6130b4848b58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',sa.Column('id',sa.Integer(),primary_key=True,nullable=False),
                    sa.Column('email',sa.String(),nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
                    sa.UniqueConstraint('email'))


def downgrade() -> None:
    op.drop_table('users')