import { Link } from "react-router-dom";
import Navbar from "react-bootstrap/Navbar";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import logo from "./../logo.svg";
import useAuth from "./../hooks/useAuth";

const AppNavbar = () => {
  const { user, isAdmin, logout } = useAuth();
  return (
    <Navbar collapseOnSelect className="app-navbar" expand="lg" variant="dark">
      <Container>
        <Navbar.Brand className="app-navbar-brand" href="#">
          <img
            src={logo}
            width="35"
            height="35"
            className="d-inline-block align-bottom"
            alt=""
          />
          Poll App With Django & React
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="me-auto">
            {user && isAdmin() && (
              <Link className="app-navbar-link" to="/questionnaires">
                Admin Panel
              </Link>
            )}
            {user && !isAdmin() && (
              <Link className="app-navbar-link" to="/voting">
                Questionnaires
              </Link>
            )}
            <Link className="app-navbar-link" to="/">
              Home
            </Link>
          </Nav>
          <Nav>
            {user ? (
              <>
                <Nav.Link className="app-navbar-link">{user.username}</Nav.Link>
                <Nav.Link className="app-navbar-link" onClick={logout}>
                  Logut
                </Nav.Link>
              </>
            ) : (
              <Link className="app-navbar-link" to="/login">
                Login
              </Link>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default AppNavbar;
