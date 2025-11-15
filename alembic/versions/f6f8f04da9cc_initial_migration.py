"""Initial migration

Revision ID: f6f8f04da9cc
Revises: b70639258c08
Create Date: 2025-11-14 18:24:42.160738

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6f8f04da9cc'
down_revision: Union[str, Sequence[str], None] = 'b70639258c08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
