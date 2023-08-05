# aioredis-rate-limiter
***

Rate limiter implements on Redis

Implementation of distributed rate limiter with aioredis, an asyncio based redis client.

Simple rate limiter based on Redis DB. 

The key features are:

* Concurrency work
* Rate by limit requests
* Rate by time for requests

# Usage

We want to limit requests from 5 pods to limited resource. Limits for resource: no more 10 request per 20 seconds.

```python
locker = AioRedisRateLimiter(redis, rate_limit=10, rate_key_ttl=20)
```

```python

import asyncio
import os
from aioredis.client import Redis
from aioredis_rate_limiter import AioRedisRateLimiter

class Executor:
    def __init__(self, name: str, locker: AioRedisRateLimiter, task_count: int = 10):
        self._locker = locker
        self._task_count = task_count
        self._name = name

    async def process(self):
        for i in range(self._task_count):
            while True:
                is_ok = await self._locker.acquire()
                if is_ok:
                    print(f'Executor {self._name} by {i+1}')
                    break
                else:
                    await asyncio.sleep(1)


async def main():
    host = os.getenv('REDIS_HOST')
    db = os.getenv('REDIS_DB')
    
    redis = Redis.from_url(host, db=db, encoding="utf-8", decode_responses=True)

    locker = AioRedisRateLimiter(redis, rate_limit=10, rate_key_ttl=15)

    w1 = Executor('first', locker, 10)
    w2 = Executor('helper', locker, 8)
    w3 = Executor('lazzy', locker, 5)

    tasks = [w1.process(), w2.process(), w3.process()]

    await asyncio.gather(*tasks)

    
if __name__ == '__main__':
    asyncio.run(main())

```