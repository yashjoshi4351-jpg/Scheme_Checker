from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class SchemeBase(BaseModel):
    """
    Common scheme information.
    """

    name: str
    description: Optional[str] = None
    department: Optional[str] = None
    state: Optional[str] = None
    benefits: Optional[str] = None


class SchemeResponse(SchemeBase):
    """
    Scheme returned by the API.
    """

    id: int

    model_config = ConfigDict(
        from_attributes=True
    )


class SchemeSummary(BaseModel):
    """
    Lightweight scheme information used in lists,
    recommendations and eligibility results.
    """

    id: int
    name: str
    department: Optional[str] = None
    state: Optional[str] = None
    benefits: Optional[str] = None


class SchemeListResponse(BaseModel):
    """
    Response containing multiple schemes.
    """

    total: int
    schemes: List[SchemeSummary]