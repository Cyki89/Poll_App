import jwtDecode from "jwt-decode";
import axios from "../api/axios";
import useAuth from "./useAuth";
import { LOCAL_STORAGE_AUTH_KEY } from "../utils/auth";

const useRefreshToken = () => {
  const { authTokens, setAuthTokens, setUser } = useAuth();

  const refresh = async () => {
    console.log("Access Token Is Expired");
    const {
      data: { access },
    } = await axios.post("/auth/jwt/refresh/", {
      refresh: authTokens.refresh,
    });

    const newAuthTokens = { refresh: authTokens.refresh, access };
    localStorage.setItem(LOCAL_STORAGE_AUTH_KEY, JSON.stringify(newAuthTokens));

    setUser(jwtDecode(access));
    setAuthTokens(newAuthTokens);

    return access;
  };
  return refresh;
};

export default useRefreshToken;
