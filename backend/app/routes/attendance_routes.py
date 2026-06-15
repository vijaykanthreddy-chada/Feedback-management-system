from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.services.attendance_service import (
    mark_attendance,
    get_all_attendance
)

attendance_bp = Blueprint(
    "attendance_bp",
    __name__
)


@attendance_bp.route("/", methods=["POST"])
@jwt_required()
def add_attendance():
    data = request.get_json()

    response, status = mark_attendance(data)

    return jsonify(response), status


@attendance_bp.route("/", methods=["GET"])
@jwt_required()
def fetch_attendance():
    return jsonify(
        get_all_attendance()
    ), 200