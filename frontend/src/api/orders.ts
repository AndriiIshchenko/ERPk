import api from "./axios";
import { Order } from "../types";

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

export const createOrder = async (customerId: string): Promise<Order> => {
  const { data } = await api.post<Order>("/orders/", { customer_id: customerId });
  return data;
};

export const addOrderItem = async (orderId: string, productId: string): Promise<Order> => {
  const { data } = await api.post<Order>(`/orders/${orderId}/items`, { product_id: productId });
  return data;
};

export const removeOrderItem = async (orderId: string, itemId: string): Promise<Order> => {
  const { data } = await api.delete<Order>(`/orders/${orderId}/items/${itemId}`);
  return data;
};

export const confirmOrder = async (orderId: string): Promise<Order> => {
  const { data } = await api.post<Order>(`/orders/${orderId}/confirm`);
  return data;
};

export const markOrderPaid = async (orderId: string): Promise<Order> => {
  const { data } = await api.post<Order>(`/orders/${orderId}/pay`);
  return data;
};

export const cancelOrder = async (orderId: string): Promise<Order> => {
  const { data } = await api.post<Order>(`/orders/${orderId}/cancel`);
  return data;
};

export const deleteOrder = async (id: string): Promise<void> => {
  await api.delete(`/orders/${id}`);
};
