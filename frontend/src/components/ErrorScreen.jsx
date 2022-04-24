import React from "react";

const ErrorScreen = ({ children }) => {
  return (
    <div className="error-container">
      <div className="error-msg">
        {children}
        <span className="error-mark">!</span>
      </div>
    </div>
  );
};

export default ErrorScreen;
