import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import LoadingScreen from "./LoadingScreen";
import ErrorScreen from "./ErrorScreen";

import { axiosPrivate } from "../api/axios";
import useAxios from "./../hooks/useAxios";

import BarChart from "./BarChart";
import BackButton from "./BackButton";

const QUESTIONNAIRES_ENDPOINT = "/poll/questionnaires";

const StatisticsQuestion = () => {
  const { id, question_id } = useParams();
  const [QUESTION_ENDPOINT] = useState(
    () => `${QUESTIONNAIRES_ENDPOINT}/${id}/questions/${question_id}/`
  );

  const [response, error, loading] = useAxios({
    axiosInstance: axiosPrivate,
    method: "GET",
    url: QUESTION_ENDPOINT,
  });

  const [barChartData, setBarChartData] = useState();

  useEffect(() => {
    if (loading || error || !response) return;
    const answers = response.answers;
    const labels = answers.map((answer) => answer.text);
    const count = answers.map((answer) => answer.count);

    setBarChartData({
      labels: labels,
      values: count,
      title: "Answers",
    });
  }, [response, loading, error]);

  return (
    <>
      {loading && <LoadingScreen />}

      {!loading && error && (
        <ErrorScreen>
          Some error occurr durring fetching data.
          <br />
          Please try again in a minute.
        </ErrorScreen>
      )}

      {!loading && !error && barChartData && (
        <div className="statistics-chart-container">
          <div className="statistics-chart-header">{response.text}</div>
          <BarChart resData={barChartData} />
          <BackButton />
        </div>
      )}

      {!loading && !error && !barChartData && <div>No Data</div>}
    </>
  );
};

export default StatisticsQuestion;
