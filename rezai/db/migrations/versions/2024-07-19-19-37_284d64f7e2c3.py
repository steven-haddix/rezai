"""Updated res relationships

Revision ID: 284d64f7e2c3
Revises: 1e5b1443ab6e
Create Date: 2024-07-19 19:37:22.191994

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "284d64f7e2c3"
down_revision = "1e5b1443ab6e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "restaurants",
        "website",
        existing_type=sa.VARCHAR(length=255),
        nullable=True,
    )
    op.alter_column(
        "restaurants",
        "description",
        existing_type=sa.VARCHAR(length=1000),
        nullable=True,
    )
    op.alter_column(
        "restaurants",
        "address",
        existing_type=sa.VARCHAR(length=255),
        nullable=True,
    )
    op.alter_column(
        "restaurants",
        "phone",
        existing_type=sa.VARCHAR(length=20),
        nullable=True,
    )
    op.alter_column("restaurants", "rating", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column("restaurants", "reviews", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column(
        "restaurants",
        "unclaimed",
        existing_type=sa.BOOLEAN(),
        nullable=True,
    )
    op.alter_column(
        "restaurants",
        "hours",
        existing_type=sa.VARCHAR(length=1000),
        nullable=True,
    )
    op.alter_column(
        "restaurants",
        "opening_hours",
        existing_type=sa.VARCHAR(length=1000),
        nullable=True,
    )
    op.alter_column(
        "restaurants",
        "people_also_search_for",
        existing_type=sa.VARCHAR(length=1000),
        nullable=True,
    )
    op.alter_column(
        "restaurants",
        "menu",
        existing_type=sa.VARCHAR(length=1000),
        nullable=True,
    )
    op.alter_column(
        "restaurants",
        "reservations",
        existing_type=sa.VARCHAR(length=1000),
        nullable=True,
    )
    op.alter_column(
        "restaurants",
        "order_food",
        existing_type=sa.VARCHAR(length=1000),
        nullable=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "restaurants",
        "order_food",
        existing_type=sa.VARCHAR(length=1000),
        nullable=False,
    )
    op.alter_column(
        "restaurants",
        "reservations",
        existing_type=sa.VARCHAR(length=1000),
        nullable=False,
    )
    op.alter_column(
        "restaurants",
        "menu",
        existing_type=sa.VARCHAR(length=1000),
        nullable=False,
    )
    op.alter_column(
        "restaurants",
        "people_also_search_for",
        existing_type=sa.VARCHAR(length=1000),
        nullable=False,
    )
    op.alter_column(
        "restaurants",
        "opening_hours",
        existing_type=sa.VARCHAR(length=1000),
        nullable=False,
    )
    op.alter_column(
        "restaurants",
        "hours",
        existing_type=sa.VARCHAR(length=1000),
        nullable=False,
    )
    op.alter_column(
        "restaurants",
        "unclaimed",
        existing_type=sa.BOOLEAN(),
        nullable=False,
    )
    op.alter_column(
        "restaurants",
        "reviews",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.alter_column("restaurants", "rating", existing_type=sa.INTEGER(), nullable=False)
    op.alter_column(
        "restaurants",
        "phone",
        existing_type=sa.VARCHAR(length=20),
        nullable=False,
    )
    op.alter_column(
        "restaurants",
        "address",
        existing_type=sa.VARCHAR(length=255),
        nullable=False,
    )
    op.alter_column(
        "restaurants",
        "description",
        existing_type=sa.VARCHAR(length=1000),
        nullable=False,
    )
    op.alter_column(
        "restaurants",
        "website",
        existing_type=sa.VARCHAR(length=255),
        nullable=False,
    )
    # ### end Alembic commands ###