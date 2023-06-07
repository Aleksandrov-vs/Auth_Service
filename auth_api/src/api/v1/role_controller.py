import json

from flask import Blueprint, jsonify, request

from src.services.role_service import get_role_service
from src.repositories import role_rep


role_bp = Blueprint('role', __name__, url_prefix='/api/v1/auth')


@role_bp.route('/roles', methods=['POST'])
def role_create():
    role_service = get_role_service(role_rep.get_role_repository())
    new_role = role_service.create_role(**json.loads(request.data))
    return jsonify(new_role)


@role_bp.route('/roles/delete', methods=['DELETE'])
def role_delete():
    role_service = get_role_service(role_rep.get_role_repository())
    response = role_service.delete_role(**json.loads(request.data))
    return jsonify(response)


@role_bp.route('/roles/update', methods=['PUT'])
def role_update():
    role_service = get_role_service(role_rep.get_role_repository())
    response = role_service.update_role(**json.loads(request.data))
    return jsonify(response)


@role_bp.route('/roles/view', methods=['GET'])
def roles_viewed():
    role_service = get_role_service(role_rep.get_role_repository())
    response = role_service.viewing_roles()
    return jsonify(response)
