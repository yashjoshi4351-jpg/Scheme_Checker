from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database.database import Base


class EligibilityResult(Base):
    __tablename__ = "eligibility_results"

    # ----------------------------------------------
    # Primary Key
    # ----------------------------------------------

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # ----------------------------------------------
    # Foreign Keys
    # ----------------------------------------------

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    scheme_id = Column(
        Integer,
        ForeignKey("schemes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    profile_snapshot = Column(
        Text,
        nullable=True
    )

    # ----------------------------------------------
    # Eligibility Result
    # ----------------------------------------------

    status = Column(
        String(30),
        nullable=False
    )

    reason = Column(
        Text,
        nullable=True
    )

    matched_rules = Column(
        Text,
        nullable=True
    )

    failed_rules = Column(
        Text,
        nullable=True
    )

    # ----------------------------------------------
    # Timestamp
    # ----------------------------------------------

    checked_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # ----------------------------------------------
    # Relationships
    # ----------------------------------------------

    user = relationship(
        "User",
        back_populates="eligibility_results"
    )

    scheme = relationship(
        "Scheme",
        back_populates="eligibility_results"
    )