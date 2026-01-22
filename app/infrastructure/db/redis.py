import redis

from app.core.config import settings


class RedisService:
    def __init__(self):
        self.redis_url = settings.redis.REDIS_URL
        self.redis_client = redis.asyncio.from_url(
            self.redis_url, decode_responses=True
        )

    async def get(self, key):
        return await self.redis_client.get(key)

    async def set(self, key, value):
        return await self.redis_client.set(key, value)
