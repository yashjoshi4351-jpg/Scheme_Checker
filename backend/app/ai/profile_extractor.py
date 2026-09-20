import logging
from typing import Any, Dict, Optional

from app.ai.llm_client import llm_client

logger = logging.getLogger(__name__)


PROFILE_FIELDS = [
    "age",
    "gender",
    "state",
    "district",
    "category",
    "annual_income",
    "family_size",
    "employment_status",
    "education",
    "occupation",
    "is_farmer",
    "has_disability",
    "owns_house",
    "is_bpl",
]


class ProfileExtractor:
    """
    Extracts a structured citizen profile from natural-language input.

    Important:
    This class only extracts information.
    It does not determine scheme eligibility.
    """

    SYSTEM_PROMPT = """
You are a structured data extraction assistant for an Indian
Government Scheme Eligibility Checker.

Your task is ONLY to extract citizen information from the user's text.

Never decide whether the citizen is eligible for any government scheme.

Use only information explicitly stated or clearly implied by the user.
Do not invent missing information.

Return a JSON object containing exactly these fields:

age
gender
state
district
category
annual_income
family_size
employment_status
education
occupation
is_farmer
has_disability
owns_house
is_bpl

Rules:

1. Missing information must be null.
2. age must be an integer when available.
3. annual_income must be a number representing annual income in INR.
4. family_size must be an integer.
5. Boolean fields must be true, false, or null.
6. Do not guess a person's caste/category.
7. Do not guess BPL status.
8. Do not guess disability status.
9. Do not guess farmer status.
10. Preserve the meaning of the user's information.
11. Return ONLY valid JSON.
"""

    def __init__(self, client=llm_client):
        self.client = client

    def extract(
        self,
        text: str,
    ) -> Dict[str, Any]:
        """
        Extract a structured profile from natural language.
        """

        if not text or not text.strip():
            raise ValueError(
                "Profile text cannot be empty."
            )

        prompt = f"""
Extract the citizen profile from the following text.

User input:
{text}

Return the required JSON object.
"""

        try:
            data = self.client.generate_json(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                temperature=0.0,
                max_tokens=700,
            )

            return self._normalize_profile(data)

        except Exception as exc:
            logger.exception(
                "Profile extraction failed: %s",
                exc
            )

            # Return an empty structured profile instead of
            # inventing information.
            return self.empty_profile()

    def _normalize_profile(
        self,
        data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Normalize the LLM output so that downstream services
        always receive the expected profile fields.
        """

        profile = {}

        for field in PROFILE_FIELDS:
            profile[field] = data.get(field)

        profile["age"] = self._to_int(
            profile["age"]
        )

        profile["annual_income"] = self._to_number(
            profile["annual_income"]
        )

        profile["family_size"] = self._to_int(
            profile["family_size"]
        )

        profile["is_farmer"] = self._to_bool(
            profile["is_farmer"]
        )

        profile["has_disability"] = self._to_bool(
            profile["has_disability"]
        )

        profile["owns_house"] = self._to_bool(
            profile["owns_house"]
        )

        profile["is_bpl"] = self._to_bool(
            profile["is_bpl"]
        )

        return profile

    @staticmethod
    def _to_int(value: Any) -> Optional[int]:
        if value is None:
            return None

        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _to_number(value: Any) -> Optional[float]:
        if value is None:
            return None

        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _to_bool(value: Any) -> Optional[bool]:
        if value is None:
            return None

        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            value = value.strip().lower()

            if value in {"true", "yes", "1"}:
                return True

            if value in {"false", "no", "0"}:
                return False

        return None

    @staticmethod
    def empty_profile() -> Dict[str, Any]:
        """
        Return a complete empty profile.
        """

        return {
            field: None
            for field in PROFILE_FIELDS
        }


# Shared extractor instance
profile_extractor = ProfileExtractor()