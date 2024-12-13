"""models table added

Revision ID: 4e9aa11c5176
Revises: f4a838359e21
Create Date: 2024-12-13 16:03:47.905691

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e9aa11c5176'
down_revision: Union[str, None] = 'f4a838359e21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('models',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('manufacturer', sa.String(length=32), nullable=False),
    sa.Column('length', sa.Float(), nullable=False),
    sa.Column('width', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('manufacturer'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('models')
    # ### end Alembic commands ###
