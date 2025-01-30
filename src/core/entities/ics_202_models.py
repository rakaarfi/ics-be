from datetime import date, time
from typing import Optional

from sqlalchemy import Time
from sqlmodel import Field, Relationship, SQLModel


class Ics202(SQLModel, table=True):
    __tablename__ = "ics_202"

    id: int = Field(default=None, primary_key=True)
    operational_period_id: Optional[int] = Field(
        default=None, foreign_key="operational_period.id", ondelete="CASCADE"
    )
    objectives: str
    command_emphasis: str
    situational_awareness: str
    is_required: Optional[bool]
    safety_plan_location: Optional[str]
    ics_203: Optional[bool]
    ics_204: Optional[bool]
    ics_205: Optional[bool]
    ics_205a: Optional[bool]
    ics_206: Optional[bool]
    ics_207: Optional[bool]
    ics_208: Optional[bool]
    map_chart: Optional[bool]
    weather_tides_currents: Optional[bool]

    ics_202_preparation: Optional["Ics202Preparation"] = Relationship(
        back_populates="ics_202",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_202_approval: Optional["Ics202Approval"] = Relationship(
        back_populates="ics_202",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    operational_period: Optional["OperationalPeriod"] = Relationship(
        back_populates="ics_202"
    )


class Ics202Preparation(SQLModel, table=True):
    __tablename__ = "ics_202_preparation"

    id: int = Field(default=None, primary_key=True)
    ics_202_id: Optional[int] = Field(default=None, foreign_key="ics_202.id", ondelete="CASCADE")
    planning_section_chief_id: Optional[int] = Field(
        default=None, foreign_key="planning_section_chief.id", ondelete="CASCADE"
    )
    is_prepared: bool
    date_prepared: Optional[date]
    time_prepared: Optional[time] = Field(sa_column=Field(sa_type=Time))

    planning_section_chief: Optional["PlanningSectionChief"] = Relationship(
        back_populates="ics_202_preparation"
    )
    ics_202: Optional["Ics202"] = Relationship(back_populates="ics_202_preparation")


class Ics202Approval(SQLModel, table=True):
    __tablename__ = "ics_202_approval"

    id: int = Field(default=None, primary_key=True)
    ics_202_id: Optional[int] = Field(default=None, foreign_key="ics_202.id", ondelete="CASCADE")
    incident_commander_id: Optional[int] = Field(
        default=None, foreign_key="incident_commander.id", ondelete="CASCADE"
    )
    is_approved: bool
    date_approved: Optional[date]
    time_approved: Optional[time] = Field(sa_column=Field(sa_type=Time))

    incident_commander: Optional["IncidentCommander"] = Relationship(
        back_populates="ics_202_approval"
    )
    ics_202: Optional["Ics202"] = Relationship(back_populates="ics_202_approval")
