"""order status: draft/pending/paid

Revision ID: a4f91c3e2b87
Revises: 031c791500ce
Create Date: 2026-06-01 00:00:00.000000

Renames the orderstatus enum:
  pending   → draft   (order being assembled)
  confirmed → pending (confirmed, awaiting payment)
Adds:
  paid      (payment received)
"""

from alembic import op

revision = "a4f91c3e2b87"
down_revision = "031c791500ce"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Convert column to plain text so we can drop the old enum type
    op.execute("ALTER TABLE orders ALTER COLUMN status TYPE varchar USING status::text")

    # 2. Migrate existing data to the new value names
    op.execute("UPDATE orders SET status = 'draft'   WHERE status = 'pending'")
    op.execute("UPDATE orders SET status = 'pending' WHERE status = 'confirmed'")

    # 3. Drop old enum and create the new one
    op.execute("DROP TYPE orderstatus")
    op.execute("CREATE TYPE orderstatus AS ENUM ('draft', 'pending', 'paid', 'cancelled')")

    # 4. Convert column back to the new enum type
    op.execute(
        "ALTER TABLE orders ALTER COLUMN status TYPE orderstatus "
        "USING status::orderstatus"
    )


def downgrade() -> None:
    op.execute("ALTER TABLE orders ALTER COLUMN status TYPE varchar USING status::text")
    op.execute("UPDATE orders SET status = 'confirmed' WHERE status = 'pending'")
    op.execute("UPDATE orders SET status = 'pending'   WHERE status = 'draft'")
    op.execute("DROP TYPE orderstatus")
    op.execute("CREATE TYPE orderstatus AS ENUM ('pending', 'confirmed', 'cancelled')")
    op.execute(
        "ALTER TABLE orders ALTER COLUMN status TYPE orderstatus "
        "USING status::orderstatus"
    )
