import logging
from typing import Any, Dict, List, Optional

from app.ai.llm_client import llm_client

logger = logging.getLogger(__name__)


class ExplanationGenerator:
    """
    Generates human-readable explanations from an already calculated
    eligibility result.

    This class MUST NOT calculate or change eligibility.
    """

    SYSTEM_PROMPT = """
You are an explanation assistant for an Indian Government Scheme
Eligibility Checker.

The eligibility decision has already been calculated by a deterministic
rule engine.

Your job is ONLY to explain that result in simple language.

You MUST NOT:
- change the eligibility status
- create new eligibility rules
- infer missing eligibility criteria
- override the rule engine
- claim a person is eligible when the supplied result says otherwise
- claim a person is not eligible when the supplied result says otherwise

Explain:
1. The scheme.
2. The eligibility status supplied by the system.
3. The important conditions that passed.
4. The important conditions that failed.
5. Missing information, if supplied.
6. Relevant required documents, if supplied.

Keep the explanation concise and citizen-friendly.

Do not provide legal advice.

Return ONLY valid JSON with:

{
    "summary": "...",
    "reasons": ["...", "..."],
    "missing_information": ["...", "..."],
    "documents": ["...", "..."]
}
"""

    def __init__(self, client=llm_client):
        self.client = client

    def generate(
        self,
        scheme: Dict[str, Any],
        eligibility_result: Dict[str, Any],
        profile: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate an explanation from an existing eligibility result.
        """

        payload = {
            "scheme": scheme,
            "eligibility_result": eligibility_result,
            "profile": profile or {},
        }

        prompt = f"""
Create a citizen-friendly explanation for the following
already-calculated eligibility result.

DATA:
{payload}

Do not recalculate eligibility.
Use the eligibility status exactly as provided.
"""

        try:
            explanation = self.client.generate_json(
                prompt=prompt,
                system_prompt=self.SYSTEM_PROMPT,
                temperature=0.2,
                max_tokens=900,
            )

            return self._normalize_explanation(
                explanation
            )

        except Exception as exc:
            logger.exception(
                "Explanation generation failed: %s",
                exc
            )

            return self._fallback_explanation(
                scheme=scheme,
                eligibility_result=eligibility_result,
            )

    def _normalize_explanation(
        self,
        data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Ensure a predictable response structure.
        """

        return {
            "summary": str(
                data.get("summary") or
                "Eligibility result is available."
            ),
            "reasons": self._to_string_list(
                data.get("reasons")
            ),
            "missing_information": self._to_string_list(
                data.get("missing_information")
            ),
            "documents": self._to_string_list(
                data.get("documents")
            ),
        }

    @staticmethod
    def _to_string_list(
        value: Any,
    ) -> List[str]:
        if value is None:
            return []

        if isinstance(value, list):
            return [
                str(item)
                for item in value
                if item is not None
            ]

        return [str(value)]

    @staticmethod
    def _fallback_explanation(
        scheme: Dict[str, Any],
        eligibility_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate a deterministic explanation if the LLM
        is unavailable.

        This guarantees that the API can still return a useful
        response without AI.
        """

        scheme_name = (
            scheme.get("name")
            or scheme.get("scheme_name")
            or "this scheme"
        )

        status = (
            eligibility_result.get("status")
            or eligibility_result.get("eligibility_status")
            or eligibility_result.get("eligible")
        )

        reasons = eligibility_result.get("reasons") or []

        if isinstance(reasons, str):
            reasons = [reasons]

        if status is True:
            summary = (
                f"Based on the eligibility rules, "
                f"you are eligible for {scheme_name}."
            )

        elif status is False:
            summary = (
                f"Based on the eligibility rules, "
                f"you are not eligible for {scheme_name}."
            )

        else:
            summary = (
                f"The eligibility result for {scheme_name} "
                f"could not be determined completely."
            )

        return {
            "summary": summary,
            "reasons": [
                str(reason)
                for reason in reasons
            ],
            "missing_information": (
                eligibility_result.get(
                    "missing_information"
                ) or []
            ),
            "documents": (
                scheme.get("required_documents")
                or []
            ),
        }


# Shared generator instance
explanation_generator = ExplanationGenerator()