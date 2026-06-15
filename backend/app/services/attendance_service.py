from datetime import datetime

from app.config.database import db
from app.models.attendance import Attendance
from app.models.enrollment import Enrollment, AttendanceStatus


def mark_attendance(data):
    enrollment_id = data.get("enrollment_id")
    attendance_date = data.get("attendance_date")
    present = data.get("present", True)

    enrollment = Enrollment.query.get(enrollment_id)

    if not enrollment:
        return {"error": "Enrollment not found"}, 404

    attendance = Attendance(
        enrollment_id=enrollment_id,
        attendance_date=datetime.strptime(
            attendance_date,
            "%Y-%m-%d"
        ).date(),
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
        result.append({
            "id": attendance.id,
            "enrollment_id": attendance.enrollment_id,
            "attendance_date": str(attendance.attendance_date),
            "present": attendance.present,
            "attendance_status": attendance.enrollment.attendance_status.value
        })

    return result