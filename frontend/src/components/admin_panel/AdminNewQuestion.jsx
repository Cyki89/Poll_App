import { useRef, useState, useEffect } from "react";
import { useNavigate, useLocation, useParams } from "react-router-dom";

import useAxiosFunction from "../../hooks/useAxiosFunction";
import useAxiosPrivate from "../../hooks/useAxiosPrivate";

import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import AdminAnswerCard from "./AdminAnswerCard";

import AdminFormAnswerModal from "./AdminFormAnswerModal";
import AdminDeleteAnswerModal from "./AdminDeleteAnswerModal";

import LoadingScreen from "./../LoadingScreen";
import { toast } from "react-toastify";

const QUESTIONNAIRES_ENDPOINT = "/poll/questionnaires";
const QUESTIONNAIRES_URL = "/questionnaires";

const setResponseError = (error) => {
  if (!error.response) return "Server problem. Please try again in a minute.";
  if ("text" in error.response.data) return "Question body is required.";
  if ("answers" in error.response.data)
    return "At least 2 answers are required.";
  return "Unknown problem. Try again";
};

const AdminNewQuestion = () => {
  const [text, setText] = useState("");

  const [answers, setAnswers] = useState([]);
  const [currentAnswerIdx, setCurrentAnswerIdx] = useState();

  const textRef = useRef();

  const addAnswerModalRef = useRef();
  const deleteAnswerModalRef = useRef();

  const { id } = useParams();
  const [QUESTIONNARY_DETAILS_ENDPOINT] = useState(
    () => `${QUESTIONNAIRES_ENDPOINT}/${id}/questions/`
  );
  const [QUESTIONNARY_DETAILS_URL] = useState(
    () => `${QUESTIONNAIRES_URL}/${id}`
  );

  const [redirect, setRedirect] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  const axiosPrivate = useAxiosPrivate();
  const { response, error, loading, clearResponse, clearError, axiosFetch } =
    useAxiosFunction();

  const openAnswerModal = (idx = null, text = null) => {
    setCurrentAnswerIdx(idx);

    addAnswerModalRef.current.setText(text);
    addAnswerModalRef.current.openModal();
  };

  const openDeleteAnswerModal = (idx, text) => {
    setCurrentAnswerIdx(idx);

    deleteAnswerModalRef.current.setText(text);
    deleteAnswerModalRef.current.openModal();
  };

  const handleAddAnswer = (text) => {
    if (currentAnswerIdx == null)
      return setAnswers((prev) => [...prev, { text }]);

    setAnswers((prev) => [
      ...prev.slice(0, currentAnswerIdx),
      { text },
      ...prev.slice(currentAnswerIdx + 1),
    ]);
  };

  const handleDeleteAnswer = () => {
    setAnswers((prev) => [
      ...prev.slice(0, currentAnswerIdx),
      ...prev.slice(currentAnswerIdx + 1),
    ]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    setRedirect(false);

    axiosFetch({
      axiosInstance: axiosPrivate,
      method: "POST",
      url: QUESTIONNARY_DETAILS_ENDPOINT,
      setResponseError: setResponseError,
      requestConfig: { text, answers },
    });
  };

  const handleSubmitWithRedirect = (e) => {
    handleSubmit(e);
    setRedirect(true);
  };

  const handleBackRedirect = (e) => {
    const from = location.state?.from || QUESTIONNARY_DETAILS_URL;
    navigate(from, { replace: true });
  };

  const showSuccessNotification = () => {
    toast.success("Question was successfully added.", {
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
    textRef.current.focus();
  }, []);

  useEffect(() => {
    clearError();
    // eslint-disable-next-line
  }, [text, answers]);

  useEffect(() => {
    if (error || loading || !response) return;

    showSuccessNotification();
    clearResponse();
    setText("");
    setAnswers([]);

    if (redirect === true)
      navigate(QUESTIONNARY_DETAILS_URL, { replace: true });
    // eslint-disable-next-line
  }, [response, loading, error, redirect]);

  return (
    <>
      {loading && <LoadingScreen />}
      {!loading && (
        <Form className="admin-panel-form">
          <h2 className="admin-panel-form-header text-center">Add Question</h2>
          <Form.Group className="mb-4">
            <Form.Control
              value={text}
              onChange={(e) => setText(e.target.value)}
              className="fg-secondary admin-panel-input"
              placeholder="Enter Question"
              as="textarea"
              ref={textRef}
              rows={2}
            />
            <div className={error ? "app-form-error" : "hidden"}>{error}</div>
          </Form.Group>
          <Form.Group>
            <div className="relative-container">
              <h2 className="admin-panel-form-header text-center">Answers</h2>
              <Button
                className="admin-panel-btn btn-add"
                variant="none"
                type="button"
                onClick={(e) => openAnswerModal()}>
                +
              </Button>
            </div>
            <div className="admin-panel-card-container">
              {answers.map((answer, idx) =>
                answer.state === "deleted" ? null : (
                  <AdminAnswerCard
                    key={idx}
                    idx={idx}
                    answer={answer}
                    openAnswerModal={openAnswerModal}
                    openDeleteAnswerModal={openDeleteAnswerModal}
                  />
                )
              )}
            </div>
            <div className="admin-panel-btn-container mt-4">
              <Button
                className="flex-grow-1 admin-panel-btn"
                type="submit"
                onClick={handleSubmitWithRedirect}>
                Add New
              </Button>
              <Button
                className="flex-grow-1 admin-panel-btn"
                type="submit"
                onClick={handleSubmit}>
                Add and Continue
              </Button>
              <Button
                className="flex-grow-1 admin-panel-btn btn-secondary"
                type="button"
                onClick={handleBackRedirect}>
                Go Back
              </Button>
            </div>
          </Form.Group>
        </Form>
      )}

      <AdminFormAnswerModal
        ref={addAnswerModalRef}
        onSubmit={handleAddAnswer}
      />
      <AdminDeleteAnswerModal
        ref={deleteAnswerModalRef}
        onSubmit={handleDeleteAnswer}
      />
    </>
  );
};

export default AdminNewQuestion;
