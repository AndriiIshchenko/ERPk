import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  createOrder,
  deleteOrder,
  getOrder,
  getOrders,
  getOrdersByCustomer,
  OrderPayload,
} from "../api/orders";

export const useOrders = () =>
  useQuery({ queryKey: ["orders"], queryFn: getOrders });

export const useOrder = (id: string) =>
  useQuery({
    queryKey: ["orders", id],
    queryFn: () => getOrder(id),
    enabled: !!id,
  });

export const useOrdersByCustomer = (customerId: string) =>
  useQuery({
    queryKey: ["orders", "customer", customerId],
    queryFn: () => getOrdersByCustomer(customerId),
    enabled: !!customerId,
  });

export const useCreateOrder = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: OrderPayload) => createOrder(payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["orders"] }),
  });
};

export const useDeleteOrder = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => deleteOrder(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["orders"] }),
  });
};
