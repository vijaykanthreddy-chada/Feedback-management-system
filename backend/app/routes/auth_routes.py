from flask import Blueprint, request, jsonify

from app.services.auth_service import register_user, login_user

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/", methods=["GET"])
def auth_home():
    return jsonify({"message": "Auth route working"}), 200


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    response, status_code = register_user(data)
    return jsonify(response), status_code


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    response, status_code = login_user(data)
    return jsonify(response), status_code