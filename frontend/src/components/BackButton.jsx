import { useNavigate } from "react-router-dom";
import Button from "react-bootstrap/Button";

const BackButton = ({ className = "" }) => {
  const navigate = useNavigate();
  return (
    <Button
      className={"admin-panel-btn bg-red " + className}
      onClick={() => navigate(-1)}>
      Go Back
    </Button>
  );
};

export default BackButton;
