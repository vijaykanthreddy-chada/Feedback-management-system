import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { Feedback as FeedbackService } from '../../services/feedback';
import { Navbar } from '../../components/navbar/navbar';

@Component({
  selector: 'app-feedback',
  standalone: true,
  imports: [CommonModule, FormsModule, Navbar],
  templateUrl: './feedback.html',
  styleUrl: './feedback.css',
})
export class Feedback {
  myEnrollments: any[] = [];
  selectedEnrollment: any = null;

  enrollment_id: number | null = null;
  faculty_id: number | null = null;

  faculty_rating: number | null = null;
  curriculum_rating: number | null = null;
  program_structure_rating: number | null = null;
  overall_rating: number | null = null;

  comments = '';

  message = '';
  errorMessage = '';

  constructor(private feedbackService: FeedbackService) {
    this.loadMyEnrollments();
  }

  loadMyEnrollments() {
    this.feedbackService.getMyEnrollments().subscribe({
      next: (data) => {
        this.myEnrollments = data;
      },
      error: () => {
        this.errorMessage = 'Failed to load your enrollments';
      }
    });
  }

  onEnrollmentChange() {
    this.faculty_id = null;

    this.selectedEnrollment = this.myEnrollments.find(
      e => e.id == this.enrollment_id
    );
  }

  submitFeedback() {
    this.message = '';
    this.errorMessage = '';

    if (
      !this.enrollment_id ||
      !this.faculty_id ||
      !this.faculty_rating ||
      !this.curriculum_rating ||
      !this.program_structure_rating ||
      !this.overall_rating
    ) {
      this.errorMessage = 'Enrollment, faculty and all ratings are required';
      return;
    }

    const ratings = [
      this.faculty_rating,
      this.curriculum_rating,
      this.program_structure_rating,
      this.overall_rating
    ];

    for (let rating of ratings) {
      if (rating < 1 || rating > 5) {
        this.errorMessage = 'All ratings must be between 1 and 5';
        return;
      }
    }

    const data = {
      enrollment_id: this.enrollment_id,
      faculty_id: this.faculty_id,
      faculty_rating: this.faculty_rating,
      curriculum_rating: this.curriculum_rating,
      program_structure_rating: this.program_structure_rating,
      overall_rating: this.overall_rating,
      comments: this.comments
    };

    this.feedbackService.createFeedback(data).subscribe({
      next: () => {
        this.message = 'Feedback submitted successfully';

        this.enrollment_id = null;
        this.faculty_id = null;
        this.faculty_rating = null;
        this.curriculum_rating = null;
        this.program_structure_rating = null;
        this.overall_rating = null;
        this.comments = '';
        this.selectedEnrollment = null;
      },
      error: (error) => {
        this.errorMessage = error.error?.error || 'Feedback submission failed';
      }
    });
  }
}