import React from "react";
import { Routes, Route } from "react-router-dom";
import Layout from "./Layout";
import Login from "./Login";
import Unauthorized from "./Unauthorized";
import Home from "./Home";
import PersistLogin from "./PersistLogin";
import ProtectedRoute from "./ProtectedRoute";
import AdminPanel from "./admin_panel/AdminPanel";
import AdminQuestionnaires from "./admin_panel/AdminQuestionnaires";
import AdminQuestionnaireOutlet from "./admin_panel/AdminQuestionnaireOutlet";
import AdminQuestionnaireDetails from "./admin_panel/AdminQuestionnaireDetails";
import Missing from "./Missing";
import AdminAddQuestionnary from "./admin_panel/AdminAddQuestionnary";
import AdminNewQuestion from "./admin_panel/AdminNewQuestion";
import AdminEditQuestion from "./admin_panel/AdminEditQuestion";
import VotingPanel from "./voting/VotingPanel";
import VotingList from "./voting/VotingList";
import VotingQuestion from "./voting/VotingQuestion";
import VotingQuestionnaire from "./voting/VotingQuestionnaire";
import StatisticsQuestion from "./StatisticsQuestion";

const GROUPS = {
  Admins: "Admins",
};

const AppRouter = () => {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route path="login" element={<Login />} />
        <Route path="unauthorized" element={<Unauthorized />} />
        <Route element={<PersistLogin />}>
          <Route element={<ProtectedRoute />}>
            <Route path="/" element={<Home />} />
          </Route>

          <Route element={<ProtectedRoute allowedGroups={[GROUPS.Admins]} />}>
            <Route path="questionnaires" element={<AdminPanel />}>
              <Route path="" element={<AdminQuestionnaires />} />
              <Route path="new" element={<AdminAddQuestionnary />} />
              <Route path=":id" element={<AdminQuestionnaireOutlet />}>
                <Route path="" element={<AdminQuestionnaireDetails />} />
                <Route path="new" element={<AdminNewQuestion />} />
                <Route path=":question_id" element={<AdminEditQuestion />} />
              </Route>
            </Route>
          </Route>

          <Route element={<ProtectedRoute allowedGroups={[]} />}>
            <Route path="voting" element={<VotingPanel />}>
              <Route path="" element={<VotingList />} />
              <Route path=":id" element={<VotingQuestionnaire />} />
              <Route path="question" element={<VotingQuestion />} />
            </Route>
          </Route>

          <Route element={<ProtectedRoute allowedGroups={[GROUPS.Admins]} />}>
            <Route
              path="statistics/:id/:question_id"
              element={<StatisticsQuestion />}
            />
          </Route>
        </Route>

        <Route path="*" element={<Missing />} />
      </Route>
    </Routes>
  );
};

export default AppRouter;
