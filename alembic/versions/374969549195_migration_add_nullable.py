"""migration add nullable

Revision ID: 374969549195
Revises: c7f3927fca74
Create Date: 2024-12-17 22:59:36.283299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '374969549195'
down_revision: Union[str, None] = 'c7f3927fca74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('call', 'status_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('call', 'dispatcher_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('call', 'brigade_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('cars', 'brigade_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cars', 'brigade_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('call', 'brigade_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('call', 'dispatcher_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('call', 'status_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###