import { useRef, useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Spinner from "react-bootstrap/Spinner";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import useAuth from "../hooks/useAuth";

const Login = () => {
  const { login } = useAuth();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const usernameRef = useRef();
  const errorRef = useRef();

  useEffect(() => {
    usernameRef.current.focus();
  }, []);

  useEffect(() => {
    setError("");
  }, [username, password]);

  const navigate = useNavigate();
  const location = useLocation();

  const handleSubmit = async (e) => {
    setLoading(true);
    e.preventDefault();
    try {
      const from = location.state?.from || "/";
      await login({ username, password });
      navigate(from, { replace: true });
    } catch (err) {
      if (!err.response)
        setError("Server problem. Please try again in a minute");
      if (err.response.status === 400) setError("Invalid Credentials");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Form className="app-form" onSubmit={handleSubmit}>
      <h1 className="app-form-header">Login Form</h1>
      <Form.Group className="mb-3">
        <Form.Label>Username</Form.Label>
        <Form.Control
          onChange={(e) => setUsername(e.target.value)}
          className="app-form-input"
          ref={usernameRef}
          type="text"
          placeholder="Enter username"
        />
      </Form.Group>
      <Form.Group className="mb-3">
        <Form.Label>Password</Form.Label>
        <Form.Control
          onChange={(e) => setPassword(e.target.value)}
          className="app-form-input"
          type="password"
          placeholder="Password"
        />
        <div ref={errorRef} className={error ? "app-form-error" : "hidden"}>
          {error}
        </div>
      </Form.Group>
      {!loading && (
        <Button className="btn-block-primary" type="submit">
          Login
        </Button>
      )}
      {loading && (
        <Button className="btn-block-primary" disabled>
          <Spinner animation="border" />
        </Button>
      )}
    </Form>
  );
};

export default Login;
