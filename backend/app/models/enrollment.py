from datetime import datetime
from enum import Enum
from app.config.database import db


class AttendanceStatus(Enum):
    REGISTERED = "REGISTERED"
    ATTENDED = "ATTENDED"
    NO_SHOW = "NO_SHOW"


class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    program_id = db.Column(
        db.Integer,
        db.ForeignKey("training_programs.id"),
        nullable=False
    )

    attendance_status = db.Column(
        db.Enum(AttendanceStatus, native_enum=False),
        default=AttendanceStatus.REGISTERED,
        nullable=False
    )

    enrolled_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    student = db.relationship(
        "Student",
        backref="enrollments"
    )

    program = db.relationship(
        "TrainingProgram",
        backref="enrollments"
    )