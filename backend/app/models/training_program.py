from datetime import datetime
from enum import Enum
from app.config.database import db


class ProgramStatus(Enum):
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


program_faculties = db.Table(
    "program_faculties",
    db.Column("program_id", db.Integer, db.ForeignKey("training_programs.id"), primary_key=True),
    db.Column("faculty_id", db.Integer, db.ForeignKey("faculties.id"), primary_key=True)
)


class TrainingProgram(db.Model):
    __tablename__ = "training_programs"

    id = db.Column(db.Integer, primary_key=True)

    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    coordinator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    location = db.Column(db.String(150), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    status = db.Column(
        db.Enum(ProgramStatus, native_enum=False),
        default=ProgramStatus.SCHEDULED,
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    course = db.relationship("Course", backref="programs")
    coordinator = db.relationship("User", backref="coordinated_programs")

    faculties = db.relationship(
        "Faculty",
        secondary=program_faculties,
        backref="training_programs"
    )