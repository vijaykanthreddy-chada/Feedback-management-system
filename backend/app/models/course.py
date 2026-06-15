from datetime import datetime
from app.config.database import db


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(db.String(50), unique=True, nullable=False)

    title = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text, nullable=True)

    duration_days = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Course {self.code}>"