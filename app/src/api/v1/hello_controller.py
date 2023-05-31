from flask import Blueprint, jsonify

hello_bp = Blueprint('hello', __name__, url_prefix='/hello_world')


@hello_bp.route('/hello_world')
def hello_world():
    return jsonify('Hello, World!')
