import { HttpErrorResponse } from '@angular/common/http';
import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';

import { AuthService } from '../../services/auth';
import { extractErrors } from '../../utils/errors';

@Component({
  selector: 'app-register',
  imports: [FormsModule, RouterLink],
  templateUrl: './register.html',
  styleUrl: './register.css',
})
export class Register {
  private auth = inject(AuthService);
  private router = inject(Router);

  username = '';
  password = '';
  errors = signal<Record<string, string>>({});
  submitting = signal<boolean>(false);

  submit(): void {
    if (!this.username || this.password.length < 6) {
      this.errors.set({ detail: 'Username required, password min 6 chars.' });
      return;
    }
    this.submitting.set(true);
    this.errors.set({});
    this.auth.register(this.username, this.password).subscribe({
      next: () => {
        this.auth.login(this.username, this.password).subscribe({
          next: () => {
            this.submitting.set(false);
            this.router.navigate(['/']);
          },
          error: () => {
            this.submitting.set(false);
            this.router.navigate(['/login']);
          },
        });
      },
      error: (err: HttpErrorResponse) => {
        this.errors.set(extractErrors(err));
        this.submitting.set(false);
      },
    });
  }
}
