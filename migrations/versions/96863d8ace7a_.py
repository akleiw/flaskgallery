"""empty message

Revision ID: 96863d8ace7a
Revises: 164aba144214
Create Date: 2021-10-23 19:35:01.489465

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "96863d8ace7a"
down_revision = "164aba144214"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("albums", sa.Column("items_count", sa.Integer(), nullable=True))
    op.add_column("albums", sa.Column("title", sa.String(length=255), nullable=True))
    op.add_column("albums", sa.Column("url_title", sa.String(length=255), nullable=True))
    op.create_index(op.f("ix_albums_title"), "albums", ["title"], unique=False)
    op.create_index(op.f("ix_albums_url_title"), "albums", ["url_title"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_albums_url_title"), table_name="albums")
    op.drop_index(op.f("ix_albums_title"), table_name="albums")
    op.drop_column("albums", "url_title")
    op.drop_column("albums", "title")
    op.drop_column("albums", "items_count")
    # ### end Alembic commands ###
