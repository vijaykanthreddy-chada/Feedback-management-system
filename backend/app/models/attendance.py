from datetime import datetime
from app.config.database import db


class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    enrollment_id = db.Column(
        db.Integer,
        db.ForeignKey("enrollments.id"),
        nullable=False
    )

    attendance_date = db.Column(
        db.Date,
        nullable=False
    )

    present = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    enrollment = db.relationship(
        "Enrollment",
        backref="attendance_records"
    )