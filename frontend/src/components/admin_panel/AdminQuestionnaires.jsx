import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

import useAxiosFunction from "../../hooks/useAxiosFunction";
import useAxiosPrivate from "../../hooks/useAxiosPrivate";

import FormCheck from "react-bootstrap/FormCheck";
import LoadingScreen from "../LoadingScreen";
import ErrorScreen from "../ErrorScreen";
import AdminPanelToolbar from "./AdminPanelToolbar";
import Table from "../Table";
import Paginations from "../Paginations";

import iconYes from "../../icon-yes.svg";
import iconNo from "../../icon-no.svg";
import { ReactComponent as CopyBtn } from "../../copy.svg";

import { toast } from "react-toastify";

const QUESTIONNAIRES_ENDPOINT = "/poll/questionnaires";
const DOMAIN_VOTING_URL = "http://localhost:3000/voting";
const PAGE_LIMIT = 10;

const setResponseError = (err) => {
  return err.message;
};

const TOAST_CONTAINER = {
  position: "top-right",
  autoClose: 5000,
  hideProgressBar: false,
  closeOnClick: true,
  pauseOnHover: true,
  draggable: true,
  progress: undefined,
  theme: "dark",
};

const showSuccessNotification = (txt) => {
  toast.success(txt, TOAST_CONTAINER);
};

const showErrorNotification = (txt) => {
  toast.error(txt, TOAST_CONTAINER);
};

const copyToClipboard = (questionnaire) => {
  if (!questionnaire.is_active)
    return showErrorNotification("Voting is no longer active");

  if (questionnaire.questions.length === 0)
    return showErrorNotification("Questionnaire don't have any questions");

  navigator.clipboard.writeText(`${DOMAIN_VOTING_URL}/${questionnaire.id}`);
  showSuccessNotification("Link To Voting Was Successfull Copied");
};

const AdminQuestionnaires = () => {
  const axiosPrivate = useAxiosPrivate();
  const { response, error, loading, axiosFetch } = useAxiosFunction();

  const [questionnaires, setQuestionnaires] = useState([]);
  const [selected, setSelected] = useState([]);

  const [sortOrder, setSortOrder] = useState("");
  const [sortColumn, setSortColumn] = useState("");

  const [search, setSearch] = useState("");

  const [currPage, setCurrPage] = useState(1);
  const [lastPage, setLastPage] = useState(0);

  const getData = () => {
    const orderingColumn =
      sortColumn === "answers" || sortColumn === "questions"
        ? `${sortColumn}_count`
        : sortColumn;
    const ordering = `${sortOrder === "asc" ? "" : "-"}${orderingColumn}`;

    let url = `${QUESTIONNAIRES_ENDPOINT}/`;
    url += `?offset=${(currPage - 1) * PAGE_LIMIT}`;
    url += `&limit=${PAGE_LIMIT}`;
    url += `&ordering=${ordering}}`;
    url += `&search=${search}`;

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
  }, [sortOrder, sortColumn, search, currPage]);

  useEffect(() => {
    if (response) {
      setQuestionnaires(response.results);

      const lastPageCalculated = Math.ceil(response.count / PAGE_LIMIT);
      setLastPage(
        lastPageCalculated < currPage ? currPage : lastPageCalculated
      );
    }
    // eslint-disable-next-line
  }, [response]);

  const handleAction = async (e, actionType) => {
    await axiosFetch({
      axiosInstance: axiosPrivate,
      method: "POST",
      url: `${QUESTIONNAIRES_ENDPOINT}/${actionType}/`,
      setResponseError: setResponseError,
      requestConfig: { questionnaires: selected },
    });

    setSelected([]);
    getData();

    showSuccessNotification("Action was successfully performed.");
  };

  const handleSort = (colPath) => {
    if (colPath === sortColumn) {
      setSortOrder(() => (sortOrder === "asc" ? "desc" : "asc"));
      return;
    }
    setSortColumn(colPath);
    setSortOrder("asc");
    setCurrPage(1);
  };

  const handleSearch = (searchValue) => {
    setSearch(searchValue);
    setCurrPage(1);
  };

  const handlePageChange = (page) => setCurrPage(page);

  const handleCheckboxChange = (e, id) => {
    if (selected.includes(id)) {
      setSelected((prev) => prev.filter((selected_id) => selected_id !== id));
      return;
    }

    setSelected((prev) => [...prev, id]);
  };

  const columns = [
    {
      label: "Check",
      content: (questionnaire) => (
        <FormCheck
          onChange={(e) => handleCheckboxChange(e, questionnaire.id)}
        />
      ),
    },
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
      sortable: true,
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
    {
      label: "Votes",
      path: "answers",
      content: (questionnaire) => JSON.stringify(questionnaire.users.length),
      sortable: true,
    },
    {
      label: "Poll Link",
      path: "link",
      content: (questionnaire) => (
        <CopyBtn
          className="copy-btn"
          onClick={() => copyToClipboard(questionnaire)}
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
          <AdminPanelToolbar
            itemName="Questionnaire"
            subTitle="Questionnaire List"
            onAction={handleAction}
            search={search}
            onSearch={handleSearch}
          />
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

export default AdminQuestionnaires;
