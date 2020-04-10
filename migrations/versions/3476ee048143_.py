"""empty message

Revision ID: 3476ee048143
Revises: 
Create Date: 2020-04-01 01:09:38.730026

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3476ee048143'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userName', sa.String(length=64), nullable=False),
    sa.Column('firstName', sa.String(length=128), nullable=True),
    sa.Column('lastName', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=128), nullable=True),
    sa.Column('CreditCard', sa.Integer(), nullable=True),
    sa.Column('CCV', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('CCV'),
    sa.UniqueConstraint('CreditCard'),
    sa.UniqueConstraint('userName')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
