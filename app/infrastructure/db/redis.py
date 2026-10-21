class RedisService:
    """Optional helper; install redis separately if a project needs caching."""

    def __init__(self, redis_url: str):
        from redis.asyncio import Redis

        self.redis_client = Redis.from_url(redis_url, decode_responses=True)

    async def get(self, key: str) -> str | None:
        return await self.redis_client.get(key)

    async def set(self, key: str, value: str, *, expires: int | None = None):
        return await self.redis_client.set(key, value, ex=expires)

    async def close(self) -> None:
        await self.redis_client.aclose()
