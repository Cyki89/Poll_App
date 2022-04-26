import { createContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import jwtDecode from "jwt-decode";
import axios from "../api/axios";

const AuthContext = createContext();

export default AuthContext;

export const AuthProvider = ({ children }) => {
  const [accessToken, setAccessToken] = useState();
  const [user, setUser] = useState();

  const navigate = useNavigate();

  const login = async ({ username, password }) => {
    const response = await axios.post("/ldap/jwt/create/", {
      username,
      password,
    });

    const data = response.data;
    setAccessToken(data?.access);
    setUser(jwtDecode(data?.access));
  };

  const logout = async () => {
    await axios.post("/ldap/logout/", {}, { withCredentials: true });

    setAccessToken(null);
    setUser(null);
    navigate("/login", { replace: true });
  };

  const isAdmin = () => {
    return user && user.groups?.includes("Admins");
  };

  const contextData = {
    user,
    isAdmin,
    accessToken,
    setAccessToken,
    setUser,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={contextData}>{children}</AuthContext.Provider>
  );
};
