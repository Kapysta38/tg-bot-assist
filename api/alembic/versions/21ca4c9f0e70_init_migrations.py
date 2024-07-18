"""Init migrations

Revision ID: 21ca4c9f0e70
Revises: 
Create Date: 2024-07-18 13:15:34.478500

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21ca4c9f0e70'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('processes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('pid', sa.Integer(), nullable=True),
    sa.Column('command', sa.String(length=255), nullable=False),
    sa.Column('log_filename', sa.String(length=255), nullable=False),
    sa.Column('status', sa.Enum('stopped', 'running', name='statusprocess'), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_roles',
    sa.Column('role_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('role_name', sa.Enum('admin', 'chat', name='roles'), nullable=False),
    sa.PrimaryKeyConstraint('role_id')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('full_name', sa.String(length=255), nullable=True),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('city', sa.String(length=255), nullable=True),
    sa.Column('tg_id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('user_role_associations',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['user_roles.role_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_role_associations')
    op.drop_table('users')
    op.drop_table('user_roles')
    op.drop_table('processes')
    # ### end Alembic commands ###
