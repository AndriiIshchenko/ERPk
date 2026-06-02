import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  createProduct,
  deactivateProduct,
  deleteProduct,
  getProduct,
  getProductHistory,
  getProducts,
  ProductPayload,
  restoreProduct,
  updateProduct,
} from "../api/products";

export const useProducts = (includeInactive = false) =>
  useQuery({
    queryKey: ["products", { includeInactive }],
    queryFn: () => getProducts(includeInactive),
  });

export const useProduct = (id: string) =>
  useQuery({
    queryKey: ["products", id],
    queryFn: () => getProduct(id),
    enabled: !!id,
  });

export const useProductHistory = (id: string) =>
  useQuery({
    queryKey: ["products", id, "history"],
    queryFn: () => getProductHistory(id),
    enabled: !!id,
  });

export const useCreateProduct = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: ProductPayload) => createProduct(payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["products"] }),
  });
};

export const useUpdateProduct = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, payload }: { id: string; payload: Partial<ProductPayload> }) =>
      updateProduct(id, payload),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["products"] }),
  });
};

export const useDeactivateProduct = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => deactivateProduct(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["products"] }),
  });
};

export const useRestoreProduct = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => restoreProduct(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["products"] }),
  });
};

export const useDeleteProduct = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => deleteProduct(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["products"] }),
  });
};
