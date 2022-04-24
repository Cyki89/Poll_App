import { Outlet } from "react-router-dom";

const VotingPanel = () => {
  return (
    <div className="voting-container">
      <Outlet />
    </div>
  );
};

export default VotingPanel;
