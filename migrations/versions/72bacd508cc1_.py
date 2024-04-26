"""empty message

Revision ID: 72bacd508cc1
Revises: 
Create Date: 2024-04-24 08:51:53.364440

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72bacd508cc1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('storage',
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('max_weight', sa.Integer(), nullable=False),
    sa.Column('curr_weight', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('weight', sa.Integer(), nullable=False),
    sa.Column('storage', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['storage'], ['storage.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    op.drop_table('users')
    op.drop_table('storage')
    # ### end Alembic commands ###