# backend/app/engine/rule_registry.py

from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.rule import Rule


class RuleRegistry:
    """
    Provides access to scheme eligibility rules stored in the database.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_rules_for_scheme(
        self,
        scheme_id: int,
    ) -> List[Rule]:
        """
        Return all rules belonging to a scheme.
        """

        return (
            self.db.query(Rule)
            .filter(Rule.scheme_id == scheme_id)
            .all()
        )

    def get_required_rules_for_scheme(
        self,
        scheme_id: int,
    ) -> List[Rule]:
        """
        Return only mandatory rules.
        """

        return (
            self.db.query(Rule)
            .filter(
                Rule.scheme_id == scheme_id,
                Rule.is_required.is_(True),
            )
            .all()
        )

    def get_rule_by_id(
        self,
        rule_id: int,
    ) -> Optional[Rule]:
        """
        Return a specific rule.
        """

        return (
            self.db.query(Rule)
            .filter(Rule.id == rule_id)
            .first()
        )

    def count_rules_for_scheme(
        self,
        scheme_id: int,
    ) -> int:
        """
        Return the number of rules configured for a scheme.
        """

        return (
            self.db.query(Rule)
            .filter(Rule.scheme_id == scheme_id)
            .count()
        )