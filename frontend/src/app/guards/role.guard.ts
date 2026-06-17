import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

export const roleGuard: CanActivateFn = (route) => {
  const router = inject(Router);

  const userRole = localStorage.getItem('role');
  const allowedRoles = route.data?.['roles'] as string[];

  if (userRole && allowedRoles.includes(userRole)) {
    return true;
  }

  router.navigate(['/dashboard']);
  return false;
};