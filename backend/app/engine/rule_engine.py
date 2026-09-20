from typing import Any, Dict, List, Optional


class RuleEngine:
    """
    Executes registered eligibility rules against a user profile.
    """

    def __init__(
        self,
        evaluator,
        registry,
    ):
        self.evaluator = evaluator
        self.registry = registry

    def evaluate_rule(
        self,
        rule: Any,
        user_profile: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Evaluate a single rule using rule.field, rule.operator, rule.value.
        """
        field = getattr(rule, "field", None) or (rule.get("field") if isinstance(rule, dict) else None)
        operator = getattr(rule, "operator", None) or (rule.get("operator") if isinstance(rule, dict) else None)
        value = getattr(rule, "value", None) if not isinstance(rule, dict) else rule.get("value")
        rule_id = getattr(rule, "rule_id", None) or getattr(rule, "id", None) or (rule.get("rule_id") if isinstance(rule, dict) else None)
        description = getattr(rule, "description", None) or (rule.get("description") if isinstance(rule, dict) else None)

        if not field or not operator:
            return {
                "rule_id": rule_id,
                "field": field,
                "passed": False,
                "reason": "Rule condition definition is missing field or operator.",
            }

        try:
            passed = self.evaluator.evaluate(
                field=field,
                operator=operator,
                expected_value=value,
                user_profile=user_profile,
            )
        except Exception as exc:
            return {
                "rule_id": rule_id,
                "field": field,
                "passed": False,
                "reason": f"Rule evaluation error: {str(exc)}",
            }

        actual_value = self.evaluator._get_field_value(user_profile, field)
        field_display = field.replace("_", " ").title()

        if passed:
            reason = description or f"{field_display} requirement satisfied ({operator} {value})."
        else:
            if actual_value is None:
                reason = f"{field_display} was not provided (Required: {operator} {value})."
            else:
                reason = f"{field_display} is {actual_value} (Does not satisfy {operator} {value})."

        return {
            "rule_id": rule_id,
            "field": field,
            "operator": operator,
            "expected_value": value,
            "actual_value": actual_value,
            "passed": bool(passed),
            "reason": reason,
        }

    def evaluate_scheme(
        self,
        scheme: Any,
        user_profile: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Evaluate all rules belonging to a scheme and return rich metadata.
        """
        scheme_id_pk = getattr(scheme, "id", None)
        if scheme_id_pk is None and isinstance(scheme, dict):
            scheme_id_pk = scheme.get("id")

        scheme_code = getattr(scheme, "scheme_id", None) or (scheme.get("scheme_id") if isinstance(scheme, dict) else None) or str(scheme_id_pk)
        name = getattr(scheme, "name", None) or (scheme.get("name") if isinstance(scheme, dict) else None) or "Government Scheme"
        ministry = getattr(scheme, "ministry", None) or (scheme.get("ministry") if isinstance(scheme, dict) else None)
        department = getattr(scheme, "department", None) or (scheme.get("department") if isinstance(scheme, dict) else None) or ministry
        category = getattr(scheme, "category", None) or (scheme.get("category") if isinstance(scheme, dict) else None)
        description = getattr(scheme, "description", None) or (scheme.get("description") if isinstance(scheme, dict) else None)
        benefits = getattr(scheme, "benefits", None) or (scheme.get("benefits") if isinstance(scheme, dict) else None)
        application_url = getattr(scheme, "application_url", None) or (scheme.get("application_url") if isinstance(scheme, dict) else None)

        rules = []
        if scheme_id_pk is not None:
            rules = self.registry.get_rules_for_scheme(scheme_id_pk)
        if not rules and scheme_code:
            rules = self.registry.get_rules_for_scheme(scheme_code)

        results: List[Dict[str, Any]] = []
        for rule in rules:
            results.append(
                self.evaluate_rule(
                    rule,
                    user_profile,
                )
            )

        passed_rules = [r for r in results if r["passed"]]
        failed_rules = [r for r in results if not r["passed"]]

        eligible = len(results) > 0 and len(failed_rules) == 0

        if eligible:
            status = "eligible"
            reasons = [r["reason"] for r in passed_rules]
            reason = "You meet all the eligibility criteria for this scheme."
        else:
            if len(passed_rules) > 0:
                status = "partially_eligible"
            else:
                status = "not_eligible"
            reasons = [r["reason"] for r in failed_rules]
            reason = reasons[0] if reasons else "Does not meet scheme eligibility criteria."

        return {
            "id": scheme_id_pk,
            "scheme_id": scheme_code,
            "name": name,
            "scheme_name": name,
            "ministry": ministry,
            "department": department,
            "category": category,
            "description": description,
            "benefits": benefits,
            "application_url": application_url,
            "eligible": eligible,
            "status": status,
            "reason": reason,
            "reasons": reasons,
            "rules": results,
            "rule_results": results,
            "passed_rules": passed_rules,
            "failed_rules": failed_rules,
        }

    def evaluate(
        self,
        schemes: List[Any],
        user_profile: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Evaluate multiple schemes.
        """
        return [
            self.evaluate_scheme(
                scheme,
                user_profile,
            )
            for scheme in schemes
        ]