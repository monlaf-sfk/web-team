import { HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { AuthService } from '../../services/auth';
import { CafeService } from '../../services/cafe';
import { FavoritesService } from '../../services/favorites';
import { ReservationService } from '../../services/reservation';
import { Cafe, MenuItem, Review } from '../../models/cafe';
import { extractErrors } from '../../utils/errors';
import { isCafeOpenNow } from '../../utils/open-now';

@Component({
  selector: 'app-cafe-detail',
  imports: [FormsModule, RouterLink],
  templateUrl: './cafe-detail.html',
  styleUrl: './cafe-detail.css',
})
export class CafeDetail implements OnInit {
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private cafeService = inject(CafeService);
  private reservationService = inject(ReservationService);
  protected auth = inject(AuthService);
  protected favorites = inject(FavoritesService);

  cafe = signal<Cafe | null>(null);
  menu = signal<MenuItem[]>([]);
  reviews = signal<Review[]>([]);
  loading = signal<boolean>(true);
  error = signal<string>('');

  date = '';
  time = '';
  guests = 2;
  submitting = signal<boolean>(false);
  successMessage = signal<string>('');
  bookingErrors = signal<Record<string, string>>({});

  reviewRating = 5;
  reviewText = '';
  submittingReview = signal<boolean>(false);
  reviewSuccess = signal<string>('');
  reviewErrors = signal<Record<string, string>>({});

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (!id) {
      this.error.set('Cafe not found.');
      this.loading.set(false);
      return;
    }

    this.cafeService.getCafeById(id).subscribe({
      next: cafe => this.cafe.set(cafe),
      error: () => this.error.set('Failed to load cafe.'),
    });
    this.cafeService.getMenuItems(id).subscribe({
      next: items => {
        this.menu.set(items);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Failed to load menu.');
        this.loading.set(false);
      },
    });
    this.loadReviews(id);
  }

  isOpen(): boolean {
    const c = this.cafe();
    return c ? isCafeOpenNow(c.opens_at, c.closes_at) : false;
  }

  toggleFav(): void {
    const c = this.cafe();
    if (c) {
      this.favorites.toggle(c.id);
    }
  }

  book(): void {
    if (!this.auth.isAuthenticated()) {
      this.router.navigate(['/login']);
      return;
    }
    const cafe = this.cafe();
    if (!cafe) {
      return;
    }

    this.bookingErrors.set({});
    this.successMessage.set('');

    if (!this.date || !this.time) {
      this.bookingErrors.set({ detail: 'Please fill in date and time.' });
      return;
    }

    this.submitting.set(true);
    this.reservationService
      .create({ cafe: cafe.id, date: this.date, time: this.time, guests: this.guests })
      .subscribe({
        next: () => {
          this.successMessage.set('Reservation created!');
          this.submitting.set(false);
          this.date = '';
          this.time = '';
          this.guests = 2;
        },
        error: (err: HttpErrorResponse) => {
          this.bookingErrors.set(extractErrors(err));
          this.submitting.set(false);
        },
      });
  }

  submitReview(): void {
    if (!this.auth.isAuthenticated()) {
      this.router.navigate(['/login']);
      return;
    }
    const cafe = this.cafe();
    if (!cafe) {
      return;
    }

    this.reviewErrors.set({});
    this.reviewSuccess.set('');
    this.submittingReview.set(true);

    this.cafeService
      .addReview(cafe.id, { rating: this.reviewRating, text: this.reviewText })
      .subscribe({
        next: review => {
          this.reviews.set([review, ...this.reviews()]);
          this.reviewRating = 5;
          this.reviewText = '';
          this.reviewSuccess.set('Thanks for your review!');
          this.submittingReview.set(false);
          this.cafeService.getCafeById(cafe.id).subscribe(c => this.cafe.set(c));
        },
        error: (err: HttpErrorResponse) => {
          this.reviewErrors.set(extractErrors(err));
          this.submittingReview.set(false);
        },
      });
  }

  private loadReviews(cafeId: number): void {
    this.cafeService.getReviews(cafeId).subscribe({
      next: data => this.reviews.set(data),
      error: () => {},
    });
  }
}
