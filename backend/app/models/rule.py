from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Boolean
)

from sqlalchemy.orm import relationship

from app.database.database import Base


class Rule(Base):
    __tablename__ = "rules"

    # ----------------------------------------------
    # Primary Key
    # ----------------------------------------------

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # ----------------------------------------------
    # Foreign Key
    # ----------------------------------------------

    scheme_id = Column(
        Integer,
        ForeignKey("schemes.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # ----------------------------------------------
    # Rule Information
    # ----------------------------------------------

    rule_id = Column(
        String(100),
        nullable=False
    )

    field = Column(
        String(100),
        nullable=False
    )

    operator = Column(
        String(30),
        nullable=False
    )

    value = Column(
        Text,
        nullable=True
    )

    description = Column(
        Text,
        nullable=True
    )

    is_required = Column(
        Boolean,
        default=True
    )

    # ----------------------------------------------
    # Relationship
    # ----------------------------------------------

    scheme = relationship(
        "Scheme",
        back_populates="rules"
    )