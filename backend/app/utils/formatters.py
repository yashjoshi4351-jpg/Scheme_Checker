from typing import Any, Dict, List


def format_currency(
    amount: Any,
) -> str:
    """
    Format an amount as Indian Rupees.
    """

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return "₹0"

    return f"₹{amount:,.2f}"


def format_eligibility_status(
    eligible: Any,
) -> str:
    """
    Convert boolean eligibility into a readable status.
    """

    if eligible is True:
        return "Eligible"

    if eligible is False:
        return "Not Eligible"

    return "Needs More Information"


def format_reasons(
    reasons: Any,
) -> List[str]:
    """
    Normalize eligibility reasons into a list.
    """

    if reasons is None:
        return []

    if isinstance(reasons, str):
        return [reasons]

    if isinstance(reasons, list):
        return [
            str(reason)
            for reason in reasons
            if reason is not None
        ]

    return [str(reasons)]


def format_eligibility_result(
    result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Convert an internal eligibility result into
    a consistent API-friendly structure.
    """

    eligible = result.get("eligible")

    return {
        "scheme_id": result.get("scheme_id"),
        "scheme_name": result.get("scheme_name"),
        "eligible": eligible,
        "status": format_eligibility_status(
            eligible
        ),
        "reasons": format_reasons(
            result.get("reasons")
        ),
        "failed_rules": format_reasons(
            result.get("failed_rules")
        ),
        "missing_information": format_reasons(
            result.get("missing_information")
        ),
        "explanation": result.get(
            "explanation"
        ),
        "required_documents": format_reasons(
            result.get("required_documents")
        ),
        "rule_results": result.get(
            "rule_results",
            [],
        ),
    }


def format_scheme(
    scheme: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Convert scheme data into a consistent API format.
    """

    return {
        "id": scheme.get("id"),
        "name": scheme.get("name"),
        "description": scheme.get(
            "description"
        ),
        "department": scheme.get(
            "department"
        ),
        "state": scheme.get(
            "state"
        ),
        "benefits": scheme.get(
            "benefits"
        ),
    }


def format_scheme_list(
    schemes: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Format multiple schemes.
    """

    formatted = [
        format_scheme(scheme)
        for scheme in schemes
    ]

    return {
        "total": len(formatted),
        "schemes": formatted,
    }