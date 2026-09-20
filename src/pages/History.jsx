import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getHistory, deleteHistory } from "../services/api";

const History = () => {
  const navigate = useNavigate();

  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchHistory = async () => {
      setLoading(true);
      setError("");

      try {
        const data = await getHistory();

        const historyData = Array.isArray(data)
          ? data
          : data?.history || [];

        setHistory(historyData);
      } catch (err) {
        console.error(err);

        setError(
          err.message ||
            "Unable to load eligibility history."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  const handleDelete = async (historyId) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this history record?"
    );

    if (!confirmed) {
      return;
    }

    try {
      await deleteHistory(historyId);

      setHistory((previousHistory) =>
        previousHistory.filter(
          (item) =>
            item.id !== historyId &&
            item.history_id !== historyId
        )
      );
    } catch (err) {
      console.error(err);

      setError(
        err.message ||
          "Unable to delete history record."
      );
    }
  };


  if (loading) {
    return (
      <div className="page">
        <div className="loading-message">
          Loading history...
        </div>
      </div>
    );
  }

  return (
    <div className="page history-page">
      <div className="page-header">
        <h1>Eligibility History</h1>

        <p>
          View your previous eligibility checks.
        </p>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {history.length === 0 ? (
        <div className="empty-state">
          <h2>No History Found</h2>

          <p>
            You have not performed any eligibility checks yet.
          </p>

          <button
            type="button"
            onClick={() =>
              navigate("/check-eligibility")
            }
          >
            Check Eligibility
          </button>
        </div>
      ) : (
        <div className="history-list">
          {history.map((item, index) => {
            const historyId =
              item.id ||
              item.history_id ||
              index;

            const date =
              item.created_at ||
              item.date ||
              item.checked_at;

            const schemeCount =
              item.scheme_count ??
              item.results_count ??
              item.results?.length ??
              0;

            return (
              <div
                className="history-card"
                key={historyId}
              >
                <div className="history-content">
                  <h3>
                    Eligibility Check
                  </h3>

                  {date && (
                    <p>
                      Date:{" "}
                      {new Date(date).toLocaleString()}
                    </p>
                  )}

                  <p>
                    Schemes evaluated: {schemeCount}
                  </p>
                </div>

                <div className="history-actions">
                  <button
                    type="button"
                    onClick={() => {
                      if (item.results) {
                        sessionStorage.setItem(
                          "eligibilityResults",
                          JSON.stringify(
                            item.results
                          )
                        );
                      }

                      navigate("/results", {
                        state: {
                          results:
                            item.results ||
                            item,
                        },
                      });
                    }}
                  >
                    View Results
                  </button>

                  <button
                    type="button"
                    onClick={() =>
                      handleDelete(historyId)
                    }
                  >
                    Delete
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default History;