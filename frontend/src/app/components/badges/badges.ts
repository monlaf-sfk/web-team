import { Component, OnInit, inject, signal } from '@angular/core';

import { CafeService } from '../../services/cafe';
import { MyBadges } from '../../models/cafe';

@Component({
  selector: 'app-badges',
  imports: [],
  templateUrl: './badges.html',
  styleUrl: './badges.css',
})
export class Badges implements OnInit {
  private cafeService = inject(CafeService);

  data = signal<MyBadges | null>(null);
  loading = signal<boolean>(true);
  error = signal<string>('');

  ngOnInit(): void {
    this.cafeService.getMyBadges().subscribe({
      next: res => {
        this.data.set(res);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Failed to load badges.');
        this.loading.set(false);
      },
    });
  }

  progressPercent(): number {
    const d = this.data();
    if (!d) return 0;
    const prev = (d.level - 1) * 5;
    const span = d.next_level_xp - prev || 1;
    return Math.min(100, ((d.xp - prev) / span) * 100);
  }

  badgeProgress(earned: boolean, progress: number, threshold: number): number {
    if (earned) return 100;
    return Math.min(100, (progress / threshold) * 100);
  }
}
