from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserProfileBase(BaseModel):
    """
    Citizen profile data used by the eligibility system.
    """

    age: Optional[int] = Field(
        default=None,
        ge=0,
        le=120
    )

    gender: Optional[str] = None

    state: Optional[str] = None

    district: Optional[str] = None

    category: Optional[str] = None

    annual_income: Optional[float] = Field(
        default=None,
        ge=0
    )

    family_size: Optional[int] = Field(
        default=None,
        ge=1
    )

    employment_status: Optional[str] = None

    education: Optional[str] = None

    occupation: Optional[str] = None

    is_farmer: Optional[bool] = None

    has_disability: Optional[bool] = None

    owns_house: Optional[bool] = None

    is_bpl: Optional[bool] = None


class UserProfileCreate(UserProfileBase):
    """
    Request schema for creating/updating a citizen profile.
    """
    pass


class UserProfileResponse(UserProfileBase):
    """
    API response schema for a citizen profile.
    """

    id: int

    model_config = ConfigDict(
        from_attributes=True
    )