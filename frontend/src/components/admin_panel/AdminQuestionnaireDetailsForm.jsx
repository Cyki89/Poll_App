import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";

const AdminQuestionnaireDetailsForm = ({ data, setData, onSubmit }) => {
  const handleSubmit = (e) => {
    e.preventDefault();

    const requestObj = {
      name: data.name,
      date_added: data.data_added,
      description: data.description,
      is_active: data.isActive,
    };

    onSubmit(e, requestObj);
  };

  return (
    <Form className="" onSubmit={(e) => handleSubmit(e)}>
      <h1 className="app-form-header">Details</h1>
      <div className="admin-panel-horizontal-form">
        {" "}
        <Form.Group>
          <Form.Label>Questionnaire Title</Form.Label>
          <Form.Control
            className="admin-panel-input form-control"
            placeholder="Questionnary..."
            value={data.name}
            onChange={(e) => {
              setData((prev) => {
                return { ...prev, name: e.target.value };
              });
            }}
          />
        </Form.Group>
        <Form.Group>
          <Form.Label>Activity</Form.Label>
          <Form.Select
            className="admin-panel-input"
            value={data.is_active}
            onChange={(e) => {
              setData((prev) => {
                return { ...prev, is_active: e.target.value };
              });
            }}>
            <option value="">Select ...</option>
            <option value={true}>Active</option>
            <option value={false}>Inactive</option>
          </Form.Select>
        </Form.Group>
      </div>
      <Form.Group className="mb-3">
        <Form.Label>Description</Form.Label>
        <Form.Control
          value={data.description}
          onChange={(e) => {
            setData((prev) => {
              return { ...prev, description: e.target.value };
            });
          }}
          className="admin-panel-input"
          placeholder="Questionnary Description"
          as="textarea"
          rows={3}
        />
      </Form.Group>
      <Button type="submit" className="admin-panel-btn btn-block mb-2">
        Change Details
      </Button>
    </Form>
  );
};

export default AdminQuestionnaireDetailsForm;
