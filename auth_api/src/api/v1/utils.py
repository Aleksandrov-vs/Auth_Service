from functools import wraps
from typing import Type

from pydantic import BaseModel
from pydantic import ValidationError
from flask import jsonify


def body_fields_validate_with_pydantic(request_schema: Type[BaseModel]):
    def decorator(funk):
        @wraps(funk)
        def wrapper(*args, **kwargs):
            try:
                res = funk(*args, **kwargs)
            except ValidationError as e:
                return jsonify(str(e)), 400
            else:
                return res
        return wrapper
    return decorator
