import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { Enrollment as EnrollmentService } from '../../services/enrollment';
import { Navbar } from '../../components/navbar/navbar';

@Component({
  selector: 'app-enrollments',
  standalone: true,
  imports: [CommonModule, FormsModule, Navbar],
  templateUrl: './enrollments.html',
  styleUrl: './enrollments.css',
})
export class Enrollments {
  enrollments: any[] = [];
  students: any[] = [];
  programs: any[] = [];

  student_id: number | null = null;
  program_id: number | null = null;

  message = '';
  errorMessage = '';

  constructor(private enrollmentService: EnrollmentService) {
    this.loadEnrollments();
    this.loadStudents();
    this.loadPrograms();
  }

  loadEnrollments() {
    this.enrollmentService.getEnrollments().subscribe({
      next: (data: any[]) => {
        this.enrollments = data;
      },
      error: () => {
        this.errorMessage = 'Failed to load enrollments';
      }
    });
  }

  loadStudents() {
    this.enrollmentService.getStudents().subscribe({
      next: (data: any[]) => {
        this.students = data;
      },
      error: () => {
        this.errorMessage = 'Failed to load students';
      }
    });
  }

  loadPrograms() {
    this.enrollmentService.getPrograms().subscribe({
      next: (data: any[]) => {
        this.programs = data;
      },
      error: () => {
        this.errorMessage = 'Failed to load programs';
      }
    });
  }

  enrollStudent() {
    this.message = '';
    this.errorMessage = '';

    if (!this.student_id || !this.program_id) {
      this.errorMessage = 'Student and Program are required';
      return;
    }

    const data = {
      student_id: this.student_id,
      program_id: this.program_id
    };

    this.enrollmentService.createEnrollment(data).subscribe({
      next: (response: any) => {
        this.message =
          `Student enrolled successfully. Enrollment ID: ${response.enrollment_id}`;

        this.student_id = null;
        this.program_id = null;

        this.loadEnrollments();
      },
      error: (error) => {
        this.errorMessage =
          error.error?.error || 'Enrollment failed';
      }
    });
  }

  deleteEnrollment(id: number) {
    this.message = '';
    this.errorMessage = '';

    if (!confirm('Are you sure you want to delete this enrollment?')) {
      return;
    }

    this.enrollmentService.deleteEnrollment(id).subscribe({
      next: () => {
        this.message = 'Enrollment deleted successfully';
        this.loadEnrollments();
      },
      error: (error) => {
        this.errorMessage =
          error.error?.error || 'Enrollment delete failed';
      }
    });
  }
}