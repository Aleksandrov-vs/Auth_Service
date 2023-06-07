import json
from functools import wraps
from typing import Type

from pydantic import BaseModel
from pydantic import ValidationError
from flask import jsonify, request


def body_fields_validate_with_pydantic(request_schema: Type[BaseModel]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                body = json.loads(request.data)
            except json.JSONDecodeError:
                return jsonify({'err_msg': 'json is not valid'}), 400
            try:
                body = request_schema(**body)
                res = func(body, *args, **kwargs)
            except ValidationError as e:
                return jsonify({'err_msg': str(e)}), 400
            else:
                return res
        return wrapper
    return decorator


def request_has_user_agent(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.headers.get('User-Agent'):
            return jsonify({'err_msg': 'User-Agent is require.'}), 400
        res = func(*args, **kwargs)
        return res
    return wrapper
