from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Add these imports
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from models import Base  # Import your Base
target_metadata = Base.metadata  # Add this line

# ... rest of the file