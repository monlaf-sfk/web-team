import { Routes } from '@angular/router';
import { Home } from './components/home/home'
import { Login } from './components/login/login'
import { CafeDetail } from './components/cafe-detail/cafe-detail'
import { MyBookings } from './components/my-bookings/my-bookings'

export const routes: Routes = [
    {path: '', component: Home},
    {path: 'login', component: Login},
    {path: 'cafe/:id', component: CafeDetail},
    {path: 'my-bookings', component: MyBookings},
    {path: '**', redirectTo: ''}
];
