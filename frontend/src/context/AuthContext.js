import { createContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import jwtDecode from "jwt-decode";
import axios from "../api/axios";
import { validToken, getTokens, LOCAL_STORAGE_AUTH_KEY } from "./../utils/auth";

const AuthContext = createContext();

export default AuthContext;

export const AuthProvider = ({ children }) => {
  const tokens = getTokens();
  const validTokens = tokens && validToken(tokens.refresh);
  if (!validTokens) localStorage.removeItem(LOCAL_STORAGE_AUTH_KEY);

  const [authTokens, setAuthTokens] = useState(validTokens ? tokens : null);
  const [user, setUser] = useState(
    validTokens ? jwtDecode(tokens.access) : null
  );

  const navigate = useNavigate();

  const login = async ({ username, password }) => {
    const response = await axios.post("/ldap/jwt/create/", {
      username,
      password,
    });

    const data = response.data;
    setAuthTokens(data);
    setUser(jwtDecode(data.access));
    localStorage.setItem(LOCAL_STORAGE_AUTH_KEY, JSON.stringify(data));
  };

  const logout = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem(LOCAL_STORAGE_AUTH_KEY);
    navigate("/login", { replace: true });
  };

  const isAdmin = () => {
    return user && user.groups?.includes("Admins");
  };

  const contextData = {
    user,
    isAdmin,
    authTokens,
    setAuthTokens,
    setUser,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={contextData}>{children}</AuthContext.Provider>
  );
};
