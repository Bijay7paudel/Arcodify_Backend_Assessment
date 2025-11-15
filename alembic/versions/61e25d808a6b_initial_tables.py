"""Initial tables

Revision ID: 61e25d808a6b
Revises: de68be802015
Create Date: 2025-11-14 18:12:37.714078

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61e25d808a6b'
down_revision: Union[str, Sequence[str], None] = 'de68be802015'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
