from datetime import date, timedelta
from werkzeug.security import generate_password_hash

from app import create_app
from app.config.database import db
from app.models.user import User, UserRole
from app.models.course import Course
from app.models.skill import Skill
from app.models.faculty import Faculty
from app.models.student import Student
from app.models.training_program import TrainingProgram, ProgramStatus
from app.models.enrollment import Enrollment, AttendanceStatus
from app.models.attendance import Attendance
from app.models.feedback import Feedback

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # ── Users ──────────────────────────────────────────────────────────
    users = [
        User(name="Admin User", email="admin@test.com",
             password_hash=generate_password_hash("password123"),
             role=UserRole.ADMIN),
        User(name="Coordinator Alice", email="alice@test.com",
             password_hash=generate_password_hash("password123"),
             role=UserRole.COORDINATOR),
        User(name="Coordinator Bob", email="bob@test.com",
             password_hash=generate_password_hash("password123"),
             role=UserRole.COORDINATOR),
        User(name="Participant Charlie", email="charlie@test.com",
             password_hash=generate_password_hash("password123"),
             role=UserRole.PARTICIPANT),
        User(name="Participant Diana", email="diana@test.com",
             password_hash=generate_password_hash("password123"),
             role=UserRole.PARTICIPANT),
        User(name="Participant Eve", email="eve@test.com",
             password_hash=generate_password_hash("password123"),
             role=UserRole.PARTICIPANT),
        User(name="Participant Frank", email="frank@test.com",
             password_hash=generate_password_hash("password123"),
             role=UserRole.PARTICIPANT),
        User(name="Participant Grace", email="grace@test.com",
             password_hash=generate_password_hash("password123"),
             role=UserRole.PARTICIPANT),
    ]
    db.session.add_all(users)
    db.session.commit()

    # ── Courses ────────────────────────────────────────────────────────
    courses = [
        Course(code="PY101", title="Python Fundamentals",
               description="Learn Python basics: variables, loops, functions, and OOP.",
               duration_days=5),
        Course(code="WD201", title="Web Development with Angular",
               description="Build modern SPAs using Angular, TypeScript, and REST APIs.",
               duration_days=10),
        Course(code="DS301", title="Data Science & Machine Learning",
               description="Pandas, NumPy, scikit-learn, and ML workflows.",
               duration_days=15),
        Course(code="CL401", title="Cloud Computing with AWS",
               description="EC2, S3, Lambda, and infrastructure as code.",
               duration_days=8),
        Course(code="DO501", title="DevOps & CI/CD Pipelines",
               description="Docker, Kubernetes, Jenkins, and GitHub Actions.",
               duration_days=12),
    ]
    db.session.add_all(courses)
    db.session.commit()

    # ── Skills ─────────────────────────────────────────────────────────
    skills = [
        Skill(name="Python"),
        Skill(name="JavaScript"),
        Skill(name="Machine Learning"),
        Skill(name="AWS"),
        Skill(name="Docker"),
        Skill(name="Angular"),
    ]
    db.session.add_all(skills)
    db.session.commit()

    # ── Faculty ────────────────────────────────────────────────────────
    faculty_list = [
        Faculty(name="Dr. Smith", email="smith@faculty.com"),
        Faculty(name="Prof. Johnson", email="johnson@faculty.com"),
        Faculty(name="Dr. Williams", email="williams@faculty.com"),
        Faculty(name="Prof. Brown", email="brown@faculty.com"),
    ]

    faculty_skills_map = [
        [skills[0], skills[1]],
        [skills[2], skills[5]],
        [skills[3]],
        [skills[4], skills[0]],
    ]

    for f, sk_list in zip(faculty_list, faculty_skills_map):
        f.skills.extend(sk_list)

    db.session.add_all(faculty_list)
    db.session.commit()

    # ── Students ───────────────────────────────────────────────────────
    students = [
        Student(name="Charlie Student", email="charlie@test.com", course_id=courses[0].id),
        Student(name="Diana Student", email="diana@test.com", course_id=courses[1].id),
        Student(name="Eve Student", email="eve@test.com", course_id=courses[2].id),
        Student(name="Frank Student", email="frank@test.com", course_id=courses[0].id),
        Student(name="Grace Student", email="grace@test.com", course_id=courses[3].id),
    ]
    db.session.add_all(students)
    db.session.commit()

    # ── Training Programs ──────────────────────────────────────────────
    today = date.today()

    programs = [
        TrainingProgram(
            course_id=courses[0].id,
            coordinator_id=users[1].id,
            start_date=today - timedelta(days=20),
            end_date=today - timedelta(days=15),
            location="Room 101",
            capacity=30,
            status=ProgramStatus.COMPLETED,
        ),
        TrainingProgram(
            course_id=courses[1].id,
            coordinator_id=users[1].id,
            start_date=today - timedelta(days=5),
            end_date=today + timedelta(days=5),
            location="Lab 202",
            capacity=25,
            status=ProgramStatus.SCHEDULED,
        ),
        TrainingProgram(
            course_id=courses[2].id,
            coordinator_id=users[2].id,
            start_date=today + timedelta(days=10),
            end_date=today + timedelta(days=25),
            location="Online - Zoom",
            capacity=50,
            status=ProgramStatus.SCHEDULED,
        ),
    ]

    program_faculties_map = [
        [faculty_list[0], faculty_list[1]],
        [faculty_list[1]],
        [faculty_list[2], faculty_list[3]],
    ]

    for p, f_list in zip(programs, program_faculties_map):
        p.faculties.extend(f_list)

    db.session.add_all(programs)
    db.session.commit()

    # ── Enrollments ────────────────────────────────────────────────────
    enrollments = [
        Enrollment(student_id=students[0].id, program_id=programs[0].id,
                   attendance_status=AttendanceStatus.ATTENDED),
        Enrollment(student_id=students[1].id, program_id=programs[0].id,
                   attendance_status=AttendanceStatus.ATTENDED),
        Enrollment(student_id=students[2].id, program_id=programs[0].id,
                   attendance_status=AttendanceStatus.NO_SHOW),
        Enrollment(student_id=students[3].id, program_id=programs[0].id,
                   attendance_status=AttendanceStatus.ATTENDED),
        Enrollment(student_id=students[4].id, program_id=programs[0].id,
                   attendance_status=AttendanceStatus.REGISTERED),

        Enrollment(student_id=students[0].id, program_id=programs[1].id,
                   attendance_status=AttendanceStatus.REGISTERED),
        Enrollment(student_id=students[1].id, program_id=programs[1].id,
                   attendance_status=AttendanceStatus.REGISTERED),
        Enrollment(student_id=students[2].id, program_id=programs[1].id,
                   attendance_status=AttendanceStatus.REGISTERED),
        Enrollment(student_id=students[3].id, program_id=programs[1].id,
                   attendance_status=AttendanceStatus.REGISTERED),

        Enrollment(student_id=students[0].id, program_id=programs[2].id,
                   attendance_status=AttendanceStatus.REGISTERED),
        Enrollment(student_id=students[4].id, program_id=programs[2].id,
                   attendance_status=AttendanceStatus.REGISTERED),
    ]
    db.session.add_all(enrollments)
    db.session.commit()

    # ── Attendance Records ─────────────────────────────────────────────
    attendance_records = [
        Attendance(enrollment_id=enrollments[0].id,
                   attendance_date=programs[0].start_date, present=True),
        Attendance(enrollment_id=enrollments[0].id,
                   attendance_date=programs[0].start_date + timedelta(days=1), present=True),
        Attendance(enrollment_id=enrollments[0].id,
                   attendance_date=programs[0].start_date + timedelta(days=2), present=True),

        Attendance(enrollment_id=enrollments[1].id,
                   attendance_date=programs[0].start_date, present=True),
        Attendance(enrollment_id=enrollments[1].id,
                   attendance_date=programs[0].start_date + timedelta(days=1), present=True),
        Attendance(enrollment_id=enrollments[1].id,
                   attendance_date=programs[0].start_date + timedelta(days=2), present=False),

        Attendance(enrollment_id=enrollments[3].id,
                   attendance_date=programs[0].start_date, present=True),
        Attendance(enrollment_id=enrollments[3].id,
                   attendance_date=programs[0].start_date + timedelta(days=1), present=False),
    ]
    db.session.add_all(attendance_records)
    db.session.commit()

    # ── Feedback (only for ATTENDED enrollments in completed programs) ─
    # enrollments[0] -> student charlie, program 0 (completed)
    # enrollments[1] -> student diana,   program 0 (completed)
    # enrollments[3] -> student frank,   program 0 (completed)
    # Program 0 has faculty_list[0] and faculty_list[1]

    feedbacks = [
        Feedback(enrollment_id=enrollments[0].id, faculty_id=faculty_list[0].id,
                 faculty_rating=5, curriculum_rating=4, program_structure_rating=5,
                 overall_rating=5, comments="Excellent instructor! Very engaging."),
        Feedback(enrollment_id=enrollments[0].id, faculty_id=faculty_list[1].id,
                 faculty_rating=4, curriculum_rating=4, program_structure_rating=4,
                 overall_rating=4, comments="Good content but could use more examples."),
        Feedback(enrollment_id=enrollments[1].id, faculty_id=faculty_list[0].id,
                 faculty_rating=4, curriculum_rating=3, program_structure_rating=4,
                 overall_rating=4, comments="Well structured. labs were helpful."),
        Feedback(enrollment_id=enrollments[1].id, faculty_id=faculty_list[1].id,
                 faculty_rating=3, curriculum_rating=3, program_structure_rating=3,
                 overall_rating=3, comments="Average experience. Needs improvement."),
        Feedback(enrollment_id=enrollments[3].id, faculty_id=faculty_list[0].id,
                 faculty_rating=5, curriculum_rating=5, program_structure_rating=5,
                 overall_rating=5, comments="Best training I've attended!"),
        Feedback(enrollment_id=enrollments[3].id, faculty_id=faculty_list[1].id,
                 faculty_rating=4, curriculum_rating=5, program_structure_rating=4,
                 overall_rating=4, comments="Great practical sessions."),
    ]
    db.session.add_all(feedbacks)
    db.session.commit()

    print("=" * 60)
    print("  Database seeded successfully!")
    print("=" * 60)
    print()
    print("  ── Login Credentials ──")
    print("  Password for all users: password123")
    print()
    print("  ADMIN:")
    print("    admin@test.com")
    print()
    print("  COORDINATORS:")
    print("    alice@test.com")
    print("    bob@test.com")
    print()
    print("  PARTICIPANTS:")
    print("    charlie@test.com  (enrolled in: Python, Web, Data Science)")
    print("    diana@test.com    (enrolled in: Python, Web)")
    print("    eve@test.com      (enrolled in: Python, Web)")
    print("    frank@test.com    (enrolled in: Python, Web)")
    print("    grace@test.com    (enrolled in: Python, Data Science)")
    print()
    print("  ── Seeded Counts ──")
    print(f"   Users:              {User.query.count()}")
    print(f"   Courses:            {Course.query.count()}")
    print(f"   Skills:             {Skill.query.count()}")
    print(f"   Faculty:            {Faculty.query.count()}")
    print(f"   Students:           {Student.query.count()}")
    print(f"   Training Programs:  {TrainingProgram.query.count()}")
    print(f"   Enrollments:        {Enrollment.query.count()}")
    print(f"   Attendance Records: {Attendance.query.count()}")
    print(f"   Feedbacks:          {Feedback.query.count()}")
    print()
