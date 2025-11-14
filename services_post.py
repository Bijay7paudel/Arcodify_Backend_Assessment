import httpx
from typing import List, Optional
from schemas_post import ExternalPost  # ← Changed from Post

POSTS_API_URL = "https://jsonplaceholder.typicode.com/posts"

async def fetch_all_posts() -> List[ExternalPost]:  # ← Changed
    """Fetch all posts from external API"""
    async with httpx.AsyncClient() as client:
        response = await client.get(POSTS_API_URL)
        response.raise_for_status()
        data = response.json()
        return [ExternalPost(**item) for item in data]  # ← Changed

async def fetch_post_by_id(post_id: int) -> Optional[ExternalPost]:  # ← Changed
    """Fetch a single post by ID"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{POSTS_API_URL}/{post_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return ExternalPost(**response.json())  # ← Changed

def search_posts(posts: List[ExternalPost], query: str) -> List[ExternalPost]:  # ← Changed
    """Search posts by title or body"""
    query_lower = query.lower()
    return [
        post for post in posts
        if query_lower in post.title.lower() or query_lower in post.body.lower()
    ]

def paginate_posts(posts: List[ExternalPost], page: int, size: int) -> tuple[List[ExternalPost], int]:  # ← Changed
    """Paginate posts"""
    start = (page - 1) * size
    end = start + size
    return posts[start:end], len(posts)