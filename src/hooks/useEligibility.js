import { useCallback, useState } from "react";
import { checkEligibility } from "../services/api";

export default function useEligibility() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const checkUserEligibility = useCallback(async (profileData) => {
    setLoading(true);
    setError(null);

    try {
      const response = await checkEligibility(profileData);

      /*
       * Backend may return:
       * {
       *   results: [...]
       * }
       *
       * or directly:
       * [...]
       */
      const eligibilityResults = Array.isArray(response)
        ? response
        : response?.results || [];

      setResults(eligibilityResults);

      return response;
    } catch (err) {
      const errorMessage =
        err?.message || "Unable to check eligibility.";

      setError(errorMessage);
      setResults([]);

      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const clearResults = useCallback(() => {
    setResults([]);
    setError(null);
  }, []);

  return {
    results,
    loading,
    error,
    checkUserEligibility,
    clearResults,
  };
}