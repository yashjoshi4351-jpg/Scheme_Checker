import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import ProfileForm from "../components/ProfileForm";
import { checkEligibility } from "../services/api";

const CheckEligibility = () => {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (profileData) => {
    setLoading(true);
    setError("");

    try {
      const data = await checkEligibility(profileData);


      // Store the result temporarily for the Results page.
      sessionStorage.setItem(
        "eligibilityResults",
        JSON.stringify(data)
      );

      navigate("/results", {
        state: {
          results: data,
          profile: profileData,
        },
      });
    } catch (err) {
      console.error(err);
      setError(
        err.message || "Something went wrong while checking eligibility."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page check-eligibility-page">
      <div className="page-header">
        <h1>Check Eligibility</h1>
        <p>
          Enter your details to find government schemes applicable
          to you.
        </p>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {loading && (
        <div className="loading-message">
          Checking your eligibility...
        </div>
      )}

      <ProfileForm
        onSubmit={handleSubmit}
        loading={loading}
      />
    </div>
  );
};

export default CheckEligibility;