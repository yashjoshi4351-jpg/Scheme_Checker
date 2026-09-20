import json
import logging
import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Centralized LLM client for the Government Scheme Eligibility Checker.

    The LLM is used only for:
    1. Extracting structured citizen profile information.
    2. Generating human-readable explanations.

    It must NOT be used to make the final eligibility decision.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model or os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-120b"
        )

        self._client = None

        if self.api_key:
            try:
                from groq import Groq

                self._client = Groq(api_key=self.api_key)

            except ImportError:
                logger.warning(
                    "Groq package is not installed. "
                    "AI features will use fallback behaviour."
                )

            except Exception as exc:
                logger.exception(
                    "Failed to initialize LLM client: %s",
                    exc
                )

        else:
            logger.warning(
                "GROQ_API_KEY not configured. "
                "AI features will use fallback behaviour."
            )

    @property
    def is_available(self) -> bool:
        """Return True when the LLM client is ready."""
        return self._client is not None

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 1000,
    ) -> str:
        """
        Generate a text response from the LLM.
        """

        if not self.is_available:
            raise RuntimeError(
                "LLM service is not available. "
                "Configure GROQ_API_KEY and install the groq package."
            )

        messages = []

        if system_prompt:
            messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        try:
            response = self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            content = response.choices[0].message.content

            if not content:
                raise RuntimeError("LLM returned an empty response.")

            return content.strip()

        except Exception as exc:
            logger.exception(
                "LLM generation failed: %s",
                exc
            )
            raise RuntimeError(
                f"LLM generation failed: {exc}"
            ) from exc

    def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: int = 1000,
    ) -> Dict[str, Any]:
        """
        Generate and safely parse a JSON response.
        """

        json_system_prompt = (
            (system_prompt or "")
            + "\n\n"
            "Return ONLY valid JSON. "
            "Do not include Markdown, code fences, or explanations "
            "outside the JSON object."
        ).strip()

        response = self.generate(
            prompt=prompt,
            system_prompt=json_system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return self._parse_json(response)

    @staticmethod
    def _parse_json(response: str) -> Dict[str, Any]:
        """
        Parse JSON returned by the model.
        Handles accidental Markdown code fences.
        """

        cleaned = response.strip()

        if cleaned.startswith("```"):
            lines = cleaned.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            cleaned = "\n".join(lines).strip()

        try:
            data = json.loads(cleaned)

        except json.JSONDecodeError as exc:
            logger.error(
                "Invalid JSON returned by LLM: %s",
                response
            )
            raise ValueError(
                "LLM returned invalid JSON."
            ) from exc

        if not isinstance(data, dict):
            raise ValueError(
                "LLM JSON response must be an object."
            )

        return data


# Shared client instance
llm_client = LLMClient()