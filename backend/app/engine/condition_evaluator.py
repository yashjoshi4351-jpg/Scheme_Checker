import json
from typing import Any


class ConditionEvaluator:
    """
    Evaluates a single eligibility condition against a user profile.

    Supported operators:
        =, ==, !=
        >, >=
        <, <=
        IN, NOT IN
        CONTAINS
        EXISTS
    """

    OPERATOR_ALIASES = {
        "=": "==",
        "==": "==",
        "!=": "!=",
        ">": ">",
        ">=": ">=",
        "<": "<",
        "<=": "<=",
        "IN": "IN",
        "in": "IN",
        "NOT IN": "NOT IN",
        "not in": "NOT IN",
        "CONTAINS": "CONTAINS",
        "contains": "CONTAINS",
        "EXISTS": "EXISTS",
        "exists": "EXISTS",
    }

    FIELD_ALIASES = {
        "farmer": ["farmer", "is_farmer"],
        "is_farmer": ["is_farmer", "farmer"],
        "land_ownership": ["land_ownership", "has_land", "owns_land", "farmer_land"],
        "house_ownership": ["house_ownership", "owns_house", "has_house"],
        "bpl_status": ["bpl_status", "is_bpl", "bpl"],
        "student_status": ["student_status", "is_student"],
        "street_vendor": ["street_vendor", "is_street_vendor", "vendor"],
        "disability": ["disability", "has_disability"],
        "education_level": ["education_level", "education"],
        "education": ["education", "education_level"],
        "minority": ["minority", "is_minority"],
    }

    @staticmethod
    def _normalize_operator(operator: str) -> str:
        if not operator:
            raise ValueError("Condition operator cannot be empty.")

        operator = operator.strip()

        if operator not in ConditionEvaluator.OPERATOR_ALIASES:
            raise ValueError(f"Unsupported operator: {operator}")

        return ConditionEvaluator.OPERATOR_ALIASES[operator]

    @classmethod
    def _get_field_value(cls, user_profile: Any, field: str):
        """
        Get a field value from either:
        - SQLAlchemy User model
        - dictionary
        Supports common field aliases.
        """
        if not field:
            raise ValueError("Condition field cannot be empty.")

        candidate_fields = cls.FIELD_ALIASES.get(field, [field])
        if field not in candidate_fields:
            candidate_fields = [field] + candidate_fields

        for candidate in candidate_fields:
            # Dictionary profile
            if isinstance(user_profile, dict):
                if candidate in user_profile and user_profile[candidate] is not None:
                    return user_profile[candidate]
            # SQLAlchemy/Python object
            elif hasattr(user_profile, candidate):
                val = getattr(user_profile, candidate)
                if val is not None:
                    return val

        return None

    @staticmethod
    def _parse_expected_value(value: Any) -> Any:
        """
        Parse raw rule values stored as strings in the database.
        """
        if not isinstance(value, str):
            return value

        cleaned = value.strip()
        if cleaned.lower() == "true":
            return True
        if cleaned.lower() == "false":
            return False

        if (cleaned.startswith("[") and cleaned.endswith("]")) or (cleaned.startswith("{") and cleaned.endswith("}")):
            try:
                return json.loads(cleaned)
            except Exception:
                pass

        try:
            if "." in cleaned:
                return float(cleaned)
            return int(cleaned)
        except (ValueError, TypeError):
            pass

        return value

    @staticmethod
    def _to_number(val: Any):
        if val is None:
            return None
        if isinstance(val, (int, float)):
            return val
        try:
            return float(str(val).strip())
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _values_equal(actual: Any, expected: Any) -> bool:
        """
        Performs a reasonably flexible equality comparison.
        """
        # Handle boolean values explicitly
        if isinstance(expected, bool):
            if isinstance(actual, bool):
                return actual == expected
            if isinstance(actual, (int, float)):
                return bool(actual) == expected
            if isinstance(actual, str):
                actual_lower = actual.strip().lower()
                if actual_lower in {"true", "yes", "1"}:
                    return expected is True
                if actual_lower in {"false", "no", "0"}:
                    return expected is False
                return actual_lower == str(expected).lower()

        # Numeric comparison
        actual_num = ConditionEvaluator._to_number(actual)
        expected_num = ConditionEvaluator._to_number(expected)
        if actual_num is not None and expected_num is not None:
            return actual_num == expected_num

        # String comparison
        if isinstance(actual, str) and isinstance(expected, str):
            return actual.strip().lower() == expected.strip().lower()

        return actual == expected

    @classmethod
    def evaluate(
        cls,
        field: str,
        operator: str,
        expected_value: Any,
        user_profile: Any,
    ) -> bool:

        """
        Evaluate one condition.

        Example:
            ConditionEvaluator.evaluate(
                field="age",
                operator=">=",
                expected_value=18,
                user_profile=user
            )
        """

        expected_value = cls._parse_expected_value(expected_value)
        actual_value = cls._get_field_value(user_profile, field)
        normalized_operator = cls._normalize_operator(operator)

        # ---------------------------------------------------------
        # EXISTS
        # ---------------------------------------------------------

        if normalized_operator == "EXISTS":
            if isinstance(expected_value, bool):
                exists = actual_value is not None
                return exists == expected_value

            return actual_value is not None

        # ---------------------------------------------------------
        # Missing value
        # ---------------------------------------------------------

        if actual_value is None:
            return False

        # ---------------------------------------------------------
        # Equality
        # ---------------------------------------------------------

        if normalized_operator == "==":
            return cls._values_equal(actual_value, expected_value)

        # ---------------------------------------------------------
        # Not equal
        # ---------------------------------------------------------

        if normalized_operator == "!=":
            return not cls._values_equal(actual_value, expected_value)

        # ---------------------------------------------------------
        # Greater than
        # ---------------------------------------------------------

        if normalized_operator == ">":
            act_num = cls._to_number(actual_value)
            exp_num = cls._to_number(expected_value)
            if act_num is not None and exp_num is not None:
                return act_num > exp_num
            try:
                return actual_value > expected_value
            except TypeError:
                return False

        # ---------------------------------------------------------
        # Greater than or equal
        # ---------------------------------------------------------

        if normalized_operator == ">=":
            act_num = cls._to_number(actual_value)
            exp_num = cls._to_number(expected_value)
            if act_num is not None and exp_num is not None:
                return act_num >= exp_num
            try:
                return actual_value >= expected_value
            except TypeError:
                return False

        # ---------------------------------------------------------
        # Less than
        # ---------------------------------------------------------

        if normalized_operator == "<":
            act_num = cls._to_number(actual_value)
            exp_num = cls._to_number(expected_value)
            if act_num is not None and exp_num is not None:
                return act_num < exp_num
            try:
                return actual_value < expected_value
            except TypeError:
                return False

        # ---------------------------------------------------------
        # Less than or equal
        # ---------------------------------------------------------

        if normalized_operator == "<=":
            act_num = cls._to_number(actual_value)
            exp_num = cls._to_number(expected_value)
            if act_num is not None and exp_num is not None:
                return act_num <= exp_num
            try:
                return actual_value <= expected_value
            except TypeError:
                return False

        # ---------------------------------------------------------
        # IN
        # ---------------------------------------------------------

        if normalized_operator == "IN":
            if not isinstance(expected_value, (list, tuple, set)):
                expected_value = [expected_value]

            return any(
                cls._values_equal(actual_value, value)
                for value in expected_value
            )

        # ---------------------------------------------------------
        # NOT IN
        # ---------------------------------------------------------

        if normalized_operator == "NOT IN":
            if not isinstance(expected_value, (list, tuple, set)):
                expected_value = [expected_value]

            return not any(
                cls._values_equal(actual_value, value)
                for value in expected_value
            )

        # ---------------------------------------------------------
        # CONTAINS
        # ---------------------------------------------------------

        if normalized_operator == "CONTAINS":
            if isinstance(actual_value, (list, tuple, set)):
                return any(
                    cls._values_equal(item, expected_value)
                    for item in actual_value
                )

            if isinstance(actual_value, str):
                return str(expected_value).lower() in actual_value.lower()

            return False

        raise ValueError(
            f"Unsupported operator: {normalized_operator}"
        )