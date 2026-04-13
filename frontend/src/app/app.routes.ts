import { Routes } from '@angular/router';
import { Home } from './components/home/home';
import { Login } from './components/login/login';
import { Register } from './components/register/register';
import { CafeDetail } from './components/cafe-detail/cafe-detail';
import { MyBookings } from './components/my-bookings/my-bookings';
import { Favorites } from './components/favorites/favorites';

export const routes: Routes = [
  { path: '', component: Home },
  { path: 'login', component: Login },
  { path: 'register', component: Register },
  { path: 'cafe/:id', component: CafeDetail },
  { path: 'my-bookings', component: MyBookings },
  { path: 'favorites', component: Favorites },
  { path: '**', redirectTo: '' },
];
