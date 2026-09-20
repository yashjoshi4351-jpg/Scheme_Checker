import { BrowserRouter, Routes, Route, Link, NavLink } from "react-router-dom";

import Home from "./pages/Home";
import CheckEligibility from "./pages/CheckEligibility";
import Results from "./pages/Results";
import SchemeDetails from "./pages/SchemeDetails";
import History from "./pages/History";

function App() {
  return (
    <BrowserRouter>
      <header className="navbar">
        <div className="nav-container">
          <Link to="/" className="nav-logo">
            🏛️ SchemeChecker
          </Link>
          <nav>
            <ul className="nav-links">
              <li>
                <NavLink to="/" className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}>
                  Home
                </NavLink>
              </li>
              <li>
                <NavLink to="/check-eligibility" className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}>
                  Check Eligibility
                </NavLink>
              </li>
              <li>
                <NavLink to="/history" className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}>
                  History
                </NavLink>
              </li>
            </ul>
          </nav>
        </div>
      </header>

      <main>
        <Routes>
          {/* Home */}
          <Route path="/" element={<Home />} />

          {/* Eligibility Checker */}
          <Route path="/check-eligibility" element={<CheckEligibility />} />

          {/* Eligibility Results */}
          <Route path="/results" element={<Results />} />

          {/* Individual Scheme Details */}
          <Route path="/schemes/:schemeId" element={<SchemeDetails />} />

          {/* Previous Eligibility Checks */}
          <Route path="/history" element={<History />} />

          {/* Fallback */}
          <Route path="*" element={<Home />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;