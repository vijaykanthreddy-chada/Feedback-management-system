from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.user_service import get_users_by_role

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/", methods=["GET"])
@jwt_required()
def get_users():
    role = request.args.get("role")

    users = get_users_by_role(role)

    return jsonify(users), 200