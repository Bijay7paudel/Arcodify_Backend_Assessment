from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import init_db
from routers import auth, profile, posts  # ← Added posts here

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting up...")
    await init_db()
    print("✅ Database initialized!")
    yield
    print("👋 Shutting down...")

app = FastAPI(
    title="FastAPI JWT Project",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(posts.router)  # ← Added this line

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI JWT Project!"}