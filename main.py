# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine, Base
from routers import auth, profile, posts, admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting up...")

    # Import models to register them with Base
    import models

    # Create all tables in PostgreSQL
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Database tables created!")
    yield
    print("👋 Shutting down...")

app = FastAPI(
    title="FastAPI JWT Project",
    version="1.0.0",
    lifespan=lifespan
)

# Include your routers
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(posts.router)
app.include_router(admin.router)


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI JWT Project!"}
