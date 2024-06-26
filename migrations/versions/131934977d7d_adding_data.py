"""Adding data

Revision ID: 131934977d7d
Revises: 72bacd508cc1
Create Date: 2024-04-24 09:00:07.725946

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '131934977d7d'
down_revision: Union[str, None] = '72bacd508cc1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        "INSERT INTO storage VALUES ('St-1', 125, 0, 1)"
    )
    op.execute(
        "INSERT INTO storage VALUES ('St-2', 2500, 0, 2)"
    )
    op.execute(
        "INSERT INTO products VALUES ('COFFEE', 25, 1)"
    )
    op.execute(
        "UPDATE storage SET curr_weight = 25 WHERE id=1"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        "DELETE FROM storage WHERE id=1"
    )
    op.execute(
        "DELETE FROM storage WHERE id=2"
    )
    op.execute(
        "DELETE FROM products WHERE id=1"
    )
    # ### end Alembic commands ###
