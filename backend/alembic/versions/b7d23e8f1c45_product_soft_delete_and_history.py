"""product soft delete and history

Revision ID: b7d23e8f1c45
Revises: a4f91c3e2b87
Create Date: 2026-06-01 00:00:00.000000
"""

import sqlalchemy as sa
from alembic import op

revision = "b7d23e8f1c45"
down_revision = "a4f91c3e2b87"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "products",
        sa.Column("deactivated_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "product_history",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("product_id", sa.UUID(), nullable=False),
        sa.Column("changed_by_user_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("change_type", sa.String(20), nullable=False),
        sa.Column("changed_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["changed_by_user_id"], ["users.id"]),
    )
    op.create_index("ix_product_history_product_id", "product_history", ["product_id"])


def downgrade() -> None:
    op.drop_index("ix_product_history_product_id", table_name="product_history")
    op.drop_table("product_history")
    op.drop_column("products", "deactivated_at")
