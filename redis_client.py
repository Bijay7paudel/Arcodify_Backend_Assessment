import redis.asyncio as redis

# Redis connection
redis_client = redis.Redis(
    host="localhost",  # Redis host
    port=6379,         # Redis port
    db=0,
    decode_responses=True
)
