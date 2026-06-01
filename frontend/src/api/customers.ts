import api from "./axios";
import { Customer } from "../types";

export interface CustomerPayload {
  name: string;
  email: string;
  phone?: string;
}

export const getCustomers = async (): Promise<Customer[]> => {
  const { data } = await api.get<Customer[]>("/customers/");
  return data;
};

export const getCustomer = async (id: string): Promise<Customer> => {
  const { data } = await api.get<Customer>(`/customers/${id}`);
  return data;
};

export const createCustomer = async (payload: CustomerPayload): Promise<Customer> => {
  const { data } = await api.post<Customer>("/customers/", payload);
  return data;
};

export const updateCustomer = async (
  id: string,
  payload: Partial<CustomerPayload>
): Promise<Customer> => {
  const { data } = await api.put<Customer>(`/customers/${id}`, payload);
  return data;
};

export const deleteCustomer = async (id: string): Promise<void> => {
  await api.delete(`/customers/${id}`);
};
