import re
from typing import Any, Dict, Optional


INDIAN_STATES = {
    "andhra pradesh",
    "arunachal pradesh",
    "assam",
    "bihar",
    "chhattisgarh",
    "goa",
    "gujarat",
    "haryana",
    "himachal pradesh",
    "jharkhand",
    "karnataka",
    "kerala",
    "madhya pradesh",
    "maharashtra",
    "manipur",
    "meghalaya",
    "mizoram",
    "nagaland",
    "odisha",
    "punjab",
    "rajasthan",
    "sikkim",
    "tamil nadu",
    "telangana",
    "tripura",
    "uttar pradesh",
    "uttarakhand",
    "west bengal",
    "delhi",
    "jammu and kashmir",
    "ladakh",
    "chandigarh",
    "puducherry",
}


def validate_age(age: Optional[Any]) -> bool:
    """
    Validate citizen age.
    """

    if age is None:
        return True

    try:
        age = int(age)
    except (TypeError, ValueError):
        return False

    return 0 <= age <= 120


def validate_income(income: Optional[Any]) -> bool:
    """
    Validate annual income.
    """

    if income is None:
        return True

    try:
        income = float(income)
    except (TypeError, ValueError):
        return False

    return income >= 0


def validate_family_size(
    family_size: Optional[Any],
) -> bool:
    """
    Validate family size.
    """

    if family_size is None:
        return True

    try:
        family_size = int(family_size)
    except (TypeError, ValueError):
        return False

    return family_size >= 1


def validate_state(
    state: Optional[str],
) -> bool:
    """
    Validate Indian state/UT name.
    """

    if state is None:
        return True

    normalized = state.strip().lower()

    return normalized in INDIAN_STATES


def validate_boolean(
    value: Optional[Any],
) -> bool:
    """
    Validate boolean-like values.
    """

    if value is None:
        return True

    if isinstance(value, bool):
        return True

    if isinstance(value, str):
        return value.strip().lower() in {
            "true",
            "false",
            "yes",
            "no",
            "1",
            "0",
        }

    if isinstance(value, int):
        return value in {0, 1}

    return False


def validate_profile(
    profile: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Validate a complete citizen profile.

    Returns:
        {
            "valid": bool,
            "errors": [...]
        }
    """

    errors = []

    if not validate_age(profile.get("age")):
        errors.append(
            "Age must be between 0 and 120."
        )

    if not validate_income(
        profile.get("annual_income")
    ):
        errors.append(
            "Annual income must be a non-negative number."
        )

    if not validate_family_size(
        profile.get("family_size")
    ):
        errors.append(
            "Family size must be at least 1."
        )

    if not validate_state(
        profile.get("state")
    ):
        errors.append(
            "Invalid Indian state or union territory."
        )

    boolean_fields = [
        "is_farmer",
        "has_disability",
        "owns_house",
        "is_bpl",
    ]

    for field in boolean_fields:
        if not validate_boolean(
            profile.get(field)
        ):
            errors.append(
                f"{field} must be a boolean value."
            )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }


def normalize_profile(
    profile: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Normalize profile values before sending them
    to the eligibility engine.
    """

    normalized = dict(profile)

    if normalized.get("state"):
        normalized["state"] = (
            normalized["state"]
            .strip()
            .title()
        )

    if normalized.get("district"):
        normalized["district"] = (
            normalized["district"]
            .strip()
            .title()
        )

    if normalized.get("gender"):
        normalized["gender"] = (
            normalized["gender"]
            .strip()
            .lower()
        )

    if normalized.get("category"):
        normalized["category"] = (
            normalized["category"]
            .strip()
            .upper()
        )

    if normalized.get("age") is not None:
        normalized["age"] = int(
            normalized["age"]
        )

    if normalized.get("annual_income") is not None:
        normalized["annual_income"] = float(
            normalized["annual_income"]
        )

    if normalized.get("family_size") is not None:
        normalized["family_size"] = int(
            normalized["family_size"]
        )

    return normalized


def sanitize_text(
    value: Optional[str],
) -> Optional[str]:
    """
    Basic text cleanup.
    """

    if value is None:
        return None

    value = re.sub(
        r"\s+",
        " ",
        value
    ).strip()

    return value or None