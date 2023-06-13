from functools import wraps
from http import HTTPStatus

import redis
from flask import jsonify, request
from opentelemetry import trace

from src.core.config import settings


redis_rate_limit = redis.StrictRedis(
    host=settings.redis.host,
    port=settings.redis.port,
    db=1,
    decode_responses=True
)


def rate_limit(
    request_limit=settings.default_rate_limit,
    period=settings.default_rate_period,
    max_penalty=settings.max_rate_penalty
):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            tracer = trace.get_tracer(__name__)
            with tracer.start_as_current_span("rate-limit-checking"):
                pipeline = redis_rate_limit.pipeline()
                key = f"{request.remote_addr}:{request.path}"
                pipeline.incr(key, 1)
                pipeline.expire(key, period)

                try:
                    request_number = pipeline.execute()[0]
                except redis.exceptions.RedisError:
                    return jsonify(msg=f"Redis error"), HTTPStatus.INTERNAL_SERVER_ERROR

                penalty = 0
                if request_number > request_limit:
                    excess_requests = request_number - request_limit
                    penalty = period * (2 ** (excess_requests - 1))
                    penalty = penalty if penalty < max_penalty else max_penalty

                    pipeline.expire(key, penalty)

                    try:
                        pipeline.execute()
                    except redis.exceptions.RedisError:
                        return jsonify(msg=f"Redis error"), HTTPStatus.INTERNAL_SERVER_ERROR

                    return jsonify(
                        msg="Too many requests",
                        retry_after=penalty
                    ), HTTPStatus.TOO_MANY_REQUESTS

            return func(*args, **kwargs)
        return inner
    return wrapper
