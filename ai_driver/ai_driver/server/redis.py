import redis

REDIS_HOST = "ai_driver_redis"
REDIS_PORT = 26379
REDIS_DB = 0

redis_client = redis.StrictRedis(
    host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True
)
