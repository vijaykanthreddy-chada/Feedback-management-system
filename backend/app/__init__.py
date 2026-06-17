from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

from app.config.database import db

migrate = Migrate()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    )

    load_dotenv()

    app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}/"
    f"{os.getenv('DB_NAME')}")

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    from app.models.user import User
    from app.models.course import Course
    from app.models.faculty import Faculty
    from app.models.skill import Skill
    from app.models.student import Student
    from app.models.training_program import TrainingProgram
    from app.models.enrollment import Enrollment
    from app.models.attendance import Attendance
    from app.models.feedback import Feedback

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


    from app.routes.user_routes import user_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.course_routes import course_bp
    from app.routes.faculty_routes import faculty_bp
    from app.routes.skill_routes import skill_bp
    from app.routes.student_routes import student_bp
    from app.routes.program_routes import program_bp
    from app.routes.enrollment_routes import enrollment_bp
    from app.routes.attendance_routes import attendance_bp
    from app.routes.feedback_routes import feedback_bp
    from app.routes.report_routes import report_bp



    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(course_bp,url_prefix="/api/courses")
    app.register_blueprint(faculty_bp,url_prefix="/api/faculties")
    app.register_blueprint(skill_bp,url_prefix="/api/skills")
    app.register_blueprint(student_bp, url_prefix="/api/students")
    app.register_blueprint(program_bp,url_prefix="/api/programs")
    app.register_blueprint(enrollment_bp,url_prefix="/api/enrollments")
    app.register_blueprint(attendance_bp,url_prefix="/api/attendance")
    app.register_blueprint(feedback_bp,url_prefix="/api/feedbacks")
    app.register_blueprint(report_bp, url_prefix="/api/reports")

    @app.route("/")
    def home():
        return "Feedback Management Backend is running"   

    return app