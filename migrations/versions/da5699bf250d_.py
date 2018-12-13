"""empty message

Revision ID: da5699bf250d
Revises: 
Create Date: 2018-12-14 00:46:00.738097

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da5699bf250d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mv',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mvname', sa.String(length=32), nullable=False),
    sa.Column('mvurl', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mvname'),
    sa.UniqueConstraint('mvurl')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mv')
    # ### end Alembic commands ###
