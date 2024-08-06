"""update_users_table

Revision ID: 7c8a59f2b168
Revises: 1f674abbd619
Create Date: 2024-08-06 15:26:09.210474

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '7c8a59f2b168'
down_revision: Union[str, None] = '1f674abbd619'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'email',
               existing_type=mysql.VARCHAR(length=20),
               type_=sa.String(length=100),
               existing_nullable=False)
    op.alter_column('users', 'password',
               existing_type=mysql.VARCHAR(length=20),
               type_=sa.String(length=100),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=20),
               existing_nullable=False)
    op.alter_column('users', 'email',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=20),
               existing_nullable=False)
    # ### end Alembic commands ###
