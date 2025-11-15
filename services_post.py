from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Post
from schemas_post import ExternalPost
from typing import Optional, List, Tuple
import httpx

POSTS_API_URL = "https://jsonplaceholder.typicode.com/posts"

# ----------------- DB POST -----------------
async def fetch_db_post_by_id(post_id: int, db: AsyncSession) -> Optional[Post]:
    """Fetch a single post from your database by ID"""
    result = await db.execute(select(Post).where(Post.id == post_id))
    return result.scalar_one_or_none()


async def fetch_all_external_posts(db: AsyncSession) -> List[ExternalPost]:
    """Fetch all posts from your database"""
    result = await db.execute(select(Post))
    posts = result.scalars().all()
    
    # Convert your Post model to ExternalPost format
    return [
        ExternalPost(
            userId=post.user_id,
            id=post.id,
            title=post.title,
            body=post.body
        ) 
        for post in posts
    ]


async def fetch_external_post_by_id(post_id: int) -> Optional[ExternalPost]:
    """Fetch a single external post by ID"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{POSTS_API_URL}/{post_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        data = response.json()
    return ExternalPost(**data)


# ----------------- SEARCH -----------------
def search_posts(posts: List[ExternalPost], query: str) -> List[ExternalPost]:
    """Search posts by title or body (case-insensitive)"""
    query_lower = query.lower()
    filtered = []
    for post in posts:
        title = getattr(post, "title", "") or ""
        body = getattr(post, "body", "") or ""
        if query_lower in title.lower() or query_lower in body.lower():
            filtered.append(post)
    return filtered


# ----------------- PAGINATION -----------------
def paginate_posts(posts: List[ExternalPost], page: int, size: int) -> Tuple[List[ExternalPost], int]:
    """Paginate the posts list safely"""
    total = len(posts)
    start = (page - 1) * size
    end = start + size
    paginated = posts[start:end] if start < total else []
    return paginated, total
