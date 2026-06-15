from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.services.enrollment_service import (
    enroll_student,
    get_all_enrollments,
    get_my_enrollments,
    delete_enrollment
)

enrollment_bp = Blueprint(
    "enrollment_bp",
    __name__
)


@enrollment_bp.route("/", methods=["POST"])
@jwt_required()
def create_enrollment():

    data = request.get_json()

    response, status = enroll_student(data)

    return jsonify(response), status


@enrollment_bp.route("/", methods=["GET"])
@jwt_required()
def fetch_enrollments():

    return jsonify(
        get_all_enrollments()
    ), 200


@enrollment_bp.route("/my", methods=["GET"])
@jwt_required()
def my_enrollments():
    response, status = get_my_enrollments()
    return jsonify(response), status


@enrollment_bp.route("/<int:enrollment_id>", methods=["DELETE"])
@jwt_required()
def remove_enrollment(enrollment_id):

    response, status = delete_enrollment(
        enrollment_id
    )

    return jsonify(response), status