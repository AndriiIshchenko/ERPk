import api from "./axios";
import { Token } from "../types";

export const login = async (email: string, password: string): Promise<Token> => {
  const { data } = await api.post<Token>("/auth/login", { email, password });
  return data;
};

export const register = async (email: string, password: string): Promise<Token> => {
  const { data } = await api.post<Token>("/auth/register", { email, password });
  return data;
};
