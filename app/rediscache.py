import redis
"""
This file initializes the redis client to be used for caching the search results.
"""
redis_client = redis.Redis(host='redis', port=6379, db=0)