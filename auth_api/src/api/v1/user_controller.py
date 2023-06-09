from flask import Blueprint, jsonify
from pydantic import BaseModel
from src.repositories import user_rep
from src.services.user_service import get_user_service

from .utils import validator_json_request

user_bp = Blueprint('user', __name__, url_prefix='/api/v1/auth')


class RoleValidator(BaseModel):
    role_name: str


@user_bp.route('/users/<login>', methods=['GET'])
def get_user(login):
    user_service = get_user_service(user_rep.get_user_repository())
    response = user_service.get_user(login=login)
    return jsonify(response)


@user_bp.route('/users/<user_id>/assign-role', methods=['POST'])
@validator_json_request(RoleValidator)
def assign_role(body: RoleValidator, user_id):
    user_service = get_user_service(user_rep.get_user_repository())
    params = body.dict()
    response = user_service.assign_role(user_id=user_id, **params)
    return jsonify(response)


@user_bp.route('/users/<user_id>/revoke-role', methods=['POST'])
@validator_json_request(RoleValidator)
def revoke_role(body: RoleValidator, user_id):
    user_service = get_user_service(user_rep.get_user_repository())
    params = body.dict()
    response = user_service.revoke_role(user_id=user_id, **params)
    return jsonify(response)


@user_bp.route('/users/<user_id>/check-permissions', methods=['GET'])
def check_role(user_id):
    user_service = get_user_service(user_rep.get_user_repository())
    roles = user_service.viewing_role(user_id=user_id)
    return jsonify(roles)


@user_bp.route('/users/<user_id>/history', methods=['GET'])
def user_history(user_id):
    user_service = get_user_service(user_rep.get_user_repository())
    history = user_service.user_history(user_id=user_id)
    return jsonify(history)
