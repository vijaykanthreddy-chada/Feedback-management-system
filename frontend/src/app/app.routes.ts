import { Routes } from '@angular/router';

import { Login } from './pages/login/login';
import { Dashboard } from './pages/dashboard/dashboard';
import { Courses } from './pages/courses/courses';
import { Faculty } from './pages/faculty/faculty';
import { Students } from './pages/students/students';
import { Programs } from './pages/programs/programs';
import { Enrollments } from './pages/enrollments/enrollments';
import { Attendance } from './pages/attendance/attendance';
import { Feedback } from './pages/feedback/feedback';
import { Reports } from './pages/reports/reports';

import { authGuard } from './guards/auth.guard';
import { roleGuard } from './guards/role.guard';

export const routes: Routes = [
  { path: '', component: Login },

  {
    path: 'dashboard',
    component: Dashboard,
    canActivate: [authGuard]
  },

  {
    path: 'courses',
    component: Courses,
    canActivate: [authGuard, roleGuard],
    data: { roles: ['ADMIN'] }
  },

  {
    path: 'faculty',
    component: Faculty,
    canActivate: [authGuard, roleGuard],
    data: { roles: ['ADMIN'] }
  },

  {
    path: 'students',
    component: Students,
    canActivate: [authGuard, roleGuard],
    data: { roles: ['ADMIN'] }
  },

  {
    path: 'programs',
    component: Programs,
    canActivate: [authGuard, roleGuard],
    data: { roles: ['ADMIN', 'COORDINATOR'] }
  },

  {
    path: 'enrollments',
    component: Enrollments,
    canActivate: [authGuard, roleGuard],
    data: { roles: ['ADMIN', 'COORDINATOR'] }
  },

  {
    path: 'attendance',
    component: Attendance,
    canActivate: [authGuard, roleGuard],
    data: { roles: ['COORDINATOR'] }
  },

  {
    path: 'feedback',
    component: Feedback,
    canActivate: [authGuard, roleGuard],
    data: { roles: ['PARTICIPANT'] }
  },

  {
    path: 'reports',
    component: Reports,
    canActivate: [authGuard, roleGuard],
    data: { roles: ['ADMIN', 'COORDINATOR'] }
  },

  { path: '**', redirectTo: '' }
];