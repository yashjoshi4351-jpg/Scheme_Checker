from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database import crud
from app.services.eligibility_service import EligibilityService


router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
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
# Profile schema
# ---------------------------------------------------------

class CitizenProfile(BaseModel):
    name: Optional[str] = "Citizen"
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


# ---------------------------------------------------------
# History routes (MUST be defined before /{user_id})
# ---------------------------------------------------------

@router.get("/history")
def get_history(
    db: Session = Depends(get_db)
):
    """
    Retrieve past eligibility check history.
    """
    try:
        results = crud.get_all_eligibility_results(db)
        history_list = []
        for item in results:
            scheme_name = item.scheme.name if item.scheme else f"Scheme #{item.scheme_id}"
            scheme_code = item.scheme.scheme_id if item.scheme else str(item.scheme_id)

            history_list.append({
                "id": item.id,
                "history_id": item.id,
                "scheme_id": scheme_code,
                "scheme_name": scheme_name,
                "status": item.status,
                "eligible": item.status == "eligible",
                "reason": item.reason,
                "checked_at": item.checked_at.isoformat() if item.checked_at else None,
                "date": item.checked_at.isoformat() if item.checked_at else None,
                "created_at": item.checked_at.isoformat() if item.checked_at else None,
                "scheme_count": 1,
            })

        return {
            "success": True,
            "count": len(history_list),
            "history": history_list
        }
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve history: {str(exc)}"
        )


@router.delete("/history/{history_id}")
def delete_history(
    history_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a history record.
    """
    try:
        deleted = crud.delete_eligibility_result(db, history_id)
        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="History record not found."
            )
        return {
            "success": True,
            "message": "History record deleted successfully."
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to delete history record: {str(exc)}"
        )


# ---------------------------------------------------------
# Create profile
# ---------------------------------------------------------

@router.post("")
def create_profile(
    profile: CitizenProfile,
    db: Session = Depends(get_db)
):
    """
    Create a citizen profile in the database.
    """

    data = profile.model_dump(
        exclude_none=True,
        exclude={"extra_data"}
    )

    if profile.extra_data:
        data.update(profile.extra_data)

    try:
        user = crud.create_user(
            db=db,
            user_data=data
        )

        return {
            "success": True,
            "message": "Citizen profile created successfully.",
            "user": user
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to create profile: {str(exc)}"
        )


# ---------------------------------------------------------
# Get profile
# ---------------------------------------------------------

@router.get("/{user_id}")
def get_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a citizen profile.
    """

    try:
        user = crud.get_user(
            db=db,
            user_id=user_id
        )

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="Citizen profile not found."
            )

        return {
            "success": True,
            "profile": user
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to retrieve profile: {str(exc)}"
        )


# ---------------------------------------------------------
# Update profile
# ---------------------------------------------------------

@router.put("/{user_id}")
def update_profile(
    user_id: int,
    profile: CitizenProfile,
    db: Session = Depends(get_db)
):
    """
    Update a citizen profile.
    """
    data = profile.model_dump(
        exclude_none=True,
        exclude={"extra_data"}
    )
    if profile.extra_data:
        data.update(profile.extra_data)

    try:
        user = crud.update_user(
            db=db,
            user_id=user_id,
            user_data=data
        )
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="Citizen profile not found."
            )
        return {
            "success": True,
            "message": "Citizen profile updated successfully.",
            "profile": user
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to update profile: {str(exc)}"
        )


# ---------------------------------------------------------
# Check eligibility using stored profile
# ---------------------------------------------------------

@router.get("/{user_id}/eligibility")
def check_profile_eligibility(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Run the stored citizen profile through the eligibility service.
    """

    try:
        service = EligibilityService(db)

        results = service.check_user_eligibility(
            user_id=user_id,
            save_results=True
        )

        return {
            "success": True,
            "user_id": user_id,
            "total_schemes_checked": len(results),
            "results": results
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to check profile eligibility: {str(exc)}"
        )