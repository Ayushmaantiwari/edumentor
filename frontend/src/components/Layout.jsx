import { Outlet } from "react-router-dom";

import Navbar from "./Navbar.jsx";
import Sidebar from "./Sidebar.jsx";

function Layout() {
  return (
    <div className="dashboard">

      <Navbar />

      <div className="dashboard-body">

        <Sidebar />

        <main className="dashboard-main">
          <Outlet />
        </main>

      </div>

    </div>
  );
}

export default Layout;