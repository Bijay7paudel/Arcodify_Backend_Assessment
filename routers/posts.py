from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from dependencies import get_current_user
from models import User, Post
from schemas_post import PostCreate, PostOut, ExternalPost, ExternalPostList
from services_post import (
    fetch_db_post_by_id,
    fetch_all_external_posts,
    fetch_external_post_by_id,
    search_posts,
    paginate_posts
)

router = APIRouter(prefix="/api/v1/posts", tags=["Posts"])

# ----------------- CREATE POST -----------------
@router.post("", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_post = Post(
        title=post_data.title,
        body=post_data.body,
        user_id=current_user.id
    )
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post


# ----------------- GET MY POSTS -----------------
@router.get("/my-posts", response_model=List[PostOut])
async def get_my_posts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Post).where(Post.user_id == current_user.id).order_by(Post.created_at.desc())
    )
    return result.scalars().all()


# ----------------- EXTERNAL POSTS (List) -----------------
# ----------------- EXTERNAL POSTS (List) -----------------
@router.get("/external", response_model=ExternalPostList)
async def get_external_posts(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)  # Add database dependency
):
    all_posts = await fetch_all_external_posts(db)  # Fetch from YOUR DB
    if search:
        all_posts = search_posts(all_posts, search)
    paginated_posts, total = paginate_posts(all_posts, page, size)
    return ExternalPostList(total=total, page=page, size=size, posts=paginated_posts)



# ----------------- DB POST BY ID (Dynamic route last!) -----------------
@router.get("/{post_id}", response_model=PostOut)
async def get_db_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await fetch_db_post_by_id(post_id, db)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found in DB")
    return post
