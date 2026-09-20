import React from "react";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="page home-page">
      <section className="hero-section">
        <div className="hero-content">
          <h1>Government Scheme Eligibility Checker</h1>

          <p>
            Find government schemes you may be eligible for by providing
            your basic profile information.
          </p>

          <Link to="/check-eligibility" className="primary-button">
            Check My Eligibility
          </Link>
        </div>
      </section>

      <section className="features-section">
        <h2>How It Works</h2>

        <div className="features-grid">
          <div className="feature-card">
            <h3>1. Enter Your Profile</h3>
            <p>
              Provide information such as age, income, occupation,
              category, state and other required details.
            </p>
          </div>

          <div className="feature-card">
            <h3>2. Check Eligibility</h3>
            <p>
              Our eligibility engine compares your profile with
              available government scheme rules.
            </p>
          </div>

          <div className="feature-card">
            <h3>3. View Results</h3>
            <p>
              See eligible, ineligible and applicable schemes along
              with reasons.
            </p>
          </div>
        </div>
      </section>

      <section className="home-links">
        <Link to="/check-eligibility">Check Eligibility</Link>
        <Link to="/history">View History</Link>
      </section>
    </div>
  );
};

export default Home;