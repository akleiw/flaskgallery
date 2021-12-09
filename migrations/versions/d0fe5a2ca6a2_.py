"""empty message

Revision ID: d0fe5a2ca6a2
Revises: 3af2cdf261e9
Create Date: 2021-12-09 20:20:40.244136

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0fe5a2ca6a2'
down_revision = '3af2cdf261e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'albums_roles', ['album_id', 'role_id'])
    op.create_unique_constraint(None, 'users_roles', ['user_id', 'role_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users_roles', type_='unique')
    op.drop_constraint(None, 'albums_roles', type_='unique')
    # ### end Alembic commands ###
