from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database import crud

from app.engine.condition_evaluator import ConditionEvaluator
from app.engine.rule_registry import RuleRegistry
from app.engine.rule_engine import RuleEngine

from app.services.eligibility_service import EligibilityService
from app.services.scheme_service import SchemeService
from app.services.recommendation_service import RecommendationService


# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------

def get_database():
    """
    FastAPI dependency for database sessions.
    """
    yield from get_db()


# ---------------------------------------------------------
# USER
# ---------------------------------------------------------

def get_user(
    user_id: int,
    db: Session = Depends(get_database),
):
    user = crud.get_user_by_id(
        db,
        user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    return user


# ---------------------------------------------------------
from typing import Union

def get_scheme(
    scheme_id: Union[int, str],
    db: Session = Depends(get_database),
):
    scheme = crud.get_scheme(
        db,
        scheme_id,
    )


    if scheme is None:
        raise HTTPException(
            status_code=404,
            detail="Scheme not found.",
        )

    return scheme


# ---------------------------------------------------------
# CONDITION EVALUATOR
# ---------------------------------------------------------

def get_condition_evaluator():
    return ConditionEvaluator()


# ---------------------------------------------------------
# RULE REGISTRY
# ---------------------------------------------------------

def get_rule_registry(
    db: Session = Depends(get_database),
):
    return RuleRegistry(db=db)


# ---------------------------------------------------------
# RULE ENGINE
# ---------------------------------------------------------

def get_rule_engine(
    evaluator: ConditionEvaluator = Depends(
        get_condition_evaluator
    ),
    registry: RuleRegistry = Depends(
        get_rule_registry
    ),
):
    return RuleEngine(
        evaluator=evaluator,
        registry=registry,
    )


# ---------------------------------------------------------
# ELIGIBILITY SERVICE
# ---------------------------------------------------------

def get_eligibility_service(
    db: Session = Depends(get_database),
    rule_engine: RuleEngine = Depends(
        get_rule_engine
    ),
):
    return EligibilityService(
        db=db,
        rule_engine=rule_engine,
    )


# ---------------------------------------------------------
# SCHEME SERVICE
# ---------------------------------------------------------

def get_scheme_service(
    db: Session = Depends(get_database),
):
    return SchemeService(
        db=db,
    )


# ---------------------------------------------------------
# RECOMMENDATION SERVICE
# ---------------------------------------------------------

def get_recommendation_service(
    db: Session = Depends(get_database),
    rule_engine: RuleEngine = Depends(
        get_rule_engine
    ),
):
    return RecommendationService(
        db=db,
        rule_engine=rule_engine,
    )