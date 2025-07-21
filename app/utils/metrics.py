import time
from functools import wraps
from flask import request, g

def track_request_time(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        
        # Registrar métrica
        request_time = end_time - start_time
        # metrics.histogram('request_duration_seconds', request_time)
        
        return result
    return decorated_function 