from app.config.database import db
from app.models.student import Student
from app.models.course import Course
from app.models.user import User, UserRole
from app.models.enrollment import Enrollment
from app.models.attendance import Attendance
from app.models.feedback import Feedback


def create_student(data):
    email = data.get("email")
    course_id = data.get("course_id")

    if not email:
        return {"error": "Email is required"}, 400

    existing = Student.query.filter_by(email=email).first()
    if existing:
        return {"error": "Student already exists"}, 409

    user = User.query.filter_by(email=email).first()

    if not user:
        return {"error": "Participant must register first"}, 404

    if user.role != UserRole.PARTICIPANT:
        return {"error": "Only PARTICIPANT user can be added as student"}, 403

    if course_id:
        course = Course.query.get(course_id)
        if not course:
            return {"error": "Course not found"}, 404

    student = Student(
        name=user.name,
        email=user.email,
        course_id=course_id
    )

    db.session.add(student)
    db.session.commit()

    return {
        "message": "Student created successfully",
        "student": {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "course_id": student.course_id
        }
    }, 201


def get_all_students():
    students = Student.query.all()

    return [{
        "id": student.id,
        "name": student.name,
        "email": student.email,
        "course_id": student.course_id,
        "course": {
            "id": student.course.id,
            "code": student.course.code,
            "title": student.course.title
        } if student.course else None
    } for student in students]


def update_student(student_id, data):
    student = Student.query.get(student_id)

    if not student:
        return {"error": "Student not found"}, 404

    course_id = data.get("course_id")

    if course_id:
        course = Course.query.get(course_id)

        if not course:
            return {"error": "Course not found"}, 404

        student.course_id = course_id

    db.session.commit()

    return {
        "message": "Student updated successfully"
    }, 200


def delete_student(student_id):
    student = Student.query.get(student_id)

    if not student:
        return {"error": "Student not found"}, 404

    enrollments = Enrollment.query.filter_by(student_id=student_id).all()

    for enrollment in enrollments:
        Attendance.query.filter_by(enrollment_id=enrollment.id).delete()
        Feedback.query.filter_by(enrollment_id=enrollment.id).delete()

    Enrollment.query.filter_by(student_id=student_id).delete()

    db.session.delete(student)
    db.session.commit()

    return {
        "message": "Student deleted successfully"
    }, 200    