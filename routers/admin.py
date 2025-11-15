from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func
from database import get_db
from models import User
from routers.auth import get_current_admin  # JWT admin dependency

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

# --------------------------
# GET /users - List users with pagination, search, and active filter
# --------------------------
@router.get("/users")
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Number of users per page"),
    search: str = Query(None, description="Search by email substring"),
    active: bool = Query(None, description="Filter active/inactive users"),
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """
    List users (admin-only).
    Supports pagination, search by email, and active/inactive filtering.
    """
    query = select(User)
    
    if search:
        query = query.where(User.email.ilike(f"%{search}%"))
    
    if active is not None:
        query = query.where(User.is_active == active)

    # Apply pagination
    query = query.offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()

    # Efficient total count
    count_query = select(func.count()).select_from(User)
    if search:
        count_query = count_query.where(User.email.ilike(f"%{search}%"))
    if active is not None:
        count_query = count_query.where(User.is_active == active)
    count_result = await db.execute(count_query)
    total_users = count_result.scalar()  # single integer

    return {
        "total": total_users,
        "page": page,
        "limit": limit,
        "users": users
    }

# --------------------------
# POST /users/{user_id}/deactivate - Deactivate user
# --------------------------
@router.post("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """
    Deactivate a user by ID.
    Only accessible by admin users.
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        return {"detail": "User already deactivated"}

    stmt = update(User).where(User.id == user_id).values(is_active=False)
    await db.execute(stmt)
    await db.commit()

    return {"detail": f"User {user.email} has been deactivated"}
