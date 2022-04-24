import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

import useAxiosFunction from "../../hooks/useAxiosFunction";
import useAxiosPrivate from "../../hooks/useAxiosPrivate";

import LoadingScreen from "../LoadingScreen";
import ErrorScreen from "../ErrorScreen";
import Table from "../Table";
import Paginations from "../Paginations";

import iconYes from "../../icon-yes.svg";
import iconNo from "../../icon-no.svg";

const VOTING_ENDPOINT = "/poll/voting";
const PAGE_LIMIT = 10;

const setResponseError = (err) => {
  return err.message;
};

const VotingList = () => {
  const axiosPrivate = useAxiosPrivate();
  const { response, error, loading, axiosFetch } = useAxiosFunction();

  const [questionnaires, setQuestionnaires] = useState([]);

  const [sortOrder, setSortOrder] = useState("");
  const [sortColumn, setSortColumn] = useState("");

  const [currPage, setCurrPage] = useState(1);
  const [lastPage, setLastPage] = useState(0);

  const getData = () => {
    const ordering = `${sortOrder === "asc" ? "" : "-"}${sortColumn}`;

    let url = `${VOTING_ENDPOINT}/`;
    url += `?offset=${(currPage - 1) * PAGE_LIMIT}`;
    url += `&limit=${PAGE_LIMIT}`;
    url += `&ordering=${ordering}`;

    axiosFetch({
      axiosInstance: axiosPrivate,
      method: "GET",
      url: url,
      setResponseError: setResponseError,
    });
  };

  useEffect(() => {
    getData();
    setLastPage(0);
    // eslint-disable-next-line
  }, [sortOrder, sortColumn, currPage]);

  useEffect(() => {
    if (response) {
      setQuestionnaires(response.results);

      const lastPageCalculated = Math.ceil(response.count / PAGE_LIMIT);
      setLastPage(
        lastPageCalculated < currPage ? currPage : lastPageCalculated
      );
    }
  }, [response, currPage]);

  const handleSort = (colPath) => {
    if (colPath === sortColumn) {
      setSortOrder(() => (sortOrder === "asc" ? "desc" : "asc"));
      return;
    }
    setSortColumn(colPath);
    setSortOrder("asc");
    setCurrPage(1);
  };

  const handlePageChange = (page) => setCurrPage(page);

  const columns = [
    {
      label: "Title",
      path: "name",
      content: (questionnaire) => (
        <Link to={`${questionnaire.id}`}>{questionnaire.name}</Link>
      ),
      sortable: true,
    },
    {
      label: "Added",
      path: "date_added",
      sortable: true,
    },
    {
      label: "Questions",
      path: "questions",
      content: (questionnaire) =>
        JSON.stringify(questionnaire.questions.length),
    },
    {
      label: "Votes",
      path: "users",
      content: (questionnaire) => JSON.stringify(questionnaire.users.length),
    },

    {
      label: "Active",
      path: "is_active",
      content: (questionnaire) => (
        <img
          src={questionnaire.is_active ? iconYes : iconNo}
          width="15"
          height="15"
          alt=""
        />
      ),
    },
  ];

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

      {!loading && !error && questionnaires && lastPage !== 0 && (
        <>
          <h1 className="voting-title m-3">Available Votings</h1>
          <Table
            data={questionnaires}
            columns={columns}
            sortOrder={sortOrder}
            sortColumn={sortColumn}
            onSort={handleSort}
          />
          <Paginations
            currentPage={currPage}
            lastPage={lastPage}
            onChange={handlePageChange}
          />
        </>
      )}

      {!loading && !error && !questionnaires && <div>No Data</div>}
    </>
  );
};

export default VotingList;
