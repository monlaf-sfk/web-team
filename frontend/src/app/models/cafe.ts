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
}

export interface MenuItem {
    id: number;
    name: string;
    price: number;
}

export interface Booking {
    id: number;
    cafe: number;
    date: string;
    time: string;
    guests: number;
}
