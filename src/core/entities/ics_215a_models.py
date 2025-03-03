from datetime import date, time
from typing import List, Optional

from sqlalchemy import Time, BigInteger
from sqlmodel import Field, Relationship, SQLModel

class Ics215A(SQLModel, table=True):
    __tablename__ = "ics_215a"

    id: int = Field(default=None, primary_key=True)
    operational_period_id: Optional[int] = Field(
        default=None, foreign_key="operational_period.id", ondelete="CASCADE"
    )

    ics_215a_sub_form: List["Ics215ASubForm"] = Relationship(
        back_populates="ics_215a",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_215a_preparation_safety_officer: Optional["Ics215APreparationSafetyOfficer"] = Relationship(
        back_populates="ics_215a",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_215a_preparation_os_chief: Optional["Ics215APreparationOSChief"] = Relationship(
        back_populates="ics_215a",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    operational_period: Optional["OperationalPeriod"] = Relationship(
        back_populates="ics_215a"
    )


class Ics215ASubForm(SQLModel, table=True):
    __tablename__ = "ics_215a_sub_form"

    id: int = Field(default=None, primary_key=True)
    ics_215a_id: Optional[int] = Field(default=None, foreign_key="ics_215a.id", ondelete="CASCADE")
    incident_area: str
    hazards_risks: str
    mitigations: str
    
    ics_215a: Optional["Ics215A"] = Relationship(back_populates="ics_215a_sub_form")


class Ics215APreparationSafetyOfficer(SQLModel, table=True):
    __tablename__ = "ics_215a_preparation_safety_officer"

    id: int = Field(default=None, primary_key=True)
    ics_215a_id: Optional[int] = Field(default=None, foreign_key="ics_215a.id", ondelete="CASCADE")
    safety_officer_id: Optional[int] = Field(
        default=None, foreign_key="safety_officer.id", ondelete="CASCADE"
    )
    is_prepared: bool
    date_prepared: Optional[date]
    time_prepared: Optional[time] = Field(sa_column=Field(sa_type=Time))
    
    safety_officer: Optional["SafetyOfficer"] = Relationship(
        back_populates="ics_215a_preparation_safety_officer"
    )
    ics_215a: Optional["Ics215A"] = Relationship(back_populates="ics_215a_preparation_safety_officer")
    
    
class Ics215APreparationOSChief(SQLModel, table=True):
    __tablename__ = "ics_215a_preparation_os_chief"

    id: int = Field(default=None, primary_key=True)
    ics_215a_id: Optional[int] = Field(default=None, foreign_key="ics_215a.id", ondelete="CASCADE")
    operation_section_chief_id: Optional[int] = Field(
        default=None, foreign_key="operation_section_chief.id", ondelete="CASCADE"
    )
    is_prepared: bool
    date_prepared: Optional[date]
    time_prepared: Optional[time] = Field(sa_column=Field(sa_type=Time))
    
    operation_section_chief : Optional["OperationSectionChief"] = Relationship(
        back_populates="ics_215a_preparation_os_chief"
    )
    ics_215a: Optional["Ics215A"] = Relationship(back_populates="ics_215a_preparation_os_chief")
    