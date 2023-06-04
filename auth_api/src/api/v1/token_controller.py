import logging

from flask import Blueprint, jsonify, request, json
from pydantic import BaseModel

from src.services.token_service import get_token_service
from src.repositories import token_rep


token = Blueprint('token', __name__, url_prefix='/api/v1/auth')


@token.route('/change-password', methods=["POST"])
def change_password():
    token_service = get_token_service(token_rep.get_token_repository())
    response = token_service.change_password()
    return jsonify(response)


@token.route('/login')
def login():
    token_service = get_token_service(token_rep.get_token_repository())
    response = token_service.login()
    return jsonify(response)


@token.route('/logout')
def logout():
    response = token_service.logout()
    return jsonify(response)


@token.route('/refresh-tokens')
def refresh_tokens():
    response = token_service.refresh_tokens()
    return jsonify(response)


class RegisterRequest(BaseModel):
    login: str
    password: str


@token.route('/register', methods=["POST"])
def register():
    token_service = get_token_service(token_rep.get_token_repository())
    body = RegisterRequest(**json.loads(request.data))
    response = token_service.register(body.login, body.password)
    return jsonify(response)
