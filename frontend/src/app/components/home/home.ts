import { Component, inject, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CafeService } from '../../services/cafe';
import { Category, Cafe } from '../../models/cafe';

@Component({
  selector: 'app-home',
  imports: [RouterLink],
  templateUrl: './home.html',
  styleUrl: './home.css',
})

export class Home implements OnInit {
  private cafeService = inject(CafeService);

  categories: Category[] = [];
  cafes: Cafe[] = [];
  filteredCafes: Cafe[] = [];
  selectedCategory: number | null = null;

  ngOnInit(): void {
    this.categories = this.cafeService.getCategories();
    this.cafes = this.cafeService.getCafes();
    this.filteredCafes = this.cafes;
  }

  filterByCategory(categoryId: number): void {
    if(this.selectedCategory === categoryId) {
      this.selectedCategory = null;
      this.filteredCafes = this.cafes;
    }
    else{
      this.selectedCategory = categoryId;
      this.filteredCafes = this.cafes.filter(cafe => cafe.category.id === categoryId);
    }
  }

}
