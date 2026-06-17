import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { Student as StudentService } from '../../services/student';
import { Navbar } from '../../components/navbar/navbar';

@Component({
  selector: 'app-students',
  standalone: true,
  imports: [CommonModule, FormsModule, Navbar],
  templateUrl: './students.html',
  styleUrl: './students.css',
})
export class Students {
  students: any[] = [];
  courses: any[] = [];
  participants: any[] = [];

  email = '';
  course_id: number | null = null;

  editingStudentId: number | null = null;

  message = '';
  errorMessage = '';

  constructor(private studentService: StudentService) {
    this.loadStudents();
    this.loadCourses();
    this.loadParticipants();
  }

  loadStudents() {
    this.studentService.getStudents().subscribe({
      next: (data: any[]) => {
        this.students = data;
      },
      error: () => {
        this.errorMessage = 'Failed to load students';
      }
    });
  }

  loadCourses() {
    this.studentService.getCourses().subscribe({
      next: (data: any[]) => {
        this.courses = data;
      },
      error: () => {
        this.errorMessage = 'Failed to load courses';
      }
    });
  }

  loadParticipants() {
    this.studentService.getParticipants().subscribe({
      next: (data: any[]) => {
        this.participants = data;
      },
      error: () => {
        this.errorMessage = 'Failed to load participants';
      }
    });
  }

  addStudent() {
    this.message = '';
    this.errorMessage = '';

    if (!this.email || !this.course_id) {
      this.errorMessage = 'Participant and Course are required';
      return;
    }

    const data = {
      email: this.email,
      course_id: this.course_id
    };

    this.studentService.createStudent(data).subscribe({
      next: () => {
        this.message = 'Student created successfully';
        this.clearForm();
        this.loadStudents();
      },
      error: (error) => {
        this.errorMessage = error.error?.error || 'Student creation failed';
      }
    });
  }

  editStudent(student: any) {
    this.editingStudentId = student.id;
    this.email = student.email;
    this.course_id = student.course_id;
  }

  updateStudent() {
    this.message = '';
    this.errorMessage = '';

    if (!this.editingStudentId) {
      return;
    }

    if (!this.course_id) {
      this.errorMessage = 'Course is required';
      return;
    }

    this.studentService.updateStudent(
      this.editingStudentId,
      {
        course_id: this.course_id
      }
    ).subscribe({
      next: () => {
        this.message = 'Student updated successfully';
        this.clearForm();
        this.loadStudents();
      },
      error: (error) => {
        this.errorMessage = error.error?.error || 'Student update failed';
      }
    });
  }

  deleteStudent(id: number) {
    this.message = '';
    this.errorMessage = '';

    if (!confirm('Are you sure you want to delete this student?')) {
      return;
    }

    this.studentService.deleteStudent(id).subscribe({
      next: () => {
        this.message = 'Student deleted successfully';
        this.loadStudents();
      },
      error: (error) => {
        this.errorMessage = error.error?.error || 'Student delete failed';
      }
    });
  }

  cancelEdit() {
    this.clearForm();
  }

  clearForm() {
    this.email = '';
    this.course_id = null;
    this.editingStudentId = null;
  }
}