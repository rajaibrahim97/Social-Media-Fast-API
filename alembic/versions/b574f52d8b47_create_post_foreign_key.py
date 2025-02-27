"""create post foreign key

Revision ID: b574f52d8b47
Revises: 2d7929a31558
Create Date: 2025-02-26 09:04:17.397713

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b574f52d8b47'
down_revision: Union[str, None] = '2d7929a31558'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_user_fk',source_table="posts",referent_table="users",local_cols=["owner_id"],remote_cols=["id"],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk',table_name="posts")
    op.drop_column("posts","owner_id")
    pass
