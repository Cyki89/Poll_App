import { forwardRef, useImperativeHandle, useState } from "react";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";

const AdminAddAnswerModal = ({ onSubmit }, ref) => {
  const [show, setShow] = useState(false);
  const [text, setText] = useState("");

  const handleClose = () => setShow(false);
  const handleSubmit = () => {
    onSubmit();
    setShow(false);
  };

  useImperativeHandle(ref, () => ({
    setText: (txt) => setText(txt),
    openModal: () => setShow(true),
  }));

  return (
    <Modal
      show={show}
      onHide={handleClose}
      centered
      contentClassName="modal-content">
      <Modal.Header closeButton closeVariant="white">
        <Modal.Title className="fg-white">Delete Answer</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <div>
          Are you sure to delete answer <span className="fg-brand">{text}</span>
          ?
        </div>
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

export default forwardRef(AdminAddAnswerModal);
