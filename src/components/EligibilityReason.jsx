function EligibilityReason({ reason, eligible }) {
  if (!reason) {
    return null;
  }

  const reasons = Array.isArray(reason) ? reason : [reason];

  return (
    <div
      className={`eligibility-reason ${
        eligible ? "reason-success" : "reason-warning"
      }`}
    >
      <h4>
        {eligible ? "Why you are eligible" : "Eligibility information"}
      </h4>

      <ul>
        {reasons.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export default EligibilityReason;