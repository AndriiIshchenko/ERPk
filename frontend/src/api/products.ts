import api from "./axios";
import { Product } from "../types";

export interface ProductPayload {
  name: string;
  description?: string;
  price: number;
}

export const getProducts = async (): Promise<Product[]> => {
  const { data } = await api.get<Product[]>("/products/");
  return data;
};

export const getProduct = async (id: string): Promise<Product> => {
  const { data } = await api.get<Product>(`/products/${id}`);
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

export const deleteProduct = async (id: string): Promise<void> => {
  await api.delete(`/products/${id}`);
};
