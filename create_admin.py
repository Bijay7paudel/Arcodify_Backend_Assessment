import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import User
from security import get_password_hash
from sqlalchemy import select

async def create_admin():
    # get async session from generator
    async for db in get_db():  # use async for, not async with
        # Check if admin already exists
        result = await db.execute(select(User).where(User.email=="admin@example.com"))
        existing = result.scalars().first()
        if existing:
            print("Admin already exists!")
            return

        # Create new admin user
        admin = User(
            email="admin@example.com",
            full_name="Admin User",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            is_admin=True
        )
        db.add(admin)
        await db.commit()
        print("Admin user created successfully!")

# Run the async function
asyncio.run(create_admin())
