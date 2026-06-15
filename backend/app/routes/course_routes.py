from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.middleware.role_required import role_required
from app.services.course_service import (
    create_course,
    get_all_courses,
    get_course_by_id,
    update_course,
    delete_course
)

course_bp = Blueprint("course_bp", __name__)


@course_bp.route("/", methods=["POST"])
@jwt_required()
@role_required("ADMIN")
def add_course():
    data = request.get_json()
    response, status = create_course(data)
    return jsonify(response), status


@course_bp.route("/", methods=["GET"])
@jwt_required()
def fetch_courses():
    return jsonify(get_all_courses()), 200

@course_bp.route("/<int:course_id>", methods=["GET"])
@jwt_required()
def get_course(course_id):
    response, status = get_course_by_id(course_id)
    return jsonify(response), status


@course_bp.route("/<int:course_id>", methods=["PUT"])
@jwt_required()
@role_required("ADMIN")
def edit_course(course_id):
    data = request.get_json()
    response, status = update_course(course_id, data)
    return jsonify(response), status


@course_bp.route("/<int:course_id>", methods=["DELETE"])
@jwt_required()
@role_required("ADMIN")
def remove_course(course_id):
    response, status = delete_course(course_id)
    return jsonify(response), status



