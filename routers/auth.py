from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from schemas import UserCreate, UserOut, Token
from crud import create_user, get_user_by_email, authenticate_user
from security import create_access_token, create_refresh_token, SECRET_KEY, ALGORITHM
from models import User
import jwt

# 🚀 ADD THIS IMPORT FOR CELERY TASK
from celery_worker import send_welcome_email

router = APIRouter(prefix="/auth", tags=["authentication"])

# --------------------------
# User Registration Endpoint (WITH CELERY TASK)
# --------------------------
@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user and send welcome email in background"""
    # Check if user already exists
    existing_user = await get_user_by_email(db, payload.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user (normal user, is_admin=False)
    user = await create_user(db, payload.email, payload.password, payload.full_name)
    
    # 🚀 SEND WELCOME EMAIL IN BACKGROUND (NON-BLOCKING)
    send_welcome_email.delay(user.email, user.full_name or "User")
    print(f"✨ User {user.email} registered! Welcome email task queued.")
    
    return user

# --------------------------
# User Login Endpoint
# --------------------------
@router.post("/login", response_model=Token)
async def login(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Login and get access token"""
    user = await authenticate_user(db, payload.email, payload.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# --------------------------
# Admin Dependency
# --------------------------
security = HTTPBearer()

async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    Dependency for admin-only routes.
    Verifies JWT and ensures user is an admin.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    # Get user from DB
    q = await db.execute(select(User).where(User.id == user_id))
    user = q.scalars().first()
    
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    
    return user
