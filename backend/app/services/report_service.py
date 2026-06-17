import csv
from io import StringIO

from flask import Response

from app.models.course import Course
from app.models.faculty import Faculty
from app.models.student import Student
from app.models.training_program import TrainingProgram
from app.models.enrollment import Enrollment, AttendanceStatus
from app.models.attendance import Attendance
from app.models.feedback import Feedback


def dashboard_summary():
    return {
        "total_courses": Course.query.count(),
        "total_faculties": Faculty.query.count(),
        "total_students": Student.query.count(),
        "total_programs": TrainingProgram.query.count(),
        "total_enrollments": Enrollment.query.count(),
        "total_feedbacks": Feedback.query.count()
    }


def program_feedback_summary(program_id):
    program = TrainingProgram.query.get(program_id)

    if not program:
        return {"error": "Program not found"}, 404

    enrollments = Enrollment.query.filter_by(program_id=program_id).all()
    enrollment_ids = [e.id for e in enrollments]

    feedbacks = Feedback.query.filter(
        Feedback.enrollment_id.in_(enrollment_ids)
    ).all() if enrollment_ids else []

    total_feedbacks = len(feedbacks)

    average_rating = 0
    if total_feedbacks > 0:
        average_rating = round(
            sum(f.overall_rating for f in feedbacks) / total_feedbacks,
            2
        )

    comments = [
        f.comments for f in feedbacks if f.comments
    ]

    return {
        "program_id": program.id,
        "course": program.course.title,
        "total_feedbacks": total_feedbacks,
        "average_rating": average_rating,
        "comments": comments
    }, 200


def program_feedback_summary_csv(program_id):
    data, status = program_feedback_summary(program_id)

    if status != 200:
        return data, status

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Program ID",
        "Course",
        "Total Feedbacks",
        "Average Rating"
    ])

    writer.writerow([
        data["program_id"],
        data["course"],
        data["total_feedbacks"],
        data["average_rating"]
    ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment;filename=program_feedback_summary.csv"
        }
    )


def defaulters_report(program_id):
    program = TrainingProgram.query.get(program_id)

    if not program:
        return {"error": "Program not found"}, 404

    attended_enrollments = Enrollment.query.filter_by(
        program_id=program_id,
        attendance_status=AttendanceStatus.ATTENDED
    ).all()

    defaulters = []

    for enrollment in attended_enrollments:
        feedback = Feedback.query.filter_by(
            enrollment_id=enrollment.id
        ).first()

        if not feedback:
            defaulters.append({
                "student_id": enrollment.student.id,
                "student_name": enrollment.student.name,
                "email": enrollment.student.email
            })

    return {
        "program_id": program.id,
        "course": program.course.title,
        "defaulters_count": len(defaulters),
        "defaulters": defaulters
    }, 200


def program_enrollment_report(program_id):
    program = TrainingProgram.query.get(program_id)

    if not program:
        return {"error": "Program not found"}, 404

    total = Enrollment.query.filter_by(program_id=program_id).count()

    return {
        "program_id": program.id,
        "course": program.course.title,
        "location": program.location,
        "total_enrollments": total
    }, 200


def program_attendance_report(program_id):
    program = TrainingProgram.query.get(program_id)

    if not program:
        return {"error": "Program not found"}, 404

    enrollments = Enrollment.query.filter_by(program_id=program_id).all()
    enrollment_ids = [e.id for e in enrollments]

    total_enrollments = len(enrollment_ids)

    present_count = Attendance.query.filter(
        Attendance.enrollment_id.in_(enrollment_ids),
        Attendance.present == True
    ).count() if enrollment_ids else 0

    percentage = 0
    if total_enrollments > 0:
        percentage = round((present_count / total_enrollments) * 100, 2)

    return {
        "program_id": program.id,
        "course": program.course.title,
        "total_enrollments": total_enrollments,
        "present_count": present_count,
        "attendance_percentage": percentage
    }, 200


def faculty_performance_report(faculty_id):
    faculty = Faculty.query.get(faculty_id)

    if not faculty:
        return {"error": "Faculty not found"}, 404

    feedbacks = Feedback.query.filter_by(faculty_id=faculty_id).all()

    total_feedbacks = len(feedbacks)

    average_rating = 0
    if total_feedbacks > 0:
        average_rating = round(
            sum(f.overall_rating for f in feedbacks) / total_feedbacks,
            2
        )

    return {
        "faculty_id": faculty.id,
        "faculty_name": faculty.name,
        "total_feedbacks": total_feedbacks,
        "average_rating": average_rating
    }, 200