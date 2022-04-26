import jwtDecode from "jwt-decode";

export const validToken = (token) =>
  token && jwtDecode(token).exp > Date.now() / 1000;
