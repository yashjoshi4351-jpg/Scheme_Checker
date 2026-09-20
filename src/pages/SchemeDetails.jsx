import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import EligibilityBadge from "../components/EligibilityBadge";
import EligibilityReason from "../components/EligibilityReason";
import { getScheme } from "../services/api";

const SchemeDetails = () => {
  const { schemeId } = useParams();
  const navigate = useNavigate();

  const [scheme, setScheme] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchScheme = async () => {
      setLoading(true);
      setError("");

      try {
        const data = await getScheme(schemeId);
        const schemeObj = data?.scheme || data;

        // Check if we have evaluation results in sessionStorage for this scheme
        try {
          const stored = sessionStorage.getItem("eligibilityResults");
          if (stored) {
            const parsed = JSON.parse(stored);
            const resultsList = Array.isArray(parsed) ? parsed : parsed.results || [];
            const evaluated = resultsList.find(
              (s) => s.scheme_id === schemeId || String(s.id) === String(schemeId)
            );
            if (evaluated) {
              schemeObj.status = evaluated.status;
              schemeObj.eligible = evaluated.eligible;
              schemeObj.reasons = evaluated.reasons || evaluated.reason;
            }
          }
        } catch (e) {
          // Ignore session storage parse error
        }

        setScheme(schemeObj);
      } catch (err) {
        console.error(err);

        setError(
          err.message ||
            "Unable to load scheme details."
        );
      } finally {
        setLoading(false);
      }
    };

    if (schemeId) {
      fetchScheme();
    }
  }, [schemeId]);


  if (loading) {
    return (
      <div className="page">
        <div className="loading-message">
          Loading scheme details...
        </div>
      </div>
    );
  }

  if (error || !scheme) {
    return (
      <div className="page">
        <div className="error-message">
          {error || "Scheme not found."}
        </div>

        <button
          type="button"
          onClick={() => navigate(-1)}
        >
          Go Back
        </button>
      </div>
    );
  }

  const status =
    scheme.status ||
    scheme.eligibility_status ||
    scheme.result ||
    "unknown";

  const reasons =
    scheme.reasons ||
    scheme.eligibility_reasons ||
    scheme.reason ||
    [];

  return (
    <div className="page scheme-details-page">
      <button
        type="button"
        className="back-button"
        onClick={() => navigate(-1)}
      >
        ← Back
      </button>

      <section className="scheme-header">
        <h1>
          {scheme.name ||
            scheme.scheme_name ||
            "Government Scheme"}
        </h1>

        <EligibilityBadge status={status} />
      </section>

      <section className="scheme-information">
        <h2>About the Scheme</h2>

        <p>
          {scheme.description ||
            "No description available."}
        </p>
      </section>

      <section className="scheme-details">
        <h2>Scheme Details</h2>

        {scheme.department && (
          <div className="detail-item">
            <strong>Department:</strong>
            <span>{scheme.department}</span>
          </div>
        )}

        {scheme.category && (
          <div className="detail-item">
            <strong>Category:</strong>
            <span>{scheme.category}</span>
          </div>
        )}

        {scheme.benefit && (
          <div className="detail-item">
            <strong>Benefits:</strong>
            <span>{scheme.benefit}</span>
          </div>
        )}

        {scheme.benefits && (
          <div className="detail-item">
            <strong>Benefits:</strong>
            <span>
              {Array.isArray(scheme.benefits)
                ? scheme.benefits.join(", ")
                : scheme.benefits}
            </span>
          </div>
        )}
      </section>

      <section className="eligibility-section">
        <h2>Eligibility Result</h2>

        <EligibilityReason
          reasons={reasons}
          status={status}
        />
      </section>

      {scheme.documents && (
        <section className="documents-section">
          <h2>Required Documents</h2>

          <ul>
            {Array.isArray(scheme.documents) ? (
              scheme.documents.map((document, index) => (
                <li key={index}>{document}</li>
              ))
            ) : (
              <li>{scheme.documents}</li>
            )}
          </ul>
        </section>
      )}

      {scheme.application_url && (
        <section className="application-section">
          <a
            href={scheme.application_url}
            target="_blank"
            rel="noopener noreferrer"
            className="primary-button"
          >
            Apply / Official Website
          </a>
        </section>
      )}
    </div>
  );
};

export default SchemeDetails;