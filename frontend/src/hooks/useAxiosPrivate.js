import { useEffect } from "react";
import { axiosPrivate } from "../api/axios";
import { validToken } from "../utils/auth";
import useRefreshToken from "./useRefreshToken";
import useAuth from "./useAuth";

const useAxiosPrivate = () => {
  const { authTokens, logout } = useAuth();
  const refreshAccess = useRefreshToken();

  useEffect(() => {
    const requestIntercept = axiosPrivate.interceptors.request.use(
      async (request) => {
        if (!request.headers["Authorization"]) {
          request.headers["Authorization"] = `JWT ${authTokens?.access}`;
        }
        const { access, refresh } = authTokens;

        if (!validToken(refresh)) return logout();

        if (validToken(access)) return request;

        const newAccess = await refreshAccess();

        request.headers.Authorization = `JWT ${newAccess}`;
        return request;
      },
      (error) => Promise.reject(error)
    );

    return () => {
      axiosPrivate.interceptors.request.eject(requestIntercept);
    };
  }, [authTokens, refreshAccess, logout]);

  return axiosPrivate;
};

export default useAxiosPrivate;
