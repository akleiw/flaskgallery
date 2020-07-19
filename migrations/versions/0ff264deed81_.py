"""empty message

Revision ID: 0ff264deed81
Revises: 4f188b018871
Create Date: 2020-07-19 06:27:34.559480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ff264deed81'
down_revision = '4f188b018871'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('commenter_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'comments', 'users', ['commenter_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.drop_column('comments', 'commenter_id')
    # ### end Alembic commands ###
