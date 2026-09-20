function EligibilityBadge({ eligible, status }) {
  let label = "Not Eligible";
  let className = "eligibility-badge not-eligible";

  if (eligible === true) {
    label = "Eligible";
    className = "eligibility-badge eligible";
  } else if (
    status === "partial" ||
    status === "partially_eligible"
  ) {
    label = "Partially Eligible";
    className = "eligibility-badge partial";
  } else if (
    status === "unknown" ||
    status === "pending"
  ) {
    label = "Needs Verification";
    className = "eligibility-badge pending";
  }

  return (
    <span
      className={className}
      role="status"
      aria-label={`Eligibility status: ${label}`}
    >
      {label}
    </span>
  );
}

export default EligibilityBadge;