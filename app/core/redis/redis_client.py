# app/core/redis/redis_client.py

import redis
from .redis_settings import redis_settings


class RedisClient:
    _client: redis.Redis | None = None

    @classmethod
    def get_client(cls) -> redis.Redis:
        if cls._client is None:
            cls._client = redis.Redis(
                host=redis_settings.host,
                port=redis_settings.port,
                db=redis_settings.db,
                password=redis_settings.password,
                decode_responses=True,
            )
        return cls._client
