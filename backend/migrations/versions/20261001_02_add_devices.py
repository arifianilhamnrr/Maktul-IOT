"""Add devices and link LED statuses.

Revision ID: 20261001_02
Revises: 20261001_01
Create Date: 2026-10-01
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20261001_02"
down_revision: str | None = "20261001_01"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "devices",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.execute("DELETE FROM led_statuses")
    op.add_column(
        "led_statuses",
        sa.Column("id_device", sa.Integer(), nullable=False),
    )
    op.alter_column(
        "led_statuses",
        "status",
        new_column_name="status_led",
        existing_type=sa.Boolean(),
        existing_nullable=False,
    )
    op.create_index(
        op.f("ix_led_statuses_id_device"),
        "led_statuses",
        ["id_device"],
        unique=False,
    )
    op.create_foreign_key(
        "fk_led_statuses_id_device_devices",
        "led_statuses",
        "devices",
        ["id_device"],
        ["id"],
        ondelete="RESTRICT",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_led_statuses_id_device_devices",
        "led_statuses",
        type_="foreignkey",
    )
    op.drop_index(op.f("ix_led_statuses_id_device"), table_name="led_statuses")
    op.alter_column(
        "led_statuses",
        "status_led",
        new_column_name="status",
        existing_type=sa.Boolean(),
        existing_nullable=False,
    )
    op.drop_column("led_statuses", "id_device")
    op.drop_table("devices")
