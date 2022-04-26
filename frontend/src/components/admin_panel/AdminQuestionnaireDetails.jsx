import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";

import useAxiosFunction from "../../hooks/useAxiosFunction";
import useAxiosPrivate from "../../hooks/useAxiosPrivate";

import Tooltip from "react-bootstrap/Tooltip";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import Alert from "react-bootstrap/Alert";
import Button from "react-bootstrap/Button";
import LoadingScreen from "../LoadingScreen";
import ErrorScreen from "../ErrorScreen";
import Table from "../Table";

import AdminQuestionnaireDetailsForm from "./AdminQuestionnaireDetailsForm";

const QUESTIONNAIRES_ENDPOINT = "/poll/questionnaires";
const STATISTIC_QUESTION_URL = "/statistics";

const setResponseError = (error) => {
  if (!error.response) return "Server problem. Please try again in a minute.";
  if ("name" in error.response.data)
    return "Questionnaire title is required and have to be unique";
  return "Unknown problem. Try again";
};

const AdminQuestionnaireDetails = () => {
  const { id } = useParams();
  const [data, setData] = useState();
  const [submited, setSubmited] = useState(false);

  const axiosPrivate = useAxiosPrivate();
  const { response, error, clearError, loading, axiosFetch } =
    useAxiosFunction();

  const getData = () => {
    axiosFetch({
      axiosInstance: axiosPrivate,
      method: "GET",
      url: `${QUESTIONNAIRES_ENDPOINT}/${id}/`,
      setResponseError: setResponseError,
    });
  };

  const showSuccessNotification = () => {
    toast.success(`Questionnary details was successfully updated.`, {
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

  const handleUpdateData = async (e, requestConfig) => {
    e.preventDefault();

    axiosFetch({
      axiosInstance: axiosPrivate,
      method: "PATCH",
      url: `${QUESTIONNAIRES_ENDPOINT}/${id}/`,
      setResponseError: setResponseError,
      requestConfig,
    });
    setSubmited(true);
  };

  useEffect(() => {
    getData();
    // eslint-disable-next-line
  }, []);

  useEffect(() => {
    clearError();
    // eslint-disable-next-line
  }, [data]);

  useEffect(() => {
    if (!loading && response && !error) setData(response);
    if (!loading && response && !error && submited) {
      showSuccessNotification();
      setSubmited(false);
    }
    // eslint-disable-next-line
  }, [response, submited, loading]);

  const columns = [
    {
      label: "Question Idx",
      path: "name",
      content: (question, idx) => (
        <Link to={`${question.id}`}>{`Question ${idx + 1}`}</Link>
      ),
    },
    {
      label: "Added",
      path: "date_added",
    },
    {
      label: "Text",
      path: "text",
      content: (question) => (
        <OverlayTrigger
          placement={"bottom"}
          overlay={
            <Tooltip>
              <strong>{question.text}</strong>
            </Tooltip>
          }>
          <Button className="btn-anchor">Show</Button>
        </OverlayTrigger>
      ),
    },

    {
      label: "Options",
      path: "answers",
      content: (question) => question.answers.length,
    },
    {
      label: "Answers",
      path: "questions",
      content: (question) => (
        <Link to={`${STATISTIC_QUESTION_URL}/${id}/${question.id}`}>
          Statistics
        </Link>
      ),
    },
    {
      label: "Votes",
      path: "votes_count",
      content: (question) => question.votes_count,
    },
  ];

  return (
    <>
      {loading && <LoadingScreen />}

      {!loading && !data && error && (
        <ErrorScreen>
          Serwer Error.
          <br />
          Please try again in a minute.
        </ErrorScreen>
      )}

      {!loading && data && (
        <div className="admin-panel-grid">
          {error && (
            <Alert variant="danger" className="admin-panel-grid-alert">
              {error}
            </Alert>
          )}
          <AdminQuestionnaireDetailsForm
            data={data}
            setData={setData}
            onSubmit={handleUpdateData}
            clearError={clearError}
          />
          <div className="align-center">
            <h1 className="app-form-header">Questions</h1>
            <div className="admin-panel-question-table-container mt-4">
              <Table
                data={data.questions}
                columns={columns}
                className="center"
              />
            </div>
            <Link to="new">
              <Button
                type="submit"
                className="admin-panel-btn btn-block fg-white mt-3">
                Add New Question
              </Button>
            </Link>
          </div>
        </div>
      )}

      {!loading && !error && !data && <div>No Data</div>}
    </>
  );
};

export default AdminQuestionnaireDetails;
