import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';

import { Auth } from '../../services/auth';
import { Navbar } from '../../components/navbar/navbar';
import { Report } from '../../services/report';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    RouterLink,
    Navbar
  ],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css'
})
export class Dashboard {

  role: string | null = '';
  user: any = null;
  summary: any = null;

  constructor(
    private auth: Auth,
    private router: Router,
    private reportService: Report
  ) {
    this.role = this.auth.getRole();
    this.user = JSON.parse(
      localStorage.getItem('user') || '{}'
    );

    this.loadSummary();
  }

  loadSummary() {
    this.reportService.getDashboardSummary().subscribe({
      next: (data) => {
        this.summary = data;
      },
      error: () => {
        console.log('Failed to load dashboard summary');
      }
    });
  }

  logout() {
    this.auth.logout();
    this.router.navigate(['/']);
  }

}