import { forwardRef, useImperativeHandle, useState } from "react";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";

const AdminDeleteQuestionModal = ({ onSubmit }, ref) => {
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleSubmit = () => {
    onSubmit();
    setShow(false);
  };

  useImperativeHandle(ref, () => ({
    openModal: () => setShow(true),
  }));

  return (
    <Modal
      show={show}
      onHide={handleClose}
      centered
      contentClassName="modal-content">
      <Modal.Header closeButton closeVariant="white">
        <Modal.Title className="fg-white">Delete Question</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <div>Are you sure to delete question?</div>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="primary" onClick={handleSubmit}>
          Yes
        </Button>
        <Button onClick={handleClose} className="btn-secondary">
          No
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default forwardRef(AdminDeleteQuestionModal);
