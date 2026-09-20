from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.services.eligibility_service import EligibilityService
from app.services.explanation_service import ExplanationService


router = APIRouter(
    prefix="/eligibility",
    tags=["Eligibility"]
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


# ---------------------------------------------------------
# Request Schemas
# ---------------------------------------------------------

class EligibilityRequest(BaseModel):
    """
    Citizen information used by the eligibility engine.

    Additional scheme-specific fields can also be supplied
    through the extra_data dictionary.
    """

    name: Optional[str] = None
    age: Optional[int] = Field(default=None, ge=0)
    gender: Optional[str] = None

    state: Optional[str] = None
    district: Optional[str] = None


    rural_urban: Optional[str] = None
    category: Optional[str] = None

    annual_income: Optional[float] = Field(default=None, ge=0)
    family_size: Optional[int] = Field(default=None, ge=1)

    employment_status: Optional[str] = None
    education_level: Optional[str] = None
    occupation: Optional[str] = None

    farmer: Optional[bool] = None
    land_ownership: Optional[bool] = None
    disability: Optional[bool] = None
    house_ownership: Optional[bool] = None
    bpl_status: Optional[bool] = None

    student_status: Optional[bool] = None
    street_vendor: Optional[bool] = None

    marital_status: Optional[str] = None

    extra_data: Dict[str, Any] = Field(default_factory=dict)


class SchemeEligibilityRequest(EligibilityRequest):
    """
    Request used when checking one particular scheme.
    """

    scheme_id: str


# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------

def build_profile(request: EligibilityRequest) -> Dict[str, Any]:
    """
    Convert the Pydantic request into the dictionary format
    expected by the services/rule engine.
    """

    profile = request.model_dump(
        exclude_none=True,
        exclude={"extra_data"}
    )

    # Add scheme-specific fields
    if request.extra_data:
        profile.update(request.extra_data)

    return profile


# ---------------------------------------------------------
# Check all relevant schemes
# ---------------------------------------------------------

@router.post("/check")
def check_eligibility(
    request: EligibilityRequest,
    db: Session = Depends(get_db)
):
    """
    Check the citizen against relevant government schemes.
    """

    profile = build_profile(request)

    try:
        service = EligibilityService(db)

        results = service.check_eligibility(
            profile=profile,
            save_results=True
        )

        return {
            "success": True,
            "profile": profile,
            "total_schemes_checked": len(results),
            "results": results
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Eligibility checking failed: {str(exc)}"
        )


# ---------------------------------------------------------
# Check one specific scheme
# ---------------------------------------------------------

@router.post("/check-scheme")
def check_scheme_eligibility(
    request: SchemeEligibilityRequest,
    db: Session = Depends(get_db)
):
    """
    Check eligibility for one specific government scheme.
    """

    profile = build_profile(request)

    try:
        service = EligibilityService(db)

        result = service.check_scheme_eligibility(
            scheme_id=request.scheme_id,
            profile=profile,
            save_result=True
        )

        if not result:
            raise HTTPException(
                status_code=404,
                detail="Scheme not found."
            )

        return {
            "success": True,
            "result": result
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Scheme eligibility check failed: {str(exc)}"
        )


@router.post("/check/{scheme_id}")
def check_scheme_eligibility_by_path(
    scheme_id: str,
    request: EligibilityRequest,
    db: Session = Depends(get_db)
):
    """
    Check eligibility for one specific scheme passed via URL path.
    """
    profile = build_profile(request)

    try:
        service = EligibilityService(db)

        result = service.check_scheme_eligibility(
            scheme_id=scheme_id,
            profile=profile,
            save_result=True
        )

        if not result:
            raise HTTPException(
                status_code=404,
                detail="Scheme not found."
            )

        return {
            "success": True,
            "result": result
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Scheme eligibility check failed: {str(exc)}"
        )



# ---------------------------------------------------------
# Generate explanation
# ---------------------------------------------------------

@router.post("/explain")
def explain_eligibility(
    request: SchemeEligibilityRequest,
    db: Session = Depends(get_db)
):
    """
    Check eligibility and generate a human-readable explanation.
    """

    profile = build_profile(request)

    try:
        eligibility_service = EligibilityService(db)

        result = eligibility_service.check_scheme_eligibility(
            scheme_id=request.scheme_id,
            profile=profile,
            save_result=False
        )

        if not result:
            raise HTTPException(
                status_code=404,
                detail="Scheme not found."
            )

        explanation_service = ExplanationService(db)

        explanation = explanation_service.generate_explanation(
            scheme=result,
            eligibility_result=result,
            citizen_data=profile
        )

        return {
            "success": True,
            "scheme_id": request.scheme_id,
            "eligibility": result,
            "explanation": explanation
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Explanation generation failed: {str(exc)}"
        )