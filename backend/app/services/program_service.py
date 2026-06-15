from datetime import datetime

from app.config.database import db
from app.models.training_program import (
    TrainingProgram,
    ProgramStatus
)
from app.models.course import Course
from app.models.user import User
from app.models.faculty import Faculty


def create_program(data):

    course_id = data.get("course_id")
    coordinator_id = data.get("coordinator_id")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    location = data.get("location")
    capacity = data.get("capacity")

    if not course_id or not coordinator_id or not start_date or not end_date:
        return {
            "error": "Course ID, coordinator ID, start date and end date are required"
        }, 400

    course = Course.query.get(course_id)

    if not course:
        return {"error": "Course not found"}, 404

    coordinator = User.query.get(coordinator_id)

    if not coordinator:
        return {"error": "Coordinator not found"}, 404

    try:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return {"error": "Date format must be YYYY-MM-DD"}, 400

    if start >= end:
        return {"error": "Start date must be before end date"}, 400

    if capacity is not None and int(capacity) <= 0:
        return {"error": "Capacity must be greater than 0"}, 400

    program = TrainingProgram(
        course_id=course_id,
        coordinator_id=coordinator_id,
        start_date=start,
        end_date=end,
        location=location,
        capacity=capacity,
        status=ProgramStatus.SCHEDULED
    )

    db.session.add(program)
    db.session.commit()

    return {
        "message": "Program created successfully",
        "program": {
            "id": program.id,
            "course_id": program.course_id,
            "coordinator_id": program.coordinator_id
        }
    }, 201


def get_all_programs():

    programs = TrainingProgram.query.all()

    result = []

    for p in programs:
        result.append({
            "id": p.id,
            "course_id": p.course_id,
            "coordinator_id": p.coordinator_id,
            "course": p.course.title,
            "location": p.location,
            "capacity": p.capacity,
            "start_date": str(p.start_date),
            "end_date": str(p.end_date),
            "status": p.status.value
        })

    return result


def update_program(program_id, data):

    program = TrainingProgram.query.get(program_id)

    if not program:
        return {"error": "Program not found"}, 404

    course_id = data.get("course_id", program.course_id)
    coordinator_id = data.get("coordinator_id", program.coordinator_id)
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    location = data.get("location", program.location)
    capacity = data.get("capacity", program.capacity)
    status = data.get("status")

    course = Course.query.get(course_id)

    if not course:
        return {"error": "Course not found"}, 404

    coordinator = User.query.get(coordinator_id)

    if not coordinator:
        return {"error": "Coordinator not found"}, 404

    try:
        start = datetime.strptime(
            start_date,
            "%Y-%m-%d"
        ).date() if start_date else program.start_date

        end = datetime.strptime(
            end_date,
            "%Y-%m-%d"
        ).date() if end_date else program.end_date

    except ValueError:
        return {"error": "Date format must be YYYY-MM-DD"}, 400

    if start >= end:
        return {"error": "Start date must be before end date"}, 400

    if capacity is not None and int(capacity) <= 0:
        return {"error": "Capacity must be greater than 0"}, 400

    if status:
        try:
            program.status = ProgramStatus(status)
        except ValueError:
            return {"error": "Invalid program status"}, 400

    program.course_id = course_id
    program.coordinator_id = coordinator_id
    program.start_date = start
    program.end_date = end
    program.location = location
    program.capacity = capacity

    db.session.commit()

    return {
        "message": "Program updated successfully"
    }, 200


def cancel_program(program_id):

    program = TrainingProgram.query.get(program_id)

    if not program:
        return {"error": "Program not found"}, 404

    program.status = ProgramStatus.CANCELLED

    db.session.commit()

    return {
        "message": "Program cancelled successfully"
    }, 200


def delete_program(program_id):

    program = TrainingProgram.query.get(program_id)

    if not program:
        return {"error": "Program not found"}, 404

    db.session.delete(program)
    db.session.commit()

    return {
        "message": "Program deleted successfully"
    }, 200


def assign_faculty(program_id, faculty_id):

    program = TrainingProgram.query.get(program_id)

    if not program:
        return {"error": "Program not found"}, 404

    faculty = Faculty.query.get(faculty_id)

    if not faculty:
        return {"error": "Faculty not found"}, 404

    if faculty in program.faculties:
        return {
            "error": "Faculty already assigned"
        }, 409

    program.faculties.append(faculty)

    db.session.commit()

    return {
        "message": "Faculty assigned successfully"
    }, 200