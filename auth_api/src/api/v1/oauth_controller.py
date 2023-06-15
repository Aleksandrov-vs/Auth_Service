import logging
from http import HTTPStatus

from flask import Blueprint, jsonify, request, json, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import BaseModel,  constr

from src.api.v1.utils import validator_json_request, request_has_user_agent
from src.services.token_service import get_token_service
from src.repositories import token_rep
from src.core.config import settings
from src.repositories.oauth import oauth
from src.repositories.oauth_rep import get_oauth_repository, create_service

oauth_bp = Blueprint('oauth', __name__, url_prefix='/api/v1/oauth')
create_service(settings.oauth.yandex.dict())

@oauth_bp.route('/login')
def login():
    redirect_uri = url_for('oauth.authorize', _external=True)
    return oauth.yandex.authorize_redirect(redirect_uri)

@oauth_bp.route('/authorize')
def authorize():
    token = oauth.yandex.authorize_access_token()
    # Store the token in session or use it to fetch user data
    # Example: token['access_token'], token['expires_at'], token['refresh_token']

    # Fetch user data using the token
    user_info = oauth.yandex.get('user_info')
    # Process the user_info and perform further actions

    return 'Authorization successful!'
