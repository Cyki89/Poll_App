import { BrowserRouter } from "react-router-dom";
import AppNavbar from "./components/AppNavbar";
import AppRouter from "./components/AppRouter";
import { AuthProvider } from "./context/AuthContext";

import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

function App() {
  return (
    <BrowserRouter>
      <ToastContainer />
      <AuthProvider>
        <AppNavbar />
        <AppRouter />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
