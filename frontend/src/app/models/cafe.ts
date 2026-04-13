export interface Category {
  id: number;
  name: string;
}

export interface Cafe {
  id: number;
  name: string;
  address: string;
  description: string;
  image: string;
  category: Category;
  opens_at: string;
  closes_at: string;
  avg_rating: number | null;
  reviews_count: number;
}

export interface MenuItem {
  id: number;
  cafe: number;
  name: string;
  price: number;
}

export interface Booking {
  id: number;
  cafe: number;
  cafe_name?: string;
  date: string;
  time: string;
  guests: number;
  created_at?: string;
}

export interface Review {
  id: number;
  cafe: number;
  username: string;
  rating: number;
  text: string;
  created_at: string;
}

export interface Paginated<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
