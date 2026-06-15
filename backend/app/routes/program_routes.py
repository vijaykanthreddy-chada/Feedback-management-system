from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.middleware.role_required import role_required
from app.services.program_service import (
    create_program,
    get_all_programs,
    assign_faculty,
    update_program,
    cancel_program,
    delete_program
)

program_bp = Blueprint(
    "program_bp",
    __name__
)


@program_bp.route("/", methods=["POST"])
@jwt_required()
@role_required("ADMIN", "COORDINATOR")
def add_program():

    data = request.get_json()

    response, status = create_program(data)

    return jsonify(response), status


@program_bp.route("/", methods=["GET"])
@jwt_required()
def fetch_programs():

    return jsonify(
        get_all_programs()
    ), 200


@program_bp.route("/<int:program_id>", methods=["PUT"])
@jwt_required()
@role_required("ADMIN", "COORDINATOR")
def edit_program(program_id):

    data = request.get_json()

    response, status = update_program(program_id, data)

    return jsonify(response), status


@program_bp.route("/<int:program_id>/cancel", methods=["PUT"])
@jwt_required()
@role_required("ADMIN", "COORDINATOR")
def cancel_training_program(program_id):

    response, status = cancel_program(program_id)

    return jsonify(response), status


@program_bp.route("/<int:program_id>", methods=["DELETE"])
@jwt_required()
@role_required("ADMIN", "COORDINATOR")
def remove_program(program_id):

    response, status = delete_program(program_id)

    return jsonify(response), status


@program_bp.route(
    "/<int:program_id>/faculty/<int:faculty_id>",
    methods=["POST"]
)
@jwt_required()
@role_required("ADMIN", "COORDINATOR")
def add_faculty_to_program(
        program_id,
        faculty_id
):

    response, status = assign_faculty(
        program_id,
        faculty_id
    )

    return jsonify(response), status