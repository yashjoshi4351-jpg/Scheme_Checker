import { useNavigate } from "react-router-dom";
import EligibilityBadge from "./EligibilityBadge";
import EligibilityReason from "./EligibilityReason";

function SchemeCard({
  scheme,
  eligibility,
  onViewDetails,
}) {
  const navigate = useNavigate();

  if (!scheme) {
    return null;
  }

  const schemeName = scheme.name || scheme.scheme_name || "Government Scheme";

  const description =
    scheme.description || "No description available for this scheme.";

  const benefits = scheme.benefits || scheme.benefit || [];

  const normalizedBenefits = Array.isArray(benefits)
    ? benefits
    : [benefits];

  const eligibleVal = eligibility?.eligible ?? scheme.eligible;
  const statusVal = eligibility?.status ?? scheme.status;
  const reasonVal = eligibility?.reason ?? scheme.reason ?? scheme.reasons;

  const handleDetailsClick = () => {
    if (onViewDetails) {
      onViewDetails(scheme);
    } else {
      navigate(`/schemes/${scheme.scheme_id || scheme.id}`);
    }
  };

  return (
    <article className="scheme-card">
      <div className="scheme-card-header">
        <div>
          <h3>{schemeName}</h3>

          {(scheme.department || scheme.ministry) && (
            <p className="scheme-department">
              {scheme.department || scheme.ministry}
            </p>
          )}
        </div>

        {statusVal && (
          <EligibilityBadge
            eligible={eligibleVal}
            status={statusVal}
          />
        )}
      </div>

      <p className="scheme-description">{description}</p>

      {normalizedBenefits.length > 0 &&
        normalizedBenefits.some(Boolean) && (
          <div className="scheme-benefits">
            <h4>Benefits</h4>

            {typeof normalizedBenefits[0] === "string" ? (
              <p>{normalizedBenefits.filter(Boolean).join(", ")}</p>
            ) : (
              <ul>
                {normalizedBenefits
                  .filter(Boolean)
                  .map((benefit, index) => (
                    <li key={index}>
                      {typeof benefit === "object" ? (benefit.description || JSON.stringify(benefit)) : String(benefit)}
                    </li>
                  ))}
              </ul>
            )}
          </div>
        )}

      {reasonVal && (
        <EligibilityReason
          reason={reasonVal}
          eligible={eligibleVal}
        />
      )}

      <div className="scheme-card-footer">
        {scheme.category && (
          <span className="scheme-category">
            {scheme.category}
          </span>
        )}

        <button
          type="button"
          onClick={handleDetailsClick}
        >
          View Details
        </button>
      </div>
    </article>
  );
}

export default SchemeCard;