import { HttpClient } from '@angular/common/http';
import { Injectable, inject, signal } from '@angular/core';
import { Observable, tap } from 'rxjs';

const API = 'http://localhost:8000/api';

interface TokenPair {
  access: string;
  refresh: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);

  isAuthenticated = signal<boolean>(!!localStorage.getItem('access'));

  login(username: string, password: string): Observable<TokenPair> {
    return this.http
      .post<TokenPair>(`${API}/token/`, { username, password })
      .pipe(
        tap(tokens => {
          localStorage.setItem('access', tokens.access);
          localStorage.setItem('refresh', tokens.refresh);
          this.isAuthenticated.set(true);
        }),
      );
  }

  register(username: string, password: string): Observable<{ id: number; username: string }> {
    return this.http.post<{ id: number; username: string }>(`${API}/register/`, {
      username,
      password,
    });
  }

  logout(): void {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    this.isAuthenticated.set(false);
  }
}
