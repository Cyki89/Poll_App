import { useRef, useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";

import useAxiosFunction from "../../hooks/useAxiosFunction";
import useAxiosPrivate from "../../hooks/useAxiosPrivate";

import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";

import LoadingScreen from "../LoadingScreen";
import { toast } from "react-toastify";

const QUESTIONNAIRES_ENDPOINT = "/poll/questionnaires/";
const QUESTIONNAIRES_URL = "/questionnaires";

const setResponseError = (error) => {
  if (!error.response) return "Server problem. Please try again in a minute.";
  if ("name" in error.response.data)
    return "Questionnaire title is required and have to be unique";
  return "Unknown problem. Try again";
};

const AdminAddQuestionnary = () => {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  const nameRef = useRef();
  const errorRef = useRef();

  const [redirect, setRedirect] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  const axiosPrivate = useAxiosPrivate();
  const { response, error, loading, clearResponse, clearError, axiosFetch } =
    useAxiosFunction();

  const handleSubmit = (e) => {
    e.preventDefault();
    setRedirect(false);

    axiosFetch({
      axiosInstance: axiosPrivate,
      method: "POST",
      url: QUESTIONNAIRES_ENDPOINT,
      setResponseError: setResponseError,
      requestConfig: { name },
    });
  };

  const handleSubmitWithRedirect = (e) => {
    handleSubmit(e);
    setRedirect(true);
  };

  const handleBackRedirect = (e) => {
    const from = location.state?.from || QUESTIONNAIRES_URL;
    navigate(from, { replace: true });
  };

  const showSuccessNotification = () => {
    toast.success(`Questionnary ${name} was successfully added.`, {
      position: "top-right",
      autoClose: 5000,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "dark",
    });
  };

  useEffect(() => {
    nameRef.current.focus();
  }, []);

  useEffect(() => {
    clearError();
    // eslint-disable-next-line
  }, [name, description]);

  useEffect(() => {
    if (error || loading || !response) return;

    showSuccessNotification();
    clearResponse();
    setName("");
    setDescription("");

    if (redirect === true) navigate(QUESTIONNAIRES_URL, { replace: true });
    // eslint-disable-next-line
  }, [response, loading, error, redirect]);

  return (
    <>
      {loading && <LoadingScreen />}
      {!loading && (
        <Form className="admin-panel-form">
          <h1 className="app-form-header">Add Questionnaire</h1>
          <Form.Group className="mb-3">
            <Form.Label>Title</Form.Label>
            <Form.Control
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="admin-panel-input"
              ref={nameRef}
              type="text"
              placeholder="Questionnary Name"
            />
          </Form.Group>
          <Form.Group className="mb-3">
            <Form.Label>Description</Form.Label>
            <Form.Control
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="admin-panel-input"
              placeholder="Questionnary Description"
              as="textarea"
              rows={3}
            />
            <div ref={errorRef} className={error ? "app-form-error" : "hidden"}>
              {error}
            </div>
          </Form.Group>
          <div className="admin-panel-btn-container">
            <Button
              className="admin-panel-btn"
              type="submit"
              onClick={handleSubmitWithRedirect}>
              Add New
            </Button>
            <Button
              className="admin-panel-btn"
              type="submit"
              onClick={handleSubmit}>
              Add and Continue
            </Button>
            <Button
              className="admin-panel-btn btn-secondary"
              type="button"
              onClick={handleBackRedirect}>
              Back
            </Button>
          </div>
        </Form>
      )}
    </>
  );
};

export default AdminAddQuestionnary;
