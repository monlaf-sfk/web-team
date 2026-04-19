import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import {
  Cafe,
  CafeBusyness,
  Category,
  MenuItem,
  Mood,
  MyBadges,
  Paginated,
  Review,
} from '../models/cafe';

const API = 'http://localhost:8000/api';

interface NewReview {
  rating: number;
  text: string;
}

@Injectable({ providedIn: 'root' })
export class CafeService {
  private http = inject(HttpClient);

  getCategories(): Observable<Category[]> {
    return this.http
      .get<Paginated<Category>>(`${API}/categories/`)
      .pipe(map(res => res.results));
  }

  getMoods(): Observable<Mood[]> {
    return this.http.get<Mood[]>(`${API}/moods/`);
  }

  getCafes(
    categoryId?: number | null,
    search?: string,
    ordering?: string,
    moodSlugs?: string[],
  ): Observable<Cafe[]> {
    let params = new HttpParams();
    if (categoryId) {
      params = params.set('category', categoryId);
    }
    if (search) {
      params = params.set('search', search);
    }
    if (ordering) {
      params = params.set('ordering', ordering);
    }
    if (moodSlugs && moodSlugs.length) {
      params = params.set('moods', moodSlugs.join(','));
    }
    return this.http
      .get<Paginated<Cafe>>(`${API}/cafes/`, { params })
      .pipe(map(res => res.results));
  }

  getCafesByIds(ids: number[]): Observable<Cafe[]> {
    return this.http
      .get<Paginated<Cafe>>(`${API}/cafes/`)
      .pipe(map(res => res.results.filter(c => ids.includes(c.id))));
  }

  getCafeById(id: number): Observable<Cafe> {
    return this.http.get<Cafe>(`${API}/cafes/${id}/`);
  }

  getMenuItems(cafeId: number): Observable<MenuItem[]> {
    const params = new HttpParams().set('cafe', cafeId);
    return this.http
      .get<Paginated<MenuItem>>(`${API}/menu-items/`, { params })
      .pipe(map(res => res.results));
  }

  getReviews(cafeId: number): Observable<Review[]> {
    return this.http
      .get<Paginated<Review>>(`${API}/cafes/${cafeId}/reviews/`)
      .pipe(map(res => res.results));
  }

  addReview(cafeId: number, data: NewReview): Observable<Review> {
    return this.http.post<Review>(`${API}/cafes/${cafeId}/reviews/`, data);
  }

  getBusyness(cafeId: number): Observable<CafeBusyness> {
    return this.http.get<CafeBusyness>(`${API}/cafes/${cafeId}/busyness/`);
  }

  getMyBadges(): Observable<MyBadges> {
    return this.http.get<MyBadges>(`${API}/me/badges/`);
  }
}
