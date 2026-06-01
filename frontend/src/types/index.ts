export interface Customer {
  id: string;
  name: string;
  email: string;
  phone?: string;
  created_at: string;
}

export interface Product {
  id: string;
  name: string;
  description?: string;
  price: number;
  created_at: string;
}

export interface OrderItem {
  id: string;
  product_id: string;
  product_name: string;
  price_snapshot: number;
}

export interface Order {
  id: string;
  customer: Customer;
  items: OrderItem[];
  total_amount: number;
  status: "draft" | "pending" | "paid" | "cancelled";
  created_at: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}
