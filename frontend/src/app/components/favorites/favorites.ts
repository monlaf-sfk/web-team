import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { CafeService } from '../../services/cafe';
import { FavoritesService } from '../../services/favorites';
import { Cafe } from '../../models/cafe';

@Component({
  selector: 'app-favorites',
  imports: [RouterLink],
  templateUrl: './favorites.html',
  styleUrl: './favorites.css',
})
export class Favorites implements OnInit {
  private cafeService = inject(CafeService);
  protected favorites = inject(FavoritesService);

  all = signal<Cafe[]>([]);
  loading = signal<boolean>(true);
  error = signal<string>('');

  list = computed(() => this.all().filter(c => this.favorites.has(c.id)));

  ngOnInit(): void {
    this.cafeService.getCafes().subscribe({
      next: data => {
        this.all.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Failed to load cafes.');
        this.loading.set(false);
      },
    });
  }

  remove(id: number): void {
    this.favorites.toggle(id);
  }
}
