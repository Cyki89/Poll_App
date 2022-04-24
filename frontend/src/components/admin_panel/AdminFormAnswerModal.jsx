import { forwardRef, useImperativeHandle, useState } from "react";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";

const AdminFormAnswerModal = ({ onSubmit }, ref) => {
  const [show, setShow] = useState(false);
  const [text, setText] = useState("");

  const handleClose = () => setShow(false);
  const handleSubmit = () => {
    onSubmit(text);
    setShow(false);
  };

  useImperativeHandle(ref, () => ({
    setText: (txt) => setText(txt || ""),
    openModal: () => setShow(true),
  }));

  return (
    <Modal
      show={show}
      onHide={handleClose}
      centered
      contentClassName="modal-content">
      <Modal.Header closeButton closeVariant="white">
        <Modal.Title className="fg-white">Answer Details</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form>
          <Form.Group className="mb-3">
            <Form.Label>Answer Name</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              value={text}
              className="modal-input"
              onChange={(e) => setText(e.target.value)}
            />
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="primary" onClick={handleSubmit}>
          Save Changes
        </Button>
        <Button onClick={handleClose} className="btn-secondary">
          Close
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default forwardRef(AdminFormAnswerModal);
