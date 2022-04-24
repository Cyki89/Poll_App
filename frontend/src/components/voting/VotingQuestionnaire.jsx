import { useParams, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";

import useAuth from "../../hooks/useAuth";

import useAxiosFunction from "../../hooks/useAxiosFunction";
import useAxiosPrivate from "../../hooks/useAxiosPrivate";

import { toast } from "react-toastify";

import LoadingScreen from "../LoadingScreen";
import ErrorScreen from "../ErrorScreen";
import VotingQuestion from "./VotingQuestion";
import Button from "react-bootstrap/Button";
import BackButton from "../BackButton";

const VOTING_ENDPOINT = "/poll/voting/";
const VOTING_URL = "/voting";
const QUESTIONNAIRES_ENDPOINT = "/poll/questionnaires";

const setResponseError = (err) => err.message;

const VotingQuestionnaire = () => {
  const { user } = useAuth();
  const { id } = useParams();
  const navigate = useNavigate();

  const [data, setData] = useState();
  const [selected, setSelected] = useState([]);

  const axiosPrivate = useAxiosPrivate();
  const { response, error, status, clearError, loading, axiosFetch } =
    useAxiosFunction();

  const getData = () => {
    axiosFetch({
      axiosInstance: axiosPrivate,
      method: "GET",
      url: `${QUESTIONNAIRES_ENDPOINT}/${id}/`,
      setResponseError: setResponseError,
    });
  };

  const handleCheckAnswer = (prevId, currId) => {
    setSelected((prev) => [...prev.filter((id) => id !== prevId), currId]);
  };

  const showSuccessNotification = () => {
    toast.success(`Questionnaire was successfully submited.`, {
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

  const onSubmit = async (e) => {
    await axiosFetch({
      axiosInstance: axiosPrivate,
      method: "POST",
      url: VOTING_ENDPOINT,
      setResponseError: setResponseError,
      requestConfig: {
        questionnaire_id: id,
        user_id: user.user_id,
        answers: selected,
      },
    });
  };

  useEffect(() => {
    getData();
    // eslint-disable-next-line
  }, []);

  useEffect(() => {
    clearError();
    // eslint-disable-next-line
  }, [selected]);

  useEffect(() => {
    if (!status) return;
    if (status === 204) {
      showSuccessNotification();
      navigate(VOTING_URL, { replace: true });
    }
    // eslint-disable-next-line
  }, [status, navigate]);

  useEffect(() => {
    if (!response) return;

    setData(response);
  }, [response]);

  return (
    <>
      {loading && <LoadingScreen />}

      {!loading && !response && error && (
        <ErrorScreen>
          Some error occurr durring fetching data.
          <br />
          Please try again in a minute.
        </ErrorScreen>
      )}

      {!loading && data && (
        <div className="voting-quetionnaire-container mb-3">
          <div className="voting-quetionnaire-header mb-2">
            {data.name} / {data.date_added}
          </div>
          <div className="voting-quetionnaire-description mb-4">
            {data.description}
          </div>
          <div className={error ? "voting-error-box mb-4" : "hidden"}>
            {error}
          </div>
          {data.questions &&
            data.questions.map((question, idx) => (
              <VotingQuestion
                key={idx}
                selectedList={selected}
                question={question.text}
                answers={question.answers}
                onCheck={handleCheckAnswer}
              />
            ))}

          <Button
            type="submit"
            onClick={onSubmit}
            className="btn-primary btn-rounded btn-block my-3"
            disabled={selected.length < data.questions.length}>
            Submit Questionnaire
          </Button>
          <BackButton className="btn-block" />
        </div>
      )}

      {!loading && !error && !data && <div>No Questions Was Found</div>}
    </>
  );
};

export default VotingQuestionnaire;
