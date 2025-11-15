import httpx
from typing import List, Optional, Tuple
import json
from schemas_post import ExternalPost
from redis_client import redis_client

POSTS_API_URL = "https://jsonplaceholder.typicode.com/posts"
CACHE_KEY_ALL = "posts:all"
CACHE_TTL = 60 * 5  # 5 minutes TTL

# -----------------------------
# Fetch all posts with caching
# -----------------------------
async def fetch_all_posts() -> List[ExternalPost]:
    """Fetch all posts from external API, cached in Redis"""
    # Try to get posts from Redis
    cached = await redis_client.get(CACHE_KEY_ALL)
    if cached:
        data = json.loads(cached)
        return [ExternalPost(**item) for item in data]

    # If not cached, fetch from API
    async with httpx.AsyncClient() as client:
        response = await client.get(POSTS_API_URL)
        response.raise_for_status()
        data = response.json()

    # Store in Redis
    await redis_client.set(CACHE_KEY_ALL, json.dumps(data), ex=CACHE_TTL)
    return [ExternalPost(**item) for item in data]

# -----------------------------
# Fetch single post by ID
# -----------------------------
async def fetch_post_by_id(post_id: int) -> Optional[ExternalPost]:
    """Fetch a single post by ID, cached in Redis"""
    cache_key = f"posts:{post_id}"
    cached = await redis_client.get(cache_key)
    if cached:
        return ExternalPost(**json.loads(cached))

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{POSTS_API_URL}/{post_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        data = response.json()

    await redis_client.set(cache_key, json.dumps(data), ex=CACHE_TTL)
    return ExternalPost(**data)

# -----------------------------
# Search posts in memory
# -----------------------------
def search_posts(posts: List[ExternalPost], query: str) -> List[ExternalPost]:
    """Search posts by title or body"""
    query_lower = query.lower()
    return [
        post for post in posts
        if query_lower in post.title.lower() or query_lower in post.body.lower()
    ]

# -----------------------------
# Paginate posts
# -----------------------------
def paginate_posts(posts: List[ExternalPost], page: int, size: int) -> Tuple[List[ExternalPost], int]:
    """Paginate posts"""
    start = (page - 1) * size
    end = start + size
    return posts[start:end], len(posts)
