import { mockUser } from "../mock/auth.mock";

export const getCurrentUser = () => mockUser;
export const isAdmin = () => mockUser.role === "admin";
export const isOperator = () => mockUser.role === "operator";
