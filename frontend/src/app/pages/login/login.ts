import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

import { Auth } from '../../services/auth';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  email = '';
  password = '';
  role = 'ADMIN';

  registerName = '';
  registerEmail = '';
  registerPassword = '';
  registerRole = 'PARTICIPANT';

  errorMessage = '';
  successMessage = '';
  showRegister = false;

  constructor(
    private auth: Auth,
    private router: Router
  ) {}

  loginUser() {
    this.errorMessage = '';
    this.successMessage = '';

    this.auth.login({
      email: this.email,
      password: this.password
    }).subscribe({
      next: (response) => {
        this.auth.saveLoginData(response);

        const actualRole = response.user.role;

        if (actualRole !== this.role) {
          this.errorMessage = `You selected ${this.role}, but this account is ${actualRole}`;
          return;
        }

        if (actualRole === 'ADMIN') {
          this.router.navigate(['/dashboard']);
        } else if (actualRole === 'COORDINATOR') {
          this.router.navigate(['/programs']);
        } else {
          this.router.navigate(['/feedback']);
        }
      },
      error: (error) => {
        this.errorMessage = error.error?.error || 'Login failed';
      }
    });
  }

  registerUser() {
    this.errorMessage = '';
    this.successMessage = '';

    this.auth.register({
      name: this.registerName,
      email: this.registerEmail,
      password: this.registerPassword,
      role: this.registerRole
    }).subscribe({
      next: () => {
        this.successMessage = 'User registered successfully. Now login.';
        this.showRegister = false;

        this.email = this.registerEmail;
        this.password = '';
        this.role = this.registerRole;
      },
      error: (error) => {
        this.errorMessage = error.error?.error || 'Registration failed';
      }
    });
  }
}