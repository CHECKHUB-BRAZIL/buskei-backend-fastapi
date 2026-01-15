from redis import Redis
from app.infra.redis.redis_client import RedisClient


def get_redis() -> Redis:
    return RedisClient.get_client()
