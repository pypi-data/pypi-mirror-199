from aioredis.client import Redis

DEFAULT_RATE_KEY = 'RATE'


class AioRedisRateLimiter:

    def __init__(self, redis: Redis, rate_limit: int, rate_key_ttl: int = 30, rate_key: str = DEFAULT_RATE_KEY):
        self.redis = redis
        self._rate_key = rate_key
        self._rate_limit = rate_limit
        self._rate_key_ttl = rate_key_ttl

    async def __inc(self) -> int:
        """Increase rate limit"""
        async with self.redis.client() as conn:
            result = await conn.incr(self._rate_key, 1)
            if result == 1:
                await conn.expire(self._rate_key, self._rate_key_ttl)
            return result

    async def rate(self) -> int:
        """Get current rate limit"""
        async with self.redis.client() as conn:
            result = await conn.get(self._rate_key)
            return result or 0

    async def is_limited(self) -> bool:
        """Check rate state"""
        async with self.redis.client() as conn:
            value = await conn.get(self._rate_key)
            if value is None:
                return False
            return int(value) > self._rate_limit

    async def acquire(self) -> bool:
        """Acquire resource"""
        value = await self.__inc()
        return value <= self._rate_limit
