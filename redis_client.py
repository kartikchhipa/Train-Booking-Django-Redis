import os
import redis

# Connect to Redis
redis_client = redis.Redis(host="127.0.0.1", port=6379)

# Constants
LOCK_EXPIRATION_TIME = 180  # 3 minutes