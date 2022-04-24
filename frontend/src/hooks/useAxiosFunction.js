import { useState, useEffect } from "react";

const useAxiosFunction = () => {
  const [response, setResponse] = useState();
  const [status, setStatus] = useState();
  const [error, setError] = useState();
  const [loading, setLoading] = useState(false);
  const [controller, setController] = useState();

  const clearError = () => {
    setError("");
  };

  const clearResponse = () => {
    setResponse(null);
  };

  const axiosFetch = async (configObj) => {
    const {
      axiosInstance,
      method,
      url,
      setResponseError,
      requestConfig = {},
    } = configObj;

    try {
      setLoading(true);
      const ctrl = new AbortController();
      setController(ctrl);
      const res = await axiosInstance[method.toLowerCase()](url, {
        ...requestConfig,
        signal: ctrl.signal,
      });
      setResponse(res.data);
      setStatus(res.status);
    } catch (err) {
      setError(setResponseError(err));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // useEffect cleanup function
    return () => controller && controller.abort();
  }, [controller]);

  return {
    response,
    status,
    error,
    loading,
    clearResponse,
    clearError,
    axiosFetch,
  };
};

export default useAxiosFunction;
