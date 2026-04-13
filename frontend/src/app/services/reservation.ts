import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { Booking, Paginated } from '../models/cafe';

const API = 'http://localhost:8000/api';

interface NewBooking {
  cafe: number;
  date: string;
  time: string;
  guests: number;
}

@Injectable({ providedIn: 'root' })
export class ReservationService {
  private http = inject(HttpClient);

  list(): Observable<Booking[]> {
    return this.http
      .get<Paginated<Booking>>(`${API}/reservations/`)
      .pipe(map(res => res.results));
  }

  create(data: NewBooking): Observable<Booking> {
    return this.http.post<Booking>(`${API}/reservations/`, data);
  }

  remove(id: number): Observable<void> {
    return this.http.delete<void>(`${API}/reservations/${id}/`);
  }
}
