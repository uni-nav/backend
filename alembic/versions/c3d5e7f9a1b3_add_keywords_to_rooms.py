"""add keywords to rooms

Revision ID: c3d5e7f9a1b3
Revises: 2c420301e271
Create Date: 2026-02-26 00:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3d5e7f9a1b3'
down_revision: Union[str, None] = 'a43a867a194c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # nullable=True — mavjud xonalar ta'sirlanmaydi, keywords NULL bo'lib qoladi
    op.add_column('rooms', sa.Column('keywords', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('rooms', 'keywords')
