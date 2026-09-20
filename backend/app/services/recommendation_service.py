from typing import Any, Dict, List


class RecommendationService:
    """
    Provides scheme recommendations based on eligibility results.
    """

    def __init__(
        self,
        db,
        rule_engine,
    ):
        self.db = db
        self.rule_engine = rule_engine

    def recommend(
        self,
        profile: Dict[str, Any],
        schemes: List[Any],
    ) -> List[Dict[str, Any]]:
        """
        Return schemes for which the supplied profile satisfies
        all registered rules.
        """

        evaluations = self.rule_engine.evaluate(
            schemes,
            profile,
        )

        recommendations = []

        for result in evaluations:
            if result.get("eligible") is True:
                recommendations.append(result)

        return recommendations

    def recommend_all(
        self,
        profile: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Retrieve all active schemes and recommend eligible ones.
        """

        from app.database import crud

        schemes = crud.get_all_schemes(
            self.db,
            active_only=True,
        )

        return self.recommend(
            profile,
            schemes,
        )