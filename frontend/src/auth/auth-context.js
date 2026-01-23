import { createContext } from "react";

/**
 * AuthContext
 * 
 * Holds authentication state: user, token, login/logout functions, and isAuthenticated flag.
 * Exported for use in use-auth.js hook.
 */
export const AuthContext = createContext();
