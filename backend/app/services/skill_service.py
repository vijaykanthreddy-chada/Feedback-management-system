from app.config.database import db
from app.models.skill import Skill


def create_skill(data):
    name = data.get("name")

    if not name:
        return {"error": "Skill name required"}, 400

    existing = Skill.query.filter_by(name=name).first()

    if existing:
        return {"error": "Skill already exists"}, 409

    skill = Skill(name=name)

    db.session.add(skill)
    db.session.commit()

    return {
        "message": "Skill created successfully",
        "skill": {
            "id": skill.id,
            "name": skill.name
        }
    }, 201


def get_all_skills():
    skills = Skill.query.all()

    return [{
        "id": skill.id,
        "name": skill.name
    } for skill in skills]