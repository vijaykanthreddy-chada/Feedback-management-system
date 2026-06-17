import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { Course } from '../../services/course';
import { Navbar } from '../../components/navbar/navbar';

@Component({
  selector: 'app-courses',
  standalone: true,
  imports: [CommonModule, FormsModule, Navbar],
  templateUrl: './courses.html',
  styleUrl: './courses.css',
})
export class Courses {
  courses: any[] = [];

  code = '';
  title = '';
  description = '';
  duration_days: number | null = null;

  editingCourseId: number | null = null;

  message = '';
  errorMessage = '';

  constructor(private courseService: Course) {
    this.loadCourses();
  }

  loadCourses() {
    this.courseService.getCourses().subscribe({
      next: (data: any[]) => {
        this.courses = data;
      },
      error: () => {
        this.errorMessage = 'Failed to load courses';
      }
    });
  }

  addCourse() {
    this.message = '';
    this.errorMessage = '';

    if (this.duration_days && this.duration_days > 150) {
      this.errorMessage = 'Duration cannot exceed 150 days';
      return;
    }

    const data = {
      code: this.code,
      title: this.title,
      description: this.description,
      duration_days: this.duration_days
    };

    this.courseService.createCourse(data).subscribe({
      next: () => {
        this.message = 'Course created successfully';
        this.clearForm();
        this.loadCourses();
      },
      error: (error) => {
        this.errorMessage = error.error?.error || 'Course creation failed';
      }
    });
  }

  editCourse(course: any) {
    this.editingCourseId = course.id;

    this.code = course.code;
    this.title = course.title;
    this.description = course.description;
    this.duration_days = course.duration_days;
  }

  updateCourse() {
    this.message = '';
    this.errorMessage = '';

    if (!this.editingCourseId) {
      return;
    }

    if (this.duration_days && this.duration_days > 150) {
      this.errorMessage = 'Duration cannot exceed 150 days';
      return;
    }

    const data = {
      title: this.title,
      description: this.description,
      duration_days: this.duration_days
    };

    this.courseService.updateCourse(this.editingCourseId, data).subscribe({
      next: () => {
        this.message = 'Course updated successfully';
        this.clearForm();
        this.loadCourses();
      },
      error: (error) => {
        this.errorMessage = error.error?.error || 'Course update failed';
      }
    });
  }

  deleteCourse(id: number) {
    this.message = '';
    this.errorMessage = '';

    if (!confirm('Are you sure you want to delete this course?')) {
      return;
    }

    this.courseService.deleteCourse(id).subscribe({
      next: () => {
        this.message = 'Course deleted successfully';
        this.loadCourses();
      },
      error: (error) => {
        this.errorMessage = error.error?.error || 'Course delete failed';
      }
    });
  }

  cancelEdit() {
    this.clearForm();
  }

  clearForm() {
    this.code = '';
    this.title = '';
    this.description = '';
    this.duration_days = null;
    this.editingCourseId = null;
  }
}