import { Component, OnInit, inject, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

import { AuthService } from '../../services/auth';
import { ReservationService } from '../../services/reservation';
import { Booking } from '../../models/cafe';

@Component({
  selector: 'app-my-bookings',
  imports: [RouterLink],
  templateUrl: './my-bookings.html',
  styleUrl: './my-bookings.css',
})
export class MyBookings implements OnInit {
  private reservationService = inject(ReservationService);
  private auth = inject(AuthService);
  private router = inject(Router);

  bookings = signal<Booking[]>([]);
  loading = signal<boolean>(true);
  error = signal<string>('');

  ngOnInit(): void {
    if (!this.auth.isAuthenticated()) {
      this.router.navigate(['/login']);
      return;
    }
    this.load();
  }

  load(): void {
    this.loading.set(true);
    this.reservationService.list().subscribe({
      next: data => {
        this.bookings.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Failed to load bookings.');
        this.loading.set(false);
      },
    });
  }

  cancel(id: number): void {
    this.reservationService.remove(id).subscribe({
      next: () => this.bookings.set(this.bookings().filter(b => b.id !== id)),
      error: () => this.error.set('Could not cancel booking.'),
    });
  }
}
