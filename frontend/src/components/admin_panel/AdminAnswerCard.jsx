import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";

const AdminAnswerCard = ({
  idx,
  answer,
  openAnswerModal,
  openDeleteAnswerModal,
}) => {
  return (
    <Card className="admin-panel-answer-card mb-4">
      <Card.Header className="admin-panel-answer-card-header" as="div">
        <div>Answer {idx + 1}</div>
        <div>
          <Button
            className="btn-edit"
            onClick={(e) => openAnswerModal(idx, answer.text)}>
            Edit
          </Button>
          <Button
            className="btn-delete"
            onClick={(e) => openDeleteAnswerModal(idx, answer.text)}>
            Delete
          </Button>
        </div>
      </Card.Header>
      <Card.Body>{answer.text}</Card.Body>
    </Card>
  );
};

export default AdminAnswerCard;
