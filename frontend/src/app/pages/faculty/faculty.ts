import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { Faculty as FacultyService } from '../../services/faculty';
import { Navbar } from '../../components/navbar/navbar';

@Component({
  selector: 'app-faculty',
  standalone: true,
  imports: [CommonModule, FormsModule, Navbar],
  templateUrl: './faculty.html',
  styleUrl: './faculty.css',
})
export class Faculty {
  faculties: any[] = [];
  skills: any[] = [];

  name = '';
  email = '';

  editingFacultyId: number | null = null;

  skillName = '';
  facultyId: number | null = null;
  skillId: number | null = null;

  searchSkill = '';

  message = '';
  errorMessage = '';

  constructor(private facultyService: FacultyService) {
    this.loadFaculties();
    this.loadSkills();
  }

  loadFaculties() {
    this.facultyService.getFaculties().subscribe({
      next: (data: any[]) => {
        this.faculties = data;
      },
      error: () => {
        this.errorMessage = 'Failed to load faculties';
      }
    });
  }

  loadSkills() {
    this.facultyService.getSkills().subscribe({
      next: (data: any[]) => {
        this.skills = data;
      },
      error: () => {
        this.errorMessage = 'Failed to load skills';
      }
    });
  }

  addFaculty() {
    this.message = '';
    this.errorMessage = '';

    if (!this.name || !this.email) {
      this.errorMessage = 'Faculty name and email are required';
      return;
    }

    this.facultyService.createFaculty({
      name: this.name,
      email: this.email
    }).subscribe({
      next: () => {
        this.message = 'Faculty created successfully';
        this.clearFacultyForm();
        this.loadFaculties();
      },
      error: (error) => {
        this.errorMessage = error.error?.error || 'Faculty creation failed';
      }
    });
  }

  editFaculty(faculty: any) {
    this.editingFacultyId = faculty.id;
    this.name = faculty.name;
    this.email = faculty.email;
  }

  updateFaculty() {
    this.message = '';
    this.errorMessage = '';

    if (!this.editingFacultyId) {
      return;
    }

    if (!this.name || !this.email) {
      this.errorMessage = 'Faculty name and email are required';
      return;
    }

    this.facultyService.updateFaculty(
      this.editingFacultyId,
      {
        name: this.name,
        email: this.email
      }
    ).subscribe({
      next: () => {
        this.message = 'Faculty updated successfully';
        this.clearFacultyForm();
        this.loadFaculties();
      },
      error: (error) => {
        this.errorMessage = error.error?.error || 'Faculty update failed';
      }
    });
  }

  deleteFaculty(id: number) {
    this.message = '';
    this.errorMessage = '';

    if (!confirm('Are you sure you want to delete this faculty?')) {
      return;
    }

    this.facultyService.deleteFaculty(id).subscribe({
      next: () => {
        this.message = 'Faculty deleted successfully';
        this.loadFaculties();
      },
      error: (error) => {
        this.errorMessage = error.error?.error || 'Faculty delete failed';
      }
    });
  }

  cancelEdit() {
    this.clearFacultyForm();
  }

  clearFacultyForm() {
    this.name = '';
    this.email = '';
    this.editingFacultyId = null;
  }

  addSkill() {
    this.message = '';
    this.errorMessage = '';

    if (!this.skillName) {
      this.errorMessage = 'Skill name is required';
      return;
    }

    this.facultyService.createSkill({
      name: this.skillName
    }).subscribe({
      next: () => {
        this.message = 'Skill created successfully';
        this.skillName = '';
        this.loadSkills();
      },
      error: (error) => {
        this.errorMessage = error.error?.error || 'Skill creation failed';
      }
    });
  }

  assignSkill() {
    this.message = '';
    this.errorMessage = '';

    if (!this.facultyId || !this.skillId) {
      this.errorMessage = 'Faculty and Skill are required';
      return;
    }

    this.facultyService.assignSkill(
      this.facultyId,
      this.skillId
    ).subscribe({
      next: () => {
        this.message = 'Skill assigned successfully';
        this.facultyId = null;
        this.skillId = null;
        this.loadFaculties();
      },
      error: (error) => {
        this.errorMessage = error.error?.error || 'Skill assignment failed';
      }
    });
  }

  searchFaculty() {
    this.message = '';
    this.errorMessage = '';

    if (!this.searchSkill) {
      this.loadFaculties();
      return;
    }

    this.facultyService.searchBySkill(this.searchSkill).subscribe({
      next: (data: any[]) => {
        this.faculties = data;
      },
      error: () => {
        this.errorMessage = 'Faculty search failed';
      }
    });
  }
}