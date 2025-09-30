import redis
import json
from typing import Optional, Any
import os

class RealCacheConfig:
    def __init__(self):
        self.redis_client = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379, db=0, decode_responses=True)
        self.cache_ttl = {'frequent_data': 300, 'stable_data': 3600}

    def get_cache(self, key: str) -> Optional[Any]:
        cache_key = f"real_:data:{key}"
        cached = self.redis_client.get(cache_key)
        return json.loads(cached) if cached else None

    def set_cache(self, key: str, value: Any, ttl_type: str = 'frequent_data'):
        cache_key = f"real_:data:{key}"
        self.redis_client.setex(cache_key, self.cache_ttl[ttl_type], json.dumps(value))

cache = RealCacheConfig()
