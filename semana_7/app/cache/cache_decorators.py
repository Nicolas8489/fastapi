from functools import wraps
from .redis_config import cache

def cache_result(ttl_type: str = 'frequent_data'):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = f"{func.__name__}_{args}"
            cached = cache.get_cache(key)
            if cached:
                return cached
            result = await func(*args, **kwargs)
            cache.set_cache(key, result, ttl_type)
            return result
        return wrapper
    return decorator
