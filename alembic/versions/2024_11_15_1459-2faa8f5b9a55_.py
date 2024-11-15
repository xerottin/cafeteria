"""empty message

Revision ID: 2faa8f5b9a55
Revises: 0c1e8f06fd78
Create Date: 2024-11-15 14:59:01.959921

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2faa8f5b9a55'
down_revision: Union[str, None] = '0c1e8f06fd78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('cafeteria_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'order', 'cafeteria', ['cafeteria_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.drop_column('order', 'cafeteria_id')
    # ### end Alembic commands ###
