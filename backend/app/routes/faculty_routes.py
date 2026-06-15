from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.middleware.role_required import role_required
from app.services.faculty_service import (
    create_faculty,
    get_all_faculties,
    assign_skill_to_faculty,
    get_faculty_by_id,
    search_faculty_by_skill,
    update_faculty,
    delete_faculty
)

faculty_bp = Blueprint(
    "faculty_bp",
    __name__
)


@faculty_bp.route("/", methods=["POST"])
@jwt_required()
@role_required("ADMIN")
def add_faculty():
    data = request.get_json()

    response, status = create_faculty(data)

    return jsonify(response), status


@faculty_bp.route("/", methods=["GET"])
@jwt_required()
def fetch_faculties():
    return jsonify(
        get_all_faculties()
    ), 200


@faculty_bp.route("/search", methods=["GET"])
@jwt_required()
def search_faculty():
    skill = request.args.get("skill")

    if not skill:
        return jsonify({"error": "Skill query is required"}), 400

    return jsonify(search_faculty_by_skill(skill)), 200


@faculty_bp.route(
    "/<int:faculty_id>/skills/<int:skill_id>",
    methods=["POST"]
)
@jwt_required()
@role_required("ADMIN")
def assign_skill(faculty_id, skill_id):

    response, status = assign_skill_to_faculty(
        faculty_id,
        skill_id
    )

    return jsonify(response), status


@faculty_bp.route("/<int:faculty_id>", methods=["GET"])
@jwt_required()
def get_faculty(faculty_id):

    response, status = get_faculty_by_id(
        faculty_id
    )

    return jsonify(response), status


@faculty_bp.route("/<int:faculty_id>", methods=["PUT"])
@jwt_required()
@role_required("ADMIN")
def edit_faculty(faculty_id):
    data = request.get_json()

    response, status = update_faculty(faculty_id, data)

    return jsonify(response), status


@faculty_bp.route("/<int:faculty_id>", methods=["DELETE"])
@jwt_required()
@role_required("ADMIN")
def remove_faculty(faculty_id):
    response, status = delete_faculty(faculty_id)

    return jsonify(response), status