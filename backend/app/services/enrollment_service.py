from app.config.database import db
from app.models.enrollment import Enrollment
from app.models.student import Student
from app.models.training_program import TrainingProgram
from flask_jwt_extended import get_jwt_identity
from app.models.user import User


def enroll_student(data):

    student_id = data.get("student_id")
    program_id = data.get("program_id")

    student = Student.query.get(student_id)

    if not student:
        return {"error": "Student not found"}, 404

    program = TrainingProgram.query.get(program_id)

    if not program:
        return {"error": "Program not found"}, 404

    current_enrollments = Enrollment.query.filter_by(
        program_id=program_id
    ).count()

    if program.capacity is not None and current_enrollments >= program.capacity:
        return {
            "error": "Program capacity is full"
        }, 400

    existing = Enrollment.query.filter_by(
        student_id=student_id,
        program_id=program_id
    ).first()

    if existing:
        return {
            "error": "Student already enrolled"
        }, 409

    enrollment = Enrollment(
        student_id=student_id,
        program_id=program_id
    )

    db.session.add(enrollment)
    db.session.commit()

    return {
        "message": "Student enrolled successfully",
        "enrollment_id": enrollment.id
    }, 201


def get_all_enrollments():

    enrollments = Enrollment.query.all()

    result = []

    for e in enrollments:
        result.append({
            "id": e.id,
            "student": e.student.name,
            "program_id": e.program.id,
            "course": e.program.course.title
        })

    return result


def get_my_enrollments():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))

    if not user:
        return {"error": "User not found"}, 404

    student = Student.query.filter_by(email=user.email).first()

    if not student:
        return [], 200

    enrollments = Enrollment.query.filter_by(
        student_id=student.id
    ).all()

    result = []

    for e in enrollments:
        result.append({
            "id": e.id,
            "program_id": e.program.id,
            "course": e.program.course.title,
            "location": e.program.location,
            "attendance_status": e.attendance_status.value,
            "faculties": [
                {
                    "id": faculty.id,
                    "name": faculty.name
                }
                for faculty in e.program.faculties
            ]
        })

    return result, 200


def delete_enrollment(enrollment_id):

    enrollment = Enrollment.query.get(enrollment_id)

    if not enrollment:
        return {
            "error": "Enrollment not found"
        }, 404

    db.session.delete(enrollment)
    db.session.commit()

    return {
        "message": "Enrollment deleted successfully"
    }, 200