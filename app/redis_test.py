from redis import Redis

redis = Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
)

redis.set("health_check", "ok")

value = redis.get("health_check")
print("Redis respondeu:", value)
