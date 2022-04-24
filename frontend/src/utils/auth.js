import jwtDecode from "jwt-decode";

export const LOCAL_STORAGE_AUTH_KEY = "pollApp:authTokens";

export const validToken = (token) =>
  token && jwtDecode(token).exp > Date.now() / 1000;

export const getTokens = () =>
  JSON.parse(localStorage.getItem(LOCAL_STORAGE_AUTH_KEY));
