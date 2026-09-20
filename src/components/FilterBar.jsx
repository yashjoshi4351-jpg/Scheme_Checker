import { useMemo } from "react";

function FilterBar({
  schemes = [],
  filters = {},
  value,
  onChange,
  onFilterChange,
  onReset,
}) {
  const currentFilters = {
    search: filters.search || "",
    category: filters.category || "",
    eligibility: filters.eligibility || value || "",
  };

  const categories = useMemo(() => {
    const values = schemes
      .map((scheme) => scheme.category)
      .filter(Boolean);

    return [...new Set(values)];
  }, [schemes]);

  const handleChange = (event) => {
    const { name, value: fieldVal } = event.target;

    if (onFilterChange) {
      onFilterChange({
        ...currentFilters,
        [name]: fieldVal,
      });
    } else if (name === "eligibility" && onChange) {
      onChange(fieldVal);
    }
  };

  const handleReset = () => {
    if (onReset) {
      onReset();
    } else if (onFilterChange) {
      onFilterChange({ search: "", category: "", eligibility: "" });
    } else if (onChange) {
      onChange("all");
    }
  };

  return (
    <div className="filter-bar">
      <div className="filter-group">
        <label htmlFor="search">Search Schemes</label>

        <input
          id="search"
          name="search"
          type="search"
          value={currentFilters.search}
          onChange={handleChange}
          placeholder="Search by scheme name or keywords..."
        />
      </div>

      <div className="filter-group">
        <label htmlFor="category">Category</label>

        <select
          id="category"
          name="category"
          value={currentFilters.category}
          onChange={handleChange}
        >
          <option value="">All Categories</option>

          {categories.map((category) => (
            <option key={category} value={category}>
              {category}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <label htmlFor="eligibility">Eligibility</label>

        <select
          id="eligibility"
          name="eligibility"
          value={currentFilters.eligibility}
          onChange={handleChange}
        >
          <option value="">All</option>
          <option value="eligible">Eligible</option>
          <option value="not_eligible">Not Eligible</option>
          <option value="pending">Needs Verification / Partial</option>
        </select>
      </div>

      <button
        type="button"
        className="reset-filter-button"
        onClick={handleReset}
      >
        Reset
      </button>
    </div>
  );
}

export default FilterBar;