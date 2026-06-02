import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  addOrderItem,
  cancelOrder,
  confirmOrder,
  createOrder,
  deleteOrder,
  getOrder,
  getOrders,
  getOrdersByCustomer,
  markOrderPaid,
  removeOrderItem,
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
    mutationFn: (customerId: string) => createOrder(customerId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["orders"] }),
  });
};

export const useAddOrderItem = (orderId: string) => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (productId: string) => addOrderItem(orderId, productId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["orders", orderId] }),
  });
};

export const useRemoveOrderItem = (orderId: string) => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (itemId: string) => removeOrderItem(orderId, itemId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["orders", orderId] }),
  });
};

export const useConfirmOrder = (orderId: string) => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: () => confirmOrder(orderId),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["orders", orderId] });
      qc.invalidateQueries({ queryKey: ["orders"] });
    },
  });
};

export const useMarkOrderPaid = (orderId: string) => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: () => markOrderPaid(orderId),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["orders", orderId] });
      qc.invalidateQueries({ queryKey: ["orders"] });
    },
  });
};

export const useCancelOrder = (orderId: string) => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: () => cancelOrder(orderId),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["orders", orderId] });
      qc.invalidateQueries({ queryKey: ["orders"] });
    },
  });
};

export const useDeleteOrder = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => deleteOrder(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["orders"] }),
  });
};
