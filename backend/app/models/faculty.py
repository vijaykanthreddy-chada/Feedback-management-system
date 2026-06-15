from datetime import datetime
from app.config.database import db


faculty_skills = db.Table(
    "faculty_skills",
    db.Column(
        "faculty_id",
        db.Integer,
        db.ForeignKey("faculties.id"),
        primary_key=True
    ),
    db.Column(
        "skill_id",
        db.Integer,
        db.ForeignKey("skills.id"),
        primary_key=True
    )
)


class Faculty(db.Model):
    __tablename__ = "faculties"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    skills = db.relationship(
        "Skill",
        secondary=faculty_skills,
        backref="faculties"
    )

    def __repr__(self):
        return f"<Faculty {self.email}>"