import { Injectable, signal } from '@angular/core';

const KEY = 'favorites';

@Injectable({ providedIn: 'root' })
export class FavoritesService {
  private state = signal<number[]>(this.readStorage());

  list = this.state.asReadonly();

  has(id: number): boolean {
    return this.state().includes(id);
  }

  toggle(id: number): void {
    const current = this.state();
    const next = current.includes(id)
      ? current.filter(x => x !== id)
      : [...current, id];
    this.state.set(next);
    localStorage.setItem(KEY, JSON.stringify(next));
  }

  private readStorage(): number[] {
    const raw = localStorage.getItem(KEY);
    if (!raw) {
      return [];
    }
    try {
      const parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed.filter(x => typeof x === 'number') : [];
    } catch {
      return [];
    }
  }
}
