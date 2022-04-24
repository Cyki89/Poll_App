import Button from "react-bootstrap/Button";
import { useNavigate } from "react-router-dom";

const AdminAddItemGroup = ({ itemName }) => {
  const navigate = useNavigate();
  return (
    <div className="admin-panel-toolbar-item">
      <Button
        className="admin-panel-btn btn-block"
        onClick={() => navigate("new")}>
        {`Add ${itemName} +`}
      </Button>
    </div>
  );
};

export default AdminAddItemGroup;
