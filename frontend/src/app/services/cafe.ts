import { Injectable } from '@angular/core';
import { Category, Cafe, MenuItem, Booking } from '../models/cafe';

@Injectable({
  providedIn: 'root',
})

export class CafeService {
  // fake data - then will be replaced with real api calls

  private categories: Category[] = [
    { id: 1, name: 'Coffee Shops' },
    { id: 2, name: 'Italian' },
    { id: 3, name: 'Fast Food' },
  ]

  private cafes: Cafe[] = [
    { id: 1, name: 'Cozy Corner', address: 'Almaty, Abay 10', description: 'A warm cozy coffee shop', image: 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=400', category: { id: 1, name: 'Coffee Shops' } },
    { id: 2, name: 'Pasta House', address: 'Almaty, Dostyk 5', description: 'Authentic Italian pasta', image: 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=400', category: { id: 2, name: 'Italian' } },
    { id: 3, name: 'Burger Town', address: 'Almaty, Furmanov 22', description: 'Best burgers in town', image: 'https://images.unsplash.com/photo-1561758033-d89a9ad46330?w=400', category: { id: 3, name: 'Fast Food' } },
    { id: 4, name: 'Latte Art', address: 'Almaty, Nazarbayev 15', description: 'Specialty coffee and pastries', image: 'https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=400', category: { id: 1, name: 'Coffee Shops' } },
  ];

  private menuItems: MenuItem[] = [
    { id: 1, name: 'Cappuccino', price: 1200 },
    { id: 2, name: 'Croissant', price: 800 },
    { id: 3, name: 'Spaghetti Carbonara', price: 2500 },
    { id: 4, name: 'Tiramisu', price: 1500 },
    { id: 5, name: 'Cheeseburger', price: 1800 },
    { id: 6, name: 'French Fries', price: 700 },
  ];

  private bookings: Booking[] = [];


  // methods that return data

  getCategories(): Category[] {
    return this.categories;
  }

  getCafes(): Cafe[] {
    return this.cafes;
  }

  getCafeById(id: number): Cafe | undefined {
    return this.cafes.find(cafe => cafe.id === id);
  }

  getMenuItems(): MenuItem[] {
    return this.menuItems;
  }

  getBookings(): Booking[] {
    return this.bookings;
  }

  addBooking(booking: Booking): void {
    this.bookings.push(booking);
  }

}
