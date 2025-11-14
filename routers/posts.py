from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from dependencies import get_current_user
from models import User, Post
from schemas_post import (
    PostCreate, 
    PostOut, 
    ExternalPost, 
    ExternalPostList
)
from services_post import (
    fetch_all_posts,
    fetch_post_by_id,
    search_posts,
    paginate_posts
)

router = APIRouter(prefix="/api/v1/posts", tags=["Posts"])

# ============ USER'S OWN POSTS ============

@router.post("", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new post (requires authentication)
    """
    new_post = Post(
        title=post_data.title,
        body=post_data.body,
        user_id=current_user.id
    )
    
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    
    return new_post

@router.get("/my-posts", response_model=List[PostOut])
async def get_my_posts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all posts created by current user
    """
    result = await db.execute(
        select(Post)
        .where(Post.user_id == current_user.id)
        .order_by(Post.created_at.desc())
    )
    posts = result.scalars().all()
    return posts

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete your own post
    """
    result = await db.execute(
        select(Post).where(Post.id == post_id, Post.user_id == current_user.id)
    )
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found or you don't have permission to delete it"
        )
    
    await db.delete(post)
    await db.commit()
    return

# ============ EXTERNAL POSTS (READ-ONLY) ============

@router.get("/external", response_model=ExternalPostList)
async def get_external_posts(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term")
):
    """
    Get posts from external API (JSONPlaceholder)
    """
    all_posts = await fetch_all_posts()
    
    if search:
        all_posts = search_posts(all_posts, search)
    
    paginated_posts, total = paginate_posts(all_posts, page, size)
    
    return ExternalPostList(
        total=total,
        page=page,
        size=size,
        posts=paginated_posts
    )

@router.get("/external/{post_id}", response_model=ExternalPost)
async def get_external_post(post_id: int):
    """
    Get a single post from external API
    """
    post = await fetch_post_by_id(post_id)
    
    if not post:
        raise HTTPException(
            status_code=404,
            detail=f"Post with id {post_id} not found"
        )
    
    return post