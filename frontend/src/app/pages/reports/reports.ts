import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { Report as ReportService } from '../../services/report';
import { Navbar } from '../../components/navbar/navbar';

@Component({
  selector: 'app-reports',
  standalone: true,
  imports: [CommonModule, FormsModule, Navbar],
  templateUrl: './reports.html',
  styleUrl: './reports.css',
})
export class Reports {
  summary: any = null;

  programId: number | null = null;
  facultyId: number | null = null;

  enrollmentReport: any = null;
  attendanceReport: any = null;
  facultyReport: any = null;
  programSummary: any = null;
  defaultersReport: any = null;

  errorMessage = '';

  constructor(private reportService: ReportService) {
    this.loadDashboardSummary();
  }

  loadDashboardSummary() {
    this.reportService.getDashboardSummary().subscribe({
      next: (data) => {
        this.summary = data;
      },
      error: () => {
        this.errorMessage = 'Failed to load dashboard summary';
      }
    });
  }

  clearProgramReports() {
    this.enrollmentReport = null;
    this.attendanceReport = null;
    this.programSummary = null;
    this.defaultersReport = null;
  }

  loadProgramReports() {
    this.errorMessage = '';
    this.clearProgramReports();

    if (!this.programId) {
      this.errorMessage = 'Program ID is required';
      return;
    }

    this.reportService.getEnrollmentReport(this.programId).subscribe({
      next: (data) => {
        this.enrollmentReport = data;

        this.loadAttendanceReport();
        this.loadProgramSummary();
        this.loadDefaultersReport();
      },
      error: (error) => {
        this.clearProgramReports();
        this.errorMessage =
          error.error?.error || 'Program not found';
      }
    });
  }

  loadAttendanceReport() {
    if (!this.programId) return;

    this.reportService.getAttendanceReport(this.programId).subscribe({
      next: (data) => {
        this.attendanceReport = data;
      },
      error: (error) => {
        this.errorMessage =
          error.error?.error || 'Failed to load attendance report';
      }
    });
  }

  loadProgramSummary() {
    if (!this.programId) return;

    this.reportService.getProgramSummary(this.programId).subscribe({
      next: (data) => {
        this.programSummary = data;
      },
      error: (error) => {
        this.errorMessage =
          error.error?.error || 'Failed to load feedback summary';
      }
    });
  }

  loadDefaultersReport() {
    if (!this.programId) return;

    this.reportService.getDefaulters(this.programId).subscribe({
      next: (data) => {
        this.defaultersReport = data;
      },
      error: (error) => {
        this.errorMessage =
          error.error?.error || 'Failed to load defaulters report';
      }
    });
  }

  loadFacultyReport() {
    this.errorMessage = '';
    this.facultyReport = null;

    if (!this.facultyId) {
      this.errorMessage = 'Faculty ID is required';
      return;
    }

    this.reportService.getFacultyPerformance(this.facultyId).subscribe({
      next: (data) => {
        this.facultyReport = data;
      },
      error: (error) => {
        this.errorMessage =
          error.error?.error || 'Faculty not found';
      }
    });
  }

  downloadCsv() {
    this.errorMessage = '';

    if (!this.programId) {
      this.errorMessage = 'Program ID is required';
      return;
    }

    this.reportService.downloadCsv(this.programId).subscribe({
      next: (blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');

        a.href = url;
        a.download = 'program_feedback_summary.csv';
        a.click();

        window.URL.revokeObjectURL(url);
      },
      error: (error) => {
        this.errorMessage =
          error.error?.error || 'Program not found or CSV download failed';
      }
    });
  }
}