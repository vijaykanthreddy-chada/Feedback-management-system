from datetime import datetime
from app.config.database import db


class Feedback(db.Model):
    __tablename__ = "feedbacks"

    __table_args__ = (
        db.UniqueConstraint(
            "enrollment_id",
            "faculty_id",
            name="unique_feedback_per_enrollment_faculty"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    enrollment_id = db.Column(
        db.Integer,
        db.ForeignKey("enrollments.id"),
        nullable=False
    )

    faculty_id = db.Column(
        db.Integer,
        db.ForeignKey("faculties.id"),
        nullable=False
    )

    faculty_rating = db.Column(db.Integer, nullable=False)
    curriculum_rating = db.Column(db.Integer, nullable=False)
    program_structure_rating = db.Column(db.Integer, nullable=False)
    overall_rating = db.Column(db.Integer, nullable=False)

    comments = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    enrollment = db.relationship(
        "Enrollment",
        backref="feedbacks"
    )

    faculty = db.relationship(
        "Faculty",
        backref="feedbacks"
    )

    def __repr__(self):
        return f"<Feedback enrollment={self.enrollment_id} faculty={self.faculty_id}>"