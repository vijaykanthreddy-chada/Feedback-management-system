from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.middleware.role_required import role_required
from app.services.skill_service import (
    create_skill,
    get_all_skills
)

skill_bp = Blueprint(
    "skill_bp",
    __name__
)


@skill_bp.route("/", methods=["POST"])
@jwt_required()
@role_required("ADMIN")
def add_skill():

    data = request.get_json()

    response, status = create_skill(data)

    return jsonify(response), status


@skill_bp.route("/", methods=["GET"])
@jwt_required()
def fetch_skills():

    return jsonify(
        get_all_skills()
    ), 200