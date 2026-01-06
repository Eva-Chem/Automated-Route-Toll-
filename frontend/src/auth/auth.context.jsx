import { createContext, useContext } from "react";
import { mockUser } from "../mock/auth.mock";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => (
  <AuthContext.Provider value={{ user: mockUser }}>
    {children}
  </AuthContext.Provider>
);

export const useAuth = () => useContext(AuthContext);
