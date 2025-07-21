from functools import wraps
import hashlib
import json
from flask import request

def cache_result(expire_time=300):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Criar chave única baseada nos parâmetros
            cache_key = hashlib.md5(
                json.dumps(request.get_json(), sort_keys=True).encode()
            ).hexdigest()
            
            # Verificar cache (implementar Redis/Memcached)
            # cached_result = cache.get(cache_key)
            # if cached_result:
            #     return cached_result
            
            result = f(*args, **kwargs)
            # cache.set(cache_key, result, expire_time)
            return result
        return decorated_function
    return decorator 