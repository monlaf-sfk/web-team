# Web Team Project

Theme: CafeCatalog

CafeCatalog allows users to browse a structured directory of restaurants organized by cuisine categories and view detailed menus for each establishment. Authorized users can select a specific venue and instantly book a table by providing the date, time, and number of guests.

## Group Members

- Kanatkyzy Sabina
- Kerimzhanov Rasul
- Smailov Yussuf

## Stack

- Backend: Django 4.2, Django REST Framework, SimpleJWT, django-filter, django-cors-headers, SQLite
- Frontend: Angular 21 (standalone components, signals), TypeScript

## Project Structure

```
web-team/
  backend/        Django project (config) + api app
  frontend/       Angular app
  docker-compose.yml
```

## Backend — how to run

From the `backend/` folder:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate          
pip install -r requirements.txt
python manage.py migrate
python manage.py seed               
python manage.py createsuperuser    
python manage.py runserver 8000
```

API available at `http://localhost:8000/api/`, admin at `http://localhost:8000/admin/`.

### Key endpoints

| Method | URL | Description |
|--------|-----|-------------|
| `GET` | `/api/categories/` | list cuisine categories |
| `GET` | `/api/cafes/` | list cafes (supports `?category=`, `?search=`, `?ordering=name` or `-avg_rating`) |
| `GET` | `/api/cafes/<id>/` | cafe details with `avg_rating`, `opens_at`, `closes_at` |
| `GET` | `/api/menu-items/?cafe=<id>` | menu items for a cafe |
| `GET/POST` | `/api/cafes/<id>/reviews/` | list / create reviews (POST requires auth) |
| `GET/POST` | `/api/reservations/` | user's bookings (requires auth) |
| `DELETE` | `/api/reservations/<id>/` | cancel own booking |
| `POST` | `/api/register/` | register `{username, password}` |
| `POST` | `/api/token/` | obtain JWT `{access, refresh}` |
| `POST` | `/api/token/refresh/` | refresh access token |

## Frontend — how to run

From the `frontend/` folder:

```bash
cd frontend
npm install
npm start           
```

App opens at `http://localhost:4200/`. The backend must be running on `http://localhost:8000`.

## Features

- Browse cafes by cuisine category, search by name, sort by rating
- Cafe detail with menu, working hours and "Open now / Closed" badge
- JWT authentication (register, login, logout)
- Book a table (date, time, guests) for authorized users
- Personal bookings page with cancel action
- Reviews and ratings (1–5 stars, one review per user per cafe)
- Favorites via `localStorage`, separate `/favorites` page
- Client-side and server-side validation with readable error messages

## Common issues

- **CORS error in browser** — make sure the backend is running on port 8000 and the frontend on port 4200.
- **`401 Unauthorized`** — your JWT expired; the app will log you out automatically, just log in again.
- **No cafes on the page** — run `python manage.py seed` to load demo data.
