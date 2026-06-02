import api from "./axios";
import { Product, ProductHistory } from "../types";

export interface ProductPayload {
  name: string;
  description?: string;
  price: number;
}

export const getProducts = async (includeInactive = false): Promise<Product[]> => {
  const { data } = await api.get<Product[]>("/products/", {
    params: includeInactive ? { include_inactive: true } : {},
  });
  return data;
};

export const getProduct = async (id: string): Promise<Product> => {
  const { data } = await api.get<Product>(`/products/${id}`);
  return data;
};

export const getProductHistory = async (id: string): Promise<ProductHistory[]> => {
  const { data } = await api.get<ProductHistory[]>(`/products/${id}/history`);
  return data;
};

export const createProduct = async (payload: ProductPayload): Promise<Product> => {
  const { data } = await api.post<Product>("/products/", payload);
  return data;
};

export const updateProduct = async (
  id: string,
  payload: Partial<ProductPayload>
): Promise<Product> => {
  const { data } = await api.put<Product>(`/products/${id}`, payload);
  return data;
};

export const deactivateProduct = async (id: string): Promise<Product> => {
  const { data } = await api.post<Product>(`/products/${id}/deactivate`);
  return data;
};

export const restoreProduct = async (id: string): Promise<Product> => {
  const { data } = await api.post<Product>(`/products/${id}/restore`);
  return data;
};

export const deleteProduct = async (id: string): Promise<void> => {
  await api.delete(`/products/${id}`);
};
