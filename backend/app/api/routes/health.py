from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.database import SessionLocal


router = APIRouter(
    prefix="/health",
    tags=["Health"]
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
# Basic health check
# ---------------------------------------------------------

@router.get("")
def health_check():
    """
    Basic API health check.
    """

    return {
        "status": "healthy",
        "service": "Government Scheme Eligibility Checker",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# ---------------------------------------------------------
# Database health check
# ---------------------------------------------------------

@router.get("/database")
def database_health_check(
    db: Session = Depends(get_db)
):
    """
    Check whether the application can communicate with
    the configured database.
    """

    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as exc:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(exc)
        }