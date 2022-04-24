import { useRef, useState, useEffect } from "react";
import { useNavigate, useLocation, useParams } from "react-router-dom";

import useAxiosFunction from "../../hooks/useAxiosFunction";
import useAxiosPrivate from "../../hooks/useAxiosPrivate";

import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import AdminAnswerCard from "./AdminAnswerCard";

import AdminFormAnswerModal from "./AdminFormAnswerModal";
import AdminDeleteAnswerModal from "./AdminDeleteAnswerModal";
import AdminDeleteQuestionModal from "./AdminDeleteQuestionModal";

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

const AdminEditQuestion = () => {
  const [text, setText] = useState("");

  const [answers, setAnswers] = useState([]);
  const [currentAnswerIdx, setCurrentAnswerIdx] = useState();

  const [submitted, setSubmitted] = useState(false);

  const textRef = useRef();

  const formAnswerModalRef = useRef();
  const deleteAnswerModalRef = useRef();
  const deleteQuestionModalRef = useRef();

  const { id, question_id } = useParams();
  const [QUESTION_ENDPOINT] = useState(
    () => `${QUESTIONNAIRES_ENDPOINT}/${id}/questions/${question_id}/`
  );
  const [QUESTIONNARY_DETAILS_URL] = useState(
    () => `${QUESTIONNAIRES_URL}/${id}`
  );

  const location = useLocation();
  const navigate = useNavigate();

  const axiosPrivate = useAxiosPrivate();
  const { response, error, loading, clearError, axiosFetch } =
    useAxiosFunction();

  const openAnswerModal = (idx = null, text = null) => {
    setCurrentAnswerIdx(idx);

    formAnswerModalRef.current.setText(text);
    formAnswerModalRef.current.openModal();
  };

  const openDeleteAnswerModal = (idx, text) => {
    setCurrentAnswerIdx(idx);

    deleteAnswerModalRef.current.setText(text);
    deleteAnswerModalRef.current.openModal();
  };

  const openDeleteQuestionModal = () => {
    deleteQuestionModalRef.current.openModal();
  };

  const handleAddAnswer = (text) => {
    if (currentAnswerIdx == null)
      return setAnswers((prev) => [...prev, { text, state: "new" }]);

    setAnswers((prev) => [
      ...prev.slice(0, currentAnswerIdx),
      { ...prev[currentAnswerIdx], text, state: "edited" },
      ...prev.slice(currentAnswerIdx + 1),
    ]);
  };

  const handleDeleteAnswer = () => {
    if (
      response.answers
        .map((answer) => answer.id)
        .includes(answers[currentAnswerIdx].id)
    )
      return setAnswers((prev) => [
        ...prev.slice(0, currentAnswerIdx),
        { ...prev[currentAnswerIdx], state: "deleted" },
        ...prev.slice(currentAnswerIdx + 1),
      ]);

    setAnswers((prev) => [
      ...prev.slice(0, currentAnswerIdx),
      ...prev.slice(currentAnswerIdx + 1),
    ]);
  };

  const getData = () => {
    axiosFetch({
      axiosInstance: axiosPrivate,
      method: "GET",
      url: QUESTION_ENDPOINT,
      setResponseError: setResponseError,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const requestObj = { text };

    const answersArr = [];
    for (const answer of answers) {
      if (answer.state) answersArr.push(answer);
    }

    if (answersArr.length > 0) requestObj["answers"] = answersArr;

    setSubmitted(false);
    await axiosFetch({
      axiosInstance: axiosPrivate,
      method: "PATCH",
      url: QUESTION_ENDPOINT,
      setResponseError: setResponseError,
      requestConfig: requestObj,
    });
    setSubmitted(true);
  };

  const handleDelete = async () => {
    setSubmitted(false);
    await axiosFetch({
      axiosInstance: axiosPrivate,
      method: "DELETE",
      url: QUESTION_ENDPOINT,
      setResponseError: setResponseError,
    });
    setSubmitted(true);
  };

  const handleBackRedirect = (e) => {
    const from = location.state?.from || QUESTIONNARY_DETAILS_URL;
    navigate(from, { replace: true });
  };

  const showSuccessNotification = () => {
    toast.success("Question was successfully edited.", {
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
    getData();
    // eslint-disable-next-line
  }, []);

  useEffect(() => {
    if (error || loading || !submitted) return;

    showSuccessNotification();

    navigate(QUESTIONNARY_DETAILS_URL, { replace: true });
    // eslint-disable-next-line
  }, [response, loading, error, submitted]);

  useEffect(() => {
    if (!response) return;

    setText(response.text);
    setAnswers(response.answers);
    textRef.current.focus();
  }, [response]);

  useEffect(() => {
    setSubmitted(false);
    clearError();
    // eslint-disable-next-line
  }, [text, answers]);

  return (
    <>
      {loading && <LoadingScreen />}
      {!loading && (
        <Form className="admin-panel-form">
          <div className="relative-container">
            <h2 className="admin-panel-form-header text-center">
              Edit Question
            </h2>
            <Button
              className="admin-panel-btn btn-del"
              type="button"
              onClick={openDeleteQuestionModal}>
              X
            </Button>
          </div>
          <Form.Group className="mb-4">
            <Form.Control
              value={text}
              onChange={(e) => setText(e.target.value)}
              className="admin-panel-input"
              ref={textRef}
              placeholder="Enter Question"
              as="textarea"
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
            <div className="admin-panel-btn-container">
              <Button
                className="admin-panel-btn m-2"
                type="submit"
                onClick={handleSubmit}>
                Update Data
              </Button>
              <Button
                className="admin-panel-btn btn-secondary m-2"
                type="button"
                onClick={handleBackRedirect}>
                Go Back
              </Button>
            </div>
          </Form.Group>
        </Form>
      )}
      <AdminDeleteQuestionModal
        ref={deleteQuestionModalRef}
        onSubmit={handleDelete}
      />

      <AdminFormAnswerModal
        ref={formAnswerModalRef}
        onSubmit={handleAddAnswer}
      />
      <AdminDeleteAnswerModal
        ref={deleteAnswerModalRef}
        onSubmit={handleDeleteAnswer}
      />
    </>
  );
};

export default AdminEditQuestion;
