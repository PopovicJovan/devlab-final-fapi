"""empty message

Revision ID: 6b5da8946b74
Revises: 5c4c404ae123, 6e636e169627
Create Date: 2024-12-24 21:26:00.236168

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b5da8946b74'
down_revision: Union[str, None] = ('5c4c404ae123', '6e636e169627')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
