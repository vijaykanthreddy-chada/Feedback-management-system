from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.middleware.role_required import role_required
from app.services.student_service import (
    create_student,
    get_all_students,
    update_student,
    delete_student
)

student_bp = Blueprint("student_bp", __name__)


@student_bp.route("/", methods=["POST"])
@jwt_required()
@role_required("ADMIN")
def add_student():
    data = request.get_json()
    response, status = create_student(data)
    return jsonify(response), status


@student_bp.route("/", methods=["GET"])
@jwt_required()
def fetch_students():
    return jsonify(get_all_students()), 200



@student_bp.route("/<int:student_id>", methods=["PUT"])
@jwt_required()
@role_required("ADMIN")
def edit_student(student_id):
    data = request.get_json()

    response, status = update_student(
        student_id,
        data
    )

    return jsonify(response), status


@student_bp.route("/<int:student_id>", methods=["DELETE"])
@jwt_required()
@role_required("ADMIN")
def remove_student(student_id):

    response, status = delete_student(
        student_id
    )

    return jsonify(response), status    