from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from app.middleware.role_required import role_required
from app.services.feedback_service import (
    create_feedback,
    get_all_feedback,
    get_faculty_average_rating
)

feedback_bp = Blueprint("feedback_bp", __name__)


@feedback_bp.route("/", methods=["POST"])
@jwt_required()
@role_required("PARTICIPANT")
def add_feedback():
    data = request.get_json()
    claims = get_jwt()

    response, status = create_feedback(data)

    return jsonify(response), status


@feedback_bp.route("/", methods=["GET"])
@jwt_required()
def fetch_feedback():
    return jsonify(get_all_feedback()), 200


@feedback_bp.route("/faculty/<int:faculty_id>/rating", methods=["GET"])
@jwt_required()
def faculty_rating(faculty_id):
    return jsonify(get_faculty_average_rating(faculty_id)), 200