import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  createCustomer,
  CustomerPayload,
  deleteCustomer,
  getCustomer,
  getCustomers,
  updateCustomer,
} from "../api/customers";

export const useCustomers = () =>
  useQuery({ queryKey: ["customers"], queryFn: getCustomers });

export const useCustomer = (id: string) =>
  useQuery({
    queryKey: ["customers", id],
    queryFn: () => getCustomer(id),
    enabled: !!id,
  });

export const useCreateCustomer = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: CustomerPayload) => createCustomer(payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["customers"] }),
  });
};

export const useUpdateCustomer = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({
      id,
      payload,
    }: {
      id: string;
      payload: Partial<CustomerPayload>;
    }) => updateCustomer(id, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["customers"] }),
  });
};

export const useDeleteCustomer = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => deleteCustomer(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["customers"] }),
  });
};
