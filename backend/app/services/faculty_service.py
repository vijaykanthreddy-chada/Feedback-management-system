from app.config.database import db
from app.models.faculty import Faculty
from app.models.skill import Skill


def create_faculty(data):
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return {"error": "Name and email are required"}, 400

    existing = Faculty.query.filter_by(email=email).first()

    if existing:
        return {"error": "Faculty already exists"}, 409

    faculty = Faculty(
        name=name,
        email=email
    )

    db.session.add(faculty)
    db.session.commit()

    return {
        "message": "Faculty created successfully",
        "faculty": {
            "id": faculty.id,
            "name": faculty.name,
            "email": faculty.email
        }
    }, 201


def get_all_faculties():
    faculties = Faculty.query.all()

    return [{
        "id": faculty.id,
        "name": faculty.name,
        "email": faculty.email,
        "skills": [
            {
                "id": skill.id,
                "name": skill.name
            }
            for skill in faculty.skills
        ]
    } for faculty in faculties]


def get_faculty_by_id(faculty_id):

    faculty = Faculty.query.get(faculty_id)

    if not faculty:
        return {"error": "Faculty not found"}, 404

    return {
        "id": faculty.id,
        "name": faculty.name,
        "email": faculty.email,
        "skills": [
            {
                "id": skill.id,
                "name": skill.name
            }
            for skill in faculty.skills
        ]
    }, 200


def update_faculty(faculty_id, data):
    faculty = Faculty.query.get(faculty_id)

    if not faculty:
        return {"error": "Faculty not found"}, 404

    faculty.name = data.get("name", faculty.name)
    faculty.email = data.get("email", faculty.email)

    db.session.commit()

    return {
        "message": "Faculty updated successfully"
    }, 200


def delete_faculty(faculty_id):
    faculty = Faculty.query.get(faculty_id)

    if not faculty:
        return {"error": "Faculty not found"}, 404

    db.session.delete(faculty)
    db.session.commit()

    return {
        "message": "Faculty deleted successfully"
    }, 200


def assign_skill_to_faculty(faculty_id, skill_id):

    faculty = Faculty.query.get(faculty_id)

    if not faculty:
        return {"error": "Faculty not found"}, 404

    skill = Skill.query.get(skill_id)

    if not skill:
        return {"error": "Skill not found"}, 404

    if skill in faculty.skills:
        return {"error": "Skill already assigned"}, 409

    faculty.skills.append(skill)

    db.session.commit()

    return {
        "message": "Skill assigned successfully"
    }, 200


def search_faculty_by_skill(skill_name):

    faculties = Faculty.query.join(Faculty.skills).filter(
        Skill.name.ilike(f"%{skill_name}%")
    ).all()

    return [{
        "id": faculty.id,
        "name": faculty.name,
        "email": faculty.email,
        "skills": [
            {
                "id": skill.id,
                "name": skill.name
            }
            for skill in faculty.skills
        ]
    } for faculty in faculties]