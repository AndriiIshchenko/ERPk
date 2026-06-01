import api from "./axios";
import { Order } from "../types";

export interface OrderPayload {
  customer_id: string;
  product_ids: string[];
}

export const getOrders = async (): Promise<Order[]> => {
  const { data } = await api.get<Order[]>("/orders/");
  return data;
};

export const getOrder = async (id: string): Promise<Order> => {
  const { data } = await api.get<Order>(`/orders/${id}`);
  return data;
};

export const getOrdersByCustomer = async (customerId: string): Promise<Order[]> => {
  const { data } = await api.get<Order[]>(`/orders/customer/${customerId}`);
  return data;
};

export const createOrder = async (payload: OrderPayload): Promise<Order> => {
  const { data } = await api.post<Order>("/orders/", payload);
  return data;
};

export const deleteOrder = async (id: string): Promise<void> => {
  await api.delete(`/orders/${id}`);
};
