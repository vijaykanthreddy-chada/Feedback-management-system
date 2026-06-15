from flask_jwt_extended import get_jwt_identity

from app.config.database import db
from app.models.feedback import Feedback
from app.models.enrollment import Enrollment, AttendanceStatus
from app.models.faculty import Faculty
from app.models.user import User


def create_feedback(data):
    enrollment_id = data.get("enrollment_id")
    faculty_id = data.get("faculty_id")
    rating = data.get("rating")
    comments = data.get("comments")

    if not enrollment_id or not faculty_id or rating is None:
        return {
            "error": "Enrollment ID, faculty ID and rating are required"
        }, 400

    if not isinstance(rating, int):
        return {"error": "Rating must be a number"}, 400

    if rating < 1 or rating > 5:
        return {"error": "Rating must be between 1 and 5"}, 400

    enrollment = Enrollment.query.get(enrollment_id)

    if not enrollment:
        return {"error": "Enrollment not found"}, 404

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user and user.role.value == "PARTICIPANT":
        if enrollment.student.email != user.email:
            return {
                "error": "You can give feedback only for your own enrollment"
            }, 403

    if enrollment.attendance_status != AttendanceStatus.ATTENDED:
        return {
            "error": "Feedback allowed only for attended participants"
        }, 403

    faculty = Faculty.query.get(faculty_id)

    if not faculty:
        return {"error": "Faculty not found"}, 404

    existing_feedback = Feedback.query.filter_by(
        enrollment_id=enrollment_id,
        faculty_id=faculty_id
    ).first()

    if existing_feedback:
        return {
            "error": "Feedback already submitted for this faculty"
        }, 409

    feedback = Feedback(
        enrollment_id=enrollment_id,
        faculty_id=faculty_id,
        rating=rating,
        comments=comments
    )

    db.session.add(feedback)
    db.session.commit()

    return {
        "message": "Feedback submitted successfully",
        "feedback_id": feedback.id
    }, 201


def get_all_feedback():
    feedbacks = Feedback.query.all()

    result = []

    for feedback in feedbacks:
        result.append({
            "id": feedback.id,
            "enrollment_id": feedback.enrollment_id,
            "faculty_id": feedback.faculty_id,
            "rating": feedback.rating,
            "comments": feedback.comments
        })

    return result


def get_faculty_average_rating(faculty_id):
    feedbacks = Feedback.query.filter_by(
        faculty_id=faculty_id
    ).all()

    if not feedbacks:
        return {
            "faculty_id": faculty_id,
            "average_rating": 0
        }

    total = sum(
        feedback.rating
        for feedback in feedbacks
    )

    average = total / len(feedbacks)

    return {
        "faculty_id": faculty_id,
        "average_rating": round(average, 2)
    }