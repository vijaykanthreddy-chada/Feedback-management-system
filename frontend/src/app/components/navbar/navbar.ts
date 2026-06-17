import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';

import { Auth } from '../../services/auth';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  templateUrl: './navbar.html',
  styleUrl: './navbar.css',
})
export class Navbar {
  role = localStorage.getItem('role');

  constructor(
    private auth: Auth,
    private router: Router
  ) {}

  logout() {
    this.auth.logout();
    this.router.navigate(['/']);
  }
}