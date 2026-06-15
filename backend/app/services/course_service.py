from app.config.database import db
from app.models.course import Course


def create_course(data):
    code = data.get("code")
    title = data.get("title")
    description = data.get("description")
    duration_days = data.get("duration_days")

    if not code or not title or not duration_days:
        return {"error": "Code, title and duration_days are required"}, 400

    existing_course = Course.query.filter_by(code=code).first()

    if existing_course:
        return {"error": "Course code already exists"}, 409

    course = Course(
        code=code,
        title=title,
        description=description,
        duration_days=duration_days
    )

    db.session.add(course)
    db.session.commit()

    return {
        "message": "Course created successfully",
        "course": {
            "id": course.id,
            "code": course.code,
            "title": course.title,
            "duration_days": course.duration_days
        }
    }, 201


def get_all_courses():
    courses = Course.query.all()

    return [{
        "id": course.id,
        "code": course.code,
        "title": course.title,
        "description": course.description,
        "duration_days": course.duration_days
    } for course in courses]

def get_course_by_id(course_id):
    course = Course.query.get(course_id)

    if not course:
        return {"error": "Course not found"}, 404

    return {
        "id": course.id,
        "code": course.code,
        "title": course.title,
        "description": course.description,
        "duration_days": course.duration_days
    }, 200

def update_course(course_id, data):
    course = Course.query.get(course_id)

    if not course:
        return {"error": "Course not found"}, 404

    course.title = data.get("title", course.title)
    course.description = data.get("description", course.description)
    course.duration_days = data.get(
        "duration_days",
        course.duration_days
    )

    db.session.commit()

    return {
        "message": "Course updated successfully"
    }, 200

def delete_course(course_id):
    course = Course.query.get(course_id)

    if not course:
        return {"error": "Course not found"}, 404

    db.session.delete(course)
    db.session.commit()

    return {
        "message": "Course deleted successfully"
    }, 200