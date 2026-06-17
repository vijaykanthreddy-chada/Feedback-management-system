import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { Program as ProgramService } from '../../services/program';
import { Navbar } from '../../components/navbar/navbar';

@Component({
  selector: 'app-programs',
  standalone: true,
  imports: [CommonModule, FormsModule, Navbar],
  templateUrl: './programs.html',
  styleUrl: './programs.css',
})
export class Programs {
  programs: any[] = [];
  courses: any[] = [];
  coordinators: any[] = [];
  faculties: any[] = [];

  course_id: number | null = null;
  coordinator_id: number | null = null;
  start_date = '';
  end_date = '';
  location = '';
  capacity: number | null = null;

  editingProgramId: number | null = null;

  program_id: number | null = null;
  faculty_id: number | null = null;

  message = '';
  errorMessage = '';

  constructor(private programService: ProgramService) {
    this.loadPrograms();
    this.loadCourses();
    this.loadCoordinators();
    this.loadFaculties();
  }

  loadPrograms() {
    this.programService.getPrograms().subscribe({
      next: (data: any[]) => {
        this.programs = data;
      },
      error: () => {
        this.errorMessage = 'Failed to load programs';
      }
    });
  }

  loadCourses() {
    this.programService.getCourses().subscribe({
      next: (data: any[]) => {
        this.courses = data;
      },
      error: () => {
        this.errorMessage = 'Failed to load courses';
      }
    });
  }

  loadCoordinators() {
    this.programService.getCoordinators().subscribe({
      next: (data: any[]) => {
        this.coordinators = data;
      },
      error: () => {
        this.errorMessage = 'Failed to load coordinators';
      }
    });
  }

  loadFaculties() {
    this.programService.getFaculties().subscribe({
      next: (data: any[]) => {
        this.faculties = data;
      },
      error: () => {
        this.errorMessage = 'Failed to load faculties';
      }
    });
  }

  addProgram() {
    this.message = '';
    this.errorMessage = '';

    if (
      !this.course_id ||
      !this.coordinator_id ||
      !this.start_date ||
      !this.end_date ||
      !this.location ||
      !this.capacity
    ) {
      this.errorMessage = 'All program fields are required';
      return;
    }

    if (this.capacity > 70) {
      this.errorMessage = 'Capacity is 70 only for training';
      return;
    }

    const data = {
      course_id: this.course_id,
      coordinator_id: this.coordinator_id,
      start_date: this.start_date,
      end_date: this.end_date,
      location: this.location,
      capacity: this.capacity
    };

    this.programService.createProgram(data).subscribe({
      next: () => {
        this.message = 'Program created successfully';
        this.clearProgramForm();
        this.loadPrograms();
      },
      error: (error) => {
        this.errorMessage = error.error?.error || 'Program creation failed';
      }
    });
  }

  editProgram(program: any) {
    this.editingProgramId = program.id;

    this.course_id = program.course_id;
    this.coordinator_id = program.coordinator_id;
    this.start_date = program.start_date;
    this.end_date = program.end_date;
    this.location = program.location;
    this.capacity = program.capacity;
  }

  updateProgram() {
    this.message = '';
    this.errorMessage = '';

    if (!this.editingProgramId) {
      return;
    }

    if (
      !this.course_id ||
      !this.coordinator_id ||
      !this.start_date ||
      !this.end_date ||
      !this.location ||
      !this.capacity
    ) {
      this.errorMessage = 'All program fields are required';
      return;
    }

    if (this.capacity > 70) {
      this.errorMessage = 'Capacity is 70 only for training';
      return;
    }

    const data = {
      course_id: this.course_id,
      coordinator_id: this.coordinator_id,
      start_date: this.start_date,
      end_date: this.end_date,
      location: this.location,
      capacity: this.capacity
    };

    this.programService.updateProgram(this.editingProgramId, data).subscribe({
      next: () => {
        this.message = 'Program updated successfully';
        this.clearProgramForm();
        this.loadPrograms();
      },
      error: (error) => {
        this.errorMessage = error.error?.error || 'Program update failed';
      }
    });
  }

  cancelProgram(programId: number) {
    this.message = '';
    this.errorMessage = '';

    if (!confirm('Are you sure you want to cancel this program?')) {
      return;
    }

    this.programService.cancelProgram(programId).subscribe({
      next: () => {
        this.message = 'Program cancelled successfully';
        this.loadPrograms();
      },
      error: (error) => {
        this.errorMessage = error.error?.error || 'Program cancellation failed';
      }
    });
  }

  deleteProgram(programId: number) {
    this.message = '';
    this.errorMessage = '';

    if (!confirm('Are you sure you want to delete this program?')) {
      return;
    }

    this.programService.deleteProgram(programId).subscribe({
      next: () => {
        this.message = 'Program deleted successfully';
        this.loadPrograms();
      },
      error: (error) => {
        this.errorMessage = error.error?.error || 'Program delete failed';
      }
    });
  }

  getProgramStatus(program: any): string {
    if (program.status === 'CANCELLED') {
      return 'CANCELLED';
    }

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const start = new Date(program.start_date);
    const end = new Date(program.end_date);

    if (end < today) {
      return 'COMPLETED';
    }

    if (start <= today && end >= today) {
      return 'ONGOING';
    }

    return 'SCHEDULED';
  }

  cancelEdit() {
    this.clearProgramForm();
  }

  clearProgramForm() {
    this.course_id = null;
    this.coordinator_id = null;
    this.start_date = '';
    this.end_date = '';
    this.location = '';
    this.capacity = null;
    this.editingProgramId = null;
  }

  assignFaculty() {
    this.message = '';
    this.errorMessage = '';

    if (!this.program_id || !this.faculty_id) {
      this.errorMessage = 'Program and Faculty are required';
      return;
    }

    this.programService.assignFaculty(
      this.program_id,
      this.faculty_id
    ).subscribe({
      next: () => {
        this.message = 'Faculty assigned successfully';
        this.program_id = null;
        this.faculty_id = null;
      },
      error: (error) => {
        this.errorMessage = error.error?.error || 'Faculty assignment failed';
      }
    });
  }
}