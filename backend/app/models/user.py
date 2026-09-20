from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text
from sqlalchemy.orm import relationship

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    # ----------------------------------------------
    # Primary Key
    # ----------------------------------------------

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # ----------------------------------------------
    # Citizen Information
    # ----------------------------------------------

    name = Column(
        String(150),
        nullable=True,
        default="Citizen"
    )

    age = Column(
        Integer,
        nullable=True
    )

    gender = Column(
        String(20),
        nullable=True
    )

    state = Column(
        String(100),
        nullable=True
    )

    district = Column(
        String(100),
        nullable=True
    )

    rural_urban = Column(
        String(50),
        nullable=True
    )

    category = Column(
        String(50),
        nullable=True
    )

    annual_income = Column(
        Float,
        nullable=True
    )

    family_size = Column(
        Integer,
        nullable=True
    )

    employment_status = Column(
        String(100),
        nullable=True
    )

    education_level = Column(
        String(100),
        nullable=True
    )

    occupation = Column(
        String(100),
        nullable=True
    )

    marital_status = Column(
        String(50),
        nullable=True
    )

    farmer = Column(
        Boolean,
        default=False
    )

    land_ownership = Column(
        Boolean,
        default=False
    )

    disability = Column(
        Boolean,
        default=False
    )

    house_ownership = Column(
        Boolean,
        default=False
    )

    bpl_status = Column(
        Boolean,
        default=False
    )

    student_status = Column(
        Boolean,
        default=False
    )

    street_vendor = Column(
        Boolean,
        default=False
    )

    minority = Column(
        Boolean,
        default=False
    )

    extra_data = Column(
        Text,
        nullable=True
    )


    # ----------------------------------------------
    # Timestamp
    # ----------------------------------------------

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # ----------------------------------------------
    # Relationship
    # ----------------------------------------------

    eligibility_results = relationship(
        "EligibilityResult",
        back_populates="user",
        cascade="all, delete-orphan"
    )