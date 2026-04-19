import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';

import { CafeService } from '../../services/cafe';
import { FavoritesService } from '../../services/favorites';
import { Cafe, Category, Mood } from '../../models/cafe';
import { isCafeOpenNow } from '../../utils/open-now';

@Component({
  selector: 'app-home',
  imports: [RouterLink, FormsModule],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home implements OnInit {
  private cafeService = inject(CafeService);
  protected favorites = inject(FavoritesService);

  categories = signal<Category[]>([]);
  moods = signal<Mood[]>([]);
  cafes = signal<Cafe[]>([]);
  loading = signal<boolean>(true);
  error = signal<string>('');

  selectedCategory: number | null = null;
  selectedMoods = signal<Set<string>>(new Set());
  search = '';
  ordering: '' | '-avg_rating' | 'name' = '';

  ngOnInit(): void {
    this.cafeService.getCategories().subscribe({
      next: data => this.categories.set(data),
      error: () => this.error.set('Failed to load categories.'),
    });
    this.cafeService.getMoods().subscribe({
      next: data => this.moods.set(data),
      error: () => {},
    });
    this.loadCafes();
  }

  filterByCategory(categoryId: number): void {
    this.selectedCategory = this.selectedCategory === categoryId ? null : categoryId;
    this.loadCafes();
  }

  toggleMood(slug: string): void {
    const next = new Set(this.selectedMoods());
    if (next.has(slug)) {
      next.delete(slug);
    } else {
      next.add(slug);
    }
    this.selectedMoods.set(next);
    this.loadCafes();
  }

  isMoodActive(slug: string): boolean {
    return this.selectedMoods().has(slug);
  }

  onSearchChange(): void {
    this.loadCafes();
  }

  onOrderingChange(): void {
    this.loadCafes();
  }

  toggleFavorite(id: number, event: Event): void {
    event.preventDefault();
    event.stopPropagation();
    this.favorites.toggle(id);
  }

  isOpen(cafe: Cafe): boolean {
    return isCafeOpenNow(cafe.opens_at, cafe.closes_at);
  }

  private loadCafes(): void {
    this.loading.set(true);
    const moodSlugs = Array.from(this.selectedMoods());
    this.cafeService
      .getCafes(this.selectedCategory, this.search.trim(), this.ordering || undefined, moodSlugs)
      .subscribe({
        next: data => {
          this.cafes.set(data);
          this.loading.set(false);
        },
        error: () => {
          this.error.set('Failed to load cafes.');
          this.loading.set(false);
        },
      });
  }
}
