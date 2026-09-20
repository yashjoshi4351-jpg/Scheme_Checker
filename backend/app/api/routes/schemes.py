from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.services.scheme_service import SchemeService


router = APIRouter(
    prefix="/schemes",
    tags=["Schemes"]
)


# ---------------------------------------------------------
# Database dependency
# ---------------------------------------------------------

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def serialize_scheme(scheme):
    if not scheme:
        return None
    if isinstance(scheme, dict):
        return scheme
    return {
        "id": scheme.id,
        "scheme_id": scheme.scheme_id,
        "name": scheme.name,
        "ministry": scheme.ministry,
        "department": scheme.ministry,
        "level": scheme.level,
        "description": scheme.description,
        "benefits": scheme.benefits,
        "application_url": scheme.application_url,
        "is_active": scheme.is_active,
    }


def serialize_rule(rule):
    if not rule:
        return None
    if isinstance(rule, dict):
        return rule
    return {
        "id": rule.id,
        "scheme_id": rule.scheme_id,
        "rule_id": rule.rule_id,
        "field": rule.field,
        "operator": rule.operator,
        "value": rule.value,
        "description": rule.description,
        "is_required": rule.is_required,
    }


# ---------------------------------------------------------
# Get all schemes
# ---------------------------------------------------------

@router.get("")
def get_schemes(
    state: Optional[str] = None,
    category: Optional[str] = None,
    occupation: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get government schemes.

    Supports:
    - search
    - state filtering
    - category filtering
    - occupation filtering
    """

    try:
        service = SchemeService(db)

        # If filters/search are supplied, use search_schemes()
        if any([
            search,
            state,
            category,
            occupation
        ]):
            schemes = service.search_schemes(
                query=search,
                state=state,
                category=category,
                occupation=occupation
            )
        else:
            schemes = service.get_all_schemes()

        serialized = [serialize_scheme(s) for s in schemes]

        return {
            "success": True,
            "count": len(serialized),
            "schemes": serialized
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve schemes: {str(exc)}"
        )


# ---------------------------------------------------------
# Get one scheme
# ---------------------------------------------------------

@router.get("/{scheme_id}")
def get_scheme(
    scheme_id: str,
    db: Session = Depends(get_db)
):
    """
    Get complete information about one scheme.
    """

    try:
        service = SchemeService(db)

        scheme = service.get_scheme(scheme_id)

        if scheme is None:
            raise HTTPException(
                status_code=404,
                detail=f"Scheme '{scheme_id}' not found."
            )

        return {
            "success": True,
            "scheme": serialize_scheme(scheme)
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve scheme: {str(exc)}"
        )


# ---------------------------------------------------------
# Get scheme rules
# ---------------------------------------------------------

@router.get("/{scheme_id}/rules")
def get_scheme_rules(
    scheme_id: str,
    db: Session = Depends(get_db)
):
    """
    Return the rules associated with a scheme.
    """

    try:
        service = SchemeService(db)

        # First verify that the scheme exists
        scheme = service.get_scheme(scheme_id)

        if scheme is None:
            raise HTTPException(
                status_code=404,
                detail=f"Scheme '{scheme_id}' not found."
            )

        rules = service.get_rules(scheme_id)

        return {
            "success": True,
            "scheme_id": scheme_id,
            "count": len(rules),
            "rules": [serialize_rule(r) for r in rules]
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve scheme rules: {str(exc)}"
        )