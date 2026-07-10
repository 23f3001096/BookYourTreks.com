# app/utils/cache.py

import json
import app.extensions as extensions

CACHE_EXPIRY_SECONDS = 300


def get_cache(key):
    try:
        data = extensions.redis_client.get(key)
        return json.loads(data) if data else None
    except Exception:
        return None


def set_cache(key, value, expiry=CACHE_EXPIRY_SECONDS):
    try:
        extensions.redis_client.setex(key, expiry, json.dumps(value))
    except Exception:
        pass


def delete_cache(key):
    try:
        extensions.redis_client.delete(key)
    except Exception:
        pass


def delete_cache_pattern(pattern):
    try:
        for key in extensions.redis_client.scan_iter(pattern):
            extensions.redis_client.delete(key)
    except Exception:
        pass