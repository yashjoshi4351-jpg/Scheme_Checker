import React, { useEffect, useMemo, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import SchemeCard from "../components/SchemeCard";
import FilterBar from "../components/FilterBar";

const Results = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const [results, setResults] = useState([]);
  const [filters, setFilters] = useState({
    search: "",
    category: "",
    eligibility: "",
  });

  useEffect(() => {
    let resultData = location.state?.results;

    if (!resultData) {
      const storedResults = sessionStorage.getItem(
        "eligibilityResults"
      );

      if (storedResults) {
        try {
          resultData = JSON.parse(storedResults);
        } catch (error) {
          console.error("Invalid stored results:", error);
        }
      }
    }

    if (!resultData) {
      navigate("/check-eligibility");
      return;
    }

    const normalizedResults = Array.isArray(resultData)
      ? resultData
      : resultData.results || [];

    setResults(normalizedResults);
  }, [location.state, navigate]);

  const filteredResults = useMemo(() => {
    return results.filter((scheme) => {
      const name = (scheme.name || scheme.scheme_name || "").toLowerCase();
      const desc = (scheme.description || "").toLowerCase();
      const cat = (scheme.category || "").toLowerCase();
      const status = String(scheme.status || (scheme.eligible ? "eligible" : "not_eligible")).toLowerCase();

      if (filters.search) {
        const query = filters.search.toLowerCase();
        if (!name.includes(query) && !desc.includes(query)) {
          return false;
        }
      }

      if (filters.category && cat !== filters.category.toLowerCase()) {
        return false;
      }

      if (filters.eligibility && filters.eligibility !== "all") {
        if (filters.eligibility === "eligible" && !scheme.eligible) return false;
        if (filters.eligibility === "not_eligible" && scheme.eligible) return false;
        if (filters.eligibility === "pending" && status !== "partially_eligible" && status !== "pending") return false;
      }

      return true;
    });
  }, [results, filters]);

  const handleResetFilters = () => {
    setFilters({ search: "", category: "", eligibility: "" });
  };

  return (
    <div className="page results-page">
      <div className="page-header">
        <h1>Eligibility Results</h1>

        <p>
          Here are the government schemes evaluated against your profile.
        </p>
      </div>

      <FilterBar
        schemes={results}
        filters={filters}
        onFilterChange={setFilters}
        onReset={handleResetFilters}
      />

      {filteredResults.length === 0 ? (
        <div className="empty-state">
          <h2>No schemes found</h2>
          <p>
            No schemes match the selected filter criteria.
          </p>

          <button
            type="button"
            onClick={handleResetFilters}
          >
            Show All
          </button>
        </div>
      ) : (
        <div className="schemes-grid">
          {filteredResults.map((scheme, index) => (
            <SchemeCard
              key={
                scheme.scheme_id ||
                scheme.id ||
                index
              }
              scheme={scheme}
              onViewDetails={() => navigate(`/schemes/${scheme.scheme_id || scheme.id}`)}
            />
          ))}
        </div>
      )}


      <div className="results-actions">
        <button
          type="button"
          onClick={() => navigate("/check-eligibility")}
        >
          Check Again
        </button>

        <button
          type="button"
          onClick={() => navigate("/history")}
        >
          View History
        </button>
      </div>
    </div>
  );
};

export default Results;