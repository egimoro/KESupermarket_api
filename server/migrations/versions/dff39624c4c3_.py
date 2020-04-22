"""empty message

Revision ID: dff39624c4c3
Revises: 
Create Date: 2020-04-19 20:27:35.409145

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dff39624c4c3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Kenyan Supermarkets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('no_of_items', sa.Integer(), nullable=True),
    sa.Column('total', sa.Float(), nullable=True),
    sa.Column('paid', sa.Float(), nullable=True),
    sa.Column('change', sa.Float(), nullable=True),
    sa.Column('type_', sa.String(), nullable=True),
    sa.Column('food', sa.Boolean(), nullable=True),
    sa.Column('drinks', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Kenyan Supermarkets')
    # ### end Alembic commands ###
