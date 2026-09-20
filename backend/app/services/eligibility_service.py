from typing import Any, Dict, List, Optional, Union

from app.database import crud
from app.engine.condition_evaluator import ConditionEvaluator
from app.engine.rule_registry import RuleRegistry
from app.engine.rule_engine import RuleEngine


class EligibilityService:
    """
    Main service responsible for checking scheme eligibility.
    """

    def __init__(
        self,
        db,
        rule_engine: Optional[RuleEngine] = None,
    ):
        self.db = db
        if rule_engine is not None:
            self.rule_engine = rule_engine
        else:
            self.rule_engine = RuleEngine(
                evaluator=ConditionEvaluator(),
                registry=RuleRegistry(db),
            )

    def check_eligibility(
        self,
        profile: Dict[str, Any],
        save_results: bool = False,
        user_id: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Check the supplied profile against all active schemes.
        Returns a list of scheme evaluation results.
        """

        schemes = crud.get_all_schemes(
            self.db,
            active_only=True,
        )

        if not schemes:
            return []

        evaluations = self.rule_engine.evaluate(
            schemes,
            profile,
        )

        if save_results:
            for item in evaluations:
                try:
                    scheme_db_id = item.get("id")
                    if not scheme_db_id:
                        scheme_obj = crud.get_scheme(self.db, item.get("scheme_id"))
                        scheme_db_id = scheme_obj.id if scheme_obj else None

                    if scheme_db_id:
                        crud.create_eligibility_result(
                            db=self.db,
                            user_id=user_id,
                            scheme_id=scheme_db_id,
                            status=item.get("status", "unknown"),
                            reason=item.get("reason"),
                            matched_rules=item.get("passed_rules"),
                            failed_rules=item.get("failed_rules"),
                            profile_snapshot=profile,
                        )
                except Exception as err:
                    # Log but do not block eligibility return
                    print(f"Warning: Failed to save eligibility result: {err}")

        return evaluations

    def check_scheme_eligibility(
        self,
        scheme_id: Union[int, str],
        profile: Dict[str, Any],
        save_result: bool = False,
        user_id: Optional[int] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Check one specific scheme.
        """

        scheme = crud.get_scheme(
            self.db,
            scheme_id,
        )

        if scheme is None:
            return None

        result = self.rule_engine.evaluate_scheme(
            scheme,
            profile,
        )

        if save_result:
            try:
                crud.create_eligibility_result(
                    db=self.db,
                    user_id=user_id,
                    scheme_id=scheme.id,
                    status=result.get("status", "unknown"),
                    reason=result.get("reason"),
                    matched_rules=result.get("passed_rules"),
                    failed_rules=result.get("failed_rules"),
                    profile_snapshot=profile,
                )
            except Exception as err:
                print(f"Warning: Failed to save scheme eligibility result: {err}")

        return result

    # Alias for backward compatibility
    check_single_scheme = check_scheme_eligibility

    def check_user_eligibility(
        self,
        user_id: int,
        save_results: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Check eligibility for a citizen using their stored profile.
        """
        user = crud.get_user(self.db, user_id)
        if not user:
            raise ValueError(f"Citizen profile with id {user_id} not found.")

        profile = {
            "id": user.id,
            "name": user.name,
            "age": user.age,
            "gender": user.gender,
            "state": user.state,
            "district": user.district,
            "rural_urban": user.rural_urban,
            "category": user.category,
            "annual_income": user.annual_income,
            "family_size": user.family_size,
            "employment_status": user.employment_status,
            "education_level": user.education_level,
            "occupation": user.occupation,
            "marital_status": user.marital_status,
            "farmer": user.farmer,
            "land_ownership": user.land_ownership,
            "disability": user.disability,
            "house_ownership": user.house_ownership,
            "bpl_status": user.bpl_status,
            "student_status": user.student_status,
            "street_vendor": user.street_vendor,
            "minority": user.minority,
        }

        return self.check_eligibility(
            profile=profile,
            save_results=save_results,
            user_id=user_id,
        )