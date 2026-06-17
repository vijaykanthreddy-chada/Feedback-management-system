import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { Attendance as AttendanceService } from '../../services/attendance';
import { Navbar } from '../../components/navbar/navbar';

@Component({
  selector: 'app-attendance',
  standalone: true,
  imports: [CommonModule, FormsModule, Navbar],
  templateUrl: './attendance.html',
  styleUrl: './attendance.css',
})
export class Attendance {
  attendanceList: any[] = [];
  enrollments: any[] = [];

  students: any[] = [];
  selectedStudent = '';
  studentEnrollments: any[] = [];

  enrollment_id: number | null = null;
  attendance_date = '';
  present = true;

  message = '';
  errorMessage = '';

  constructor(private attendanceService: AttendanceService) {
    this.loadAttendance();
    this.loadEnrollments();
  }

  loadAttendance() {
    this.attendanceService.getAttendance().subscribe({
      next: (data: any[]) => {
        this.attendanceList = data;
      },
      error: () => {
        this.errorMessage = 'Failed to load attendance';
      }
    });
  }

  loadEnrollments() {
    this.attendanceService.getEnrollments().subscribe({
      next: (data: any[]) => {
        this.enrollments = data;
        this.prepareStudents();
      },
      error: () => {
        this.errorMessage = 'Failed to load enrollments';
      }
    });
  }

  prepareStudents() {
    const map = new Map();

    this.enrollments.forEach((enrollment) => {
      if (!map.has(enrollment.student)) {
        map.set(enrollment.student, enrollment.student);
      }
    });

    this.students = Array.from(map.values());
  }

  onStudentChange() {
    this.enrollment_id = null;
    this.attendance_date = '';

    this.studentEnrollments = this.enrollments.filter(
      enrollment => enrollment.student === this.selectedStudent
    );
  }

  markAttendance() {
    this.message = '';
    this.errorMessage = '';

    if (!this.selectedStudent || !this.enrollment_id || !this.attendance_date) {
      this.errorMessage = 'Student, enrolled program and attendance date are required';
      return;
    }

    const data = {
      enrollment_id: this.enrollment_id,
      attendance_date: this.attendance_date,
      present: this.present
    };

    this.attendanceService.markAttendance(data).subscribe({
      next: (response: any) => {
        this.message =
          `Attendance marked successfully. Status: ${response.attendance_status}`;

        this.selectedStudent = '';
        this.studentEnrollments = [];
        this.enrollment_id = null;
        this.attendance_date = '';
        this.present = true;

        this.loadAttendance();
      },
      error: (error) => {
        this.errorMessage =
          error.error?.error || 'Attendance marking failed';
      }
    });
  }
}