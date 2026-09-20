from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class EligibilityRequest(BaseModel):
    """
    Request sent by the frontend to check eligibility.
    """

    user_id: Optional[int] = None

    scheme_id: Optional[int] = None

    profile: Optional[Dict[str, Any]] = None

    natural_language_input: Optional[str] = None


class RuleResult(BaseModel):
    """
    Result of an individual eligibility rule.
    """

    rule_id: Optional[str] = None

    field: Optional[str] = None

    condition: Optional[str] = None

    passed: Optional[bool] = None

    reason: Optional[str] = None


class EligibilityResponse(BaseModel):
    """
    Final eligibility response returned to the frontend.
    """

    scheme_id: int

    scheme_name: Optional[str] = None

    eligible: bool

    status: str

    reasons: List[str] = Field(
        default_factory=list
    )

    failed_rules: List[str] = Field(
        default_factory=list
    )

    missing_information: List[str] = Field(
        default_factory=list
    )

    rule_results: List[RuleResult] = Field(
        default_factory=list
    )

    explanation: Optional[str] = None

    required_documents: List[str] = Field(
        default_factory=list
    )