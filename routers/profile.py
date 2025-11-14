from fastapi import APIRouter, Depends
from schemas import UserOut
from dependencies import get_current_user
from models import User

router = APIRouter(prefix="/api/v1/profile", tags=["Profile"])

@router.get("/me", response_model=UserOut)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """
    Get current user's profile
    You must be logged in to use this endpoint
    """
    return current_user