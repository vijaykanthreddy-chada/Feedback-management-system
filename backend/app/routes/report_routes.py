from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.services.report_service import (
    dashboard_summary,
    program_enrollment_report,
    program_attendance_report,
    faculty_performance_report,
    program_feedback_summary,
    program_feedback_summary_csv,
    defaulters_report
)

report_bp = Blueprint("report_bp", __name__)


@report_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():
    return jsonify(dashboard_summary()), 200


@report_bp.route("/programs/<int:program_id>/enrollments", methods=["GET"])
@jwt_required()
def program_enrollments(program_id):
    response, status = program_enrollment_report(program_id)
    return jsonify(response), status


@report_bp.route("/programs/<int:program_id>/attendance", methods=["GET"])
@jwt_required()
def program_attendance(program_id):
    response, status = program_attendance_report(program_id)
    return jsonify(response), status


@report_bp.route("/faculty/<int:faculty_id>/performance", methods=["GET"])
@jwt_required()
def faculty_performance(faculty_id):
    response, status = faculty_performance_report(faculty_id)
    return jsonify(response), status


@report_bp.route("/program/<int:program_id>/summary", methods=["GET"])
@jwt_required()
def program_summary(program_id):
    if request.args.get("format") == "csv":
        return program_feedback_summary_csv(program_id)

    response, status = program_feedback_summary(program_id)
    return jsonify(response), status


@report_bp.route("/defaulters/<int:program_id>", methods=["GET"])
@jwt_required()
def feedback_defaulters(program_id):
    response, status = defaulters_report(program_id)
    return jsonify(response), status