from datetime import datetime

from app.config.database import db
from app.models.attendance import Attendance
from app.models.enrollment import Enrollment, AttendanceStatus


def mark_attendance(data):
    enrollment_id = data.get("enrollment_id")
    attendance_date = data.get("attendance_date")
    present = data.get("present", True)

    if not enrollment_id or not attendance_date:
        return {
            "error": "Enrollment and attendance date are required"
        }, 400

    enrollment = Enrollment.query.get(enrollment_id)

    if not enrollment:
        return {"error": "Enrollment not found"}, 404

    try:
        selected_date = datetime.strptime(
            attendance_date,
            "%Y-%m-%d"
        ).date()
    except ValueError:
        return {
            "error": "Date format must be YYYY-MM-DD"
        }, 400

    program = enrollment.program

    if selected_date < program.start_date or selected_date > program.end_date:
        return {
            "error": "Select date between program start date and end date"
        }, 400

    attendance = Attendance(
        enrollment_id=enrollment_id,
        attendance_date=selected_date,
        present=present
    )

    if present:
        enrollment.attendance_status = AttendanceStatus.ATTENDED
    else:
        enrollment.attendance_status = AttendanceStatus.NO_SHOW

    db.session.add(attendance)
    db.session.commit()

    return {
        "message": "Attendance marked successfully",
        "attendance_id": attendance.id,
        "attendance_status": enrollment.attendance_status.value
    }, 201


def get_all_attendance():
    attendance_list = Attendance.query.all()

    result = []

    for attendance in attendance_list:
        enrollment = attendance.enrollment
        program = enrollment.program

        result.append({
            "id": attendance.id,
            "enrollment_id": attendance.enrollment_id,
            "student": enrollment.student.name,
            "program_id": program.id,
            "program_name": program.course.title,
            "attendance_date": str(attendance.attendance_date),
            "present": attendance.present,
            "attendance_status": enrollment.attendance_status.value
        })

    return result