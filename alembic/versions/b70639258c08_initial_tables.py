"""Initial tables

Revision ID: b70639258c08
Revises: 61e25d808a6b
Create Date: 2025-11-14 18:14:05.085471

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b70639258c08'
down_revision: Union[str, Sequence[str], None] = '61e25d808a6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
