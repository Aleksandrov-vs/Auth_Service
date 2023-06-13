from functools import wraps
import asyncio

from opentelemetry import trace


def tracer(name: str = None):
    def wrapper(func):
        if not asyncio.iscoroutinefunction(func):
            @wraps(func)
            def inner(*args, **kwargs):
                tracer = trace.get_tracer(__name__)
                with tracer.start_as_current_span(func.__name__ if not name else name):
                    return func(*args, **kwargs)
        else:
            @wraps(func)
            async def inner(*args, **kwargs):
                tracer = trace.get_tracer(__name__)
                with tracer.start_as_current_span(func.__name__ if not name else name):
                    return await func(*args, **kwargs)
        return inner
    return wrapper
