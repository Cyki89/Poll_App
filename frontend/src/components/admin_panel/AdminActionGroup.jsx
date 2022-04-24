import { useState } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";

const AdminActionGroup = ({ onAction }) => {
  const [action, setAction] = useState("");

  const handleActionChange = (e) => {
    setAction(e.target.value);
  };

  const handleSubmit = (e) => {
    if (action === "") return;
    e.preventDefault();
    onAction(e, action);
  };

  return (
    <Form className="admin-panel-toolbar-item" onSubmit={handleSubmit}>
      <Form.Select className="admin-panel-input" onChange={handleActionChange}>
        <option value="">Select Action</option>
        <option value="delete">Delete Questionnaires</option>
        <option value="activate">Make Questionnaires Active</option>
        <option value="deactivate">Make Questionnaires Inactive</option>
      </Form.Select>
      <Button className="admin-panel-btn" type="submit">
        Go
      </Button>
    </Form>
  );
};

export default AdminActionGroup;
