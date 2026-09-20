from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime
)

from sqlalchemy.orm import relationship

from app.database.database import Base


class Scheme(Base):
    __tablename__ = "schemes"

    # ----------------------------------------------
    # Primary Key
    # ----------------------------------------------

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # ----------------------------------------------
    # Scheme Identification
    # ----------------------------------------------

    scheme_id = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    name = Column(
        String(250),
        nullable=False
    )

    ministry = Column(
        String(250),
        nullable=True
    )

    level = Column(
        String(50),
        nullable=True
    )

    # ----------------------------------------------
    # Scheme Information
    # ----------------------------------------------

    description = Column(
        Text,
        nullable=True
    )

    benefits = Column(
        Text,
        nullable=True
    )

    application_url = Column(
        String(500),
        nullable=True
    )

    # ----------------------------------------------
    # Status
    # ----------------------------------------------

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # ----------------------------------------------
    # Relationships
    # ----------------------------------------------

    rules = relationship(
        "Rule",
        back_populates="scheme",
        cascade="all, delete-orphan"
    )

    eligibility_results = relationship(
        "EligibilityResult",
        back_populates="scheme",
        cascade="all, delete-orphan"
    )