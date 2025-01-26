from datetime import date, time
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Ics204(SQLModel, table=True):
    __tablename__ = "ics_204"

    id: int = Field(default=None, primary_key=True)
    operational_period_id: Optional[int] = Field(
        default=None, foreign_key="operational_period.id"
    )
    operation_section_chief_name: str
    operation_section_chief_number: str
    branch_director_name: str
    branch_director_number: str
    division_supervisor_name: str
    division_supervisor_number: str
    branch: str
    division: str
    staging_area: str
    work_assignment: str
    special_instructions: str
    radio_channel_number: str
    frequency: str
    communication_mode: str
    mobile_phone: str

    personnel_assigned: List["PersonnelAssigned"] = Relationship(
        back_populates="ics_204"
    )
    equipment_assigned: List["EquipmentAssigned"] = Relationship(
        back_populates="ics_204"
    )
    ics_204_preparation: Optional["Ics204Preparation"] = Relationship(
        back_populates="ics_204"
    )
    operational_period: Optional["OperationalPeriod"] = Relationship(
        back_populates="ics_204"
    )


class PersonnelAssigned(SQLModel, table=True):
    __tablename__ = "personnel_assigned"

    id: int = Field(default=None, primary_key=True)
    ics_204_id: Optional[int] = Field(default=None, foreign_key="ics_204.id")
    name: str
    number: str
    location: str
    equipment_tools_remarks: str

    ics_204: Optional["Ics204"] = Relationship(back_populates="personnel_assigned")


class EquipmentAssigned(SQLModel, table=True):
    __tablename__ = "equipment_assigned"

    id: int = Field(default=None, primary_key=True)
    ics_204_id: Optional[int] = Field(default=None, foreign_key="ics_204.id")
    kind: str
    quantity: int
    type_specification: str
    number: str
    location: str
    remarks: str

    ics_204: Optional["Ics204"] = Relationship(back_populates="equipment_assigned")


class Ics204Preparation(SQLModel, table=True):
    __tablename__ = "ics_204_preparation"

    id: int = Field(default=None, primary_key=True)
    ics_204_id: Optional[int] = Field(default=None, foreign_key="ics_204.id")
    name: str
    is_prepared: bool
    date_prepared: Optional[date]
    time_prepared: Optional[time]

    ics_204: Optional["Ics204"] = Relationship(back_populates="ics_204_preparation")
