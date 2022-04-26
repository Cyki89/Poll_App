import jwtDecode from "jwt-decode";
import axios from "../api/axios";
import useAuth from "./useAuth";

const useRefreshToken = () => {
  const { setAccessToken, setUser } = useAuth();

  const refresh = async () => {
    const response = await axios.post("/ldap/jwt/refresh/", {});

    const access = response.data.access;
    setAccessToken(access);
    setUser(jwtDecode(access));

    return access;
  };
  return refresh;
};

export default useRefreshToken;
