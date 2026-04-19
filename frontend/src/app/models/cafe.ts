export interface Category {
  id: number;
  name: string;
}

export interface Mood {
  id: number;
  slug: string;
  name: string;
  emoji: string;
}

export interface Cafe {
  id: number;
  name: string;
  address: string;
  description: string;
  image: string;
  category: Category;
  moods: Mood[];
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

export interface BadgeStatus {
  slug: string;
  name: string;
  emoji: string;
  description: string;
  threshold: number;
  progress: number;
  earned: boolean;
}

export interface MyBadges {
  username: string;
  level: number;
  xp: number;
  next_level_xp: number;
  reservations: number;
  reviews: number;
  earned_count: number;
  total_count: number;
  badges: BadgeStatus[];
}

export interface HourBusyness {
  hour: number;
  count: number;
  level: 'empty' | 'low' | 'medium' | 'high';
}

export interface CafeBusyness {
  hours: HourBusyness[];
  current: { count: number; level: HourBusyness['level']; hour: number };
}
