# create_tables.py
import asyncio
from database import init_db

asyncio.run(init_db())
