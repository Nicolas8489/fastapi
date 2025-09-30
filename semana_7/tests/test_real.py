def test_cache_functionality():
    from semana_7.app.cache.redis_config import cache
    cache.set_cache("test_key", {"data": "test"})
    assert cache.get_cache("test_key") == {"data": "test"}
    cache.redis_client.delete("real_:data:test_key")
