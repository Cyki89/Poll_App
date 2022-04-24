import { Outlet, useLocation, Link } from "react-router-dom";
import Breadcrumb from "react-bootstrap/Breadcrumb";

const generatePathList = (path) => {
  const pathLabels = [
    "Home",
    "Questionnaire List",
    "Questionnaire Details",
    "Question Details",
  ];

  const splited = path.split("/");
  const paths = [];
  for (let i = 0; i < splited.length; i++) {
    paths.push([pathLabels[i], splited.slice(0, i + 1).join("/") || "/"]);
  }

  return paths;
};

const AdminPanel = () => {
  const location = useLocation();
  const pathList = generatePathList(location.pathname);

  return (
    <div className="admin-panel-container">
      {/* <h1 className="admin-panel-title">{JSON.stringify(location.pathname)}</h1> */}
      <Breadcrumb>
        {pathList.map((path, idx) => (
          <Breadcrumb.Item
            className="breadcrumb-item"
            key={path}
            linkAs={Link}
            linkProps={{ to: path[1] }}
            active={idx === pathList.length - 1}>
            {path[0]}
          </Breadcrumb.Item>
        ))}
      </Breadcrumb>
      <Outlet />
    </div>
  );
};

export default AdminPanel;
