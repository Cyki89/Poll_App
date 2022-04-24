import Container from "react-bootstrap/Container";
import { Outlet } from "react-router-dom";

const Layout = () => {
  return (
    <Container className="app-container">
      <Outlet />
    </Container>
  );
};

export default Layout;
