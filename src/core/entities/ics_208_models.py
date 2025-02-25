from datetime import date, time
from typing import Optional

from sqlalchemy import Time
from sqlmodel import Field, Relationship, SQLModel


class Ics208(SQLModel, table=True):
    __tablename__ = "ics_208"

    id: int = Field(default=None, primary_key=True)
    operational_period_id: Optional[int] = Field(
        default=None, foreign_key="operational_period.id", ondelete="CASCADE"
    )
    message: str
    is_required: Optional[bool]
    site_safety_plan: Optional[str]
    additional_comments: Optional[str]

    ics_208_preparation: Optional["Ics208Preparation"] = Relationship(
        back_populates="ics_208",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    operational_period: Optional["OperationalPeriod"] = Relationship(
        back_populates="ics_208"
    )


class Ics208Preparation(SQLModel, table=True):
    __tablename__ = "ics_208_preparation"

    id: int = Field(default=None, primary_key=True)
    ics_208_id: Optional[int] = Field(default=None, foreign_key="ics_208.id", ondelete="CASCADE")
    safety_officer_id: Optional[int] = Field(
        default=None, foreign_key="safety_officer.id", ondelete="CASCADE"
    )
    is_prepared: bool
    date_prepared: Optional[date]
    time_prepared: Optional[time] = Field(sa_column=Field(sa_type=Time))

    safety_officer: Optional["SafetyOfficer"] = Relationship(
        back_populates="ics_208_preparation",
    )
    ics_208: Optional["Ics208"] = Relationship(back_populates="ics_208_preparation")
