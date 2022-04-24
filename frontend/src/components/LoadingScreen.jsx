import React from "react";
import Spinner from "react-bootstrap/Spinner";

const LoadingScreen = () => {
  return (
    <div className="loading-container">
      <Spinner animation="border" />
    </div>
  );
};

export default LoadingScreen;
