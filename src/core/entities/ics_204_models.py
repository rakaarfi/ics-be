from datetime import date, time
from typing import List, Optional

from sqlalchemy import Time
from sqlmodel import Field, Relationship, SQLModel


class Ics204(SQLModel, table=True):
    __tablename__ = "ics_204"

    id: int = Field(default=None, primary_key=True)
    operational_period_id: Optional[int] = Field(
        default=None, foreign_key="operational_period.id"
    )
    operation_section_chief_id: Optional[int] = Field(
        default=None, foreign_key="operation_section_chief.id"
    )
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

    ics_204_personnel_assigned: List["Ics204PersonnelAssigned"] = Relationship(
        back_populates="ics_204",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_204_equipment_assigned: List["Ics204EquipmentAssigned"] = Relationship(
        back_populates="ics_204",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_204_preparation_os_chief: Optional["Ics204PreparationOSChief"] = Relationship(
        back_populates="ics_204",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_204_preparation_ru_leader: Optional["Ics204PreparationRULeader"] = Relationship(
        back_populates="ics_204",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    operational_period: Optional["OperationalPeriod"] = Relationship(
        back_populates="ics_204"
    )
    operation_section_chief: Optional["OperationSectionChief"] = Relationship(
        back_populates="ics_204"
    )


class Ics204PersonnelAssigned(SQLModel, table=True):
    __tablename__ = "ics_204_personnel_assigned"

    id: int = Field(default=None, primary_key=True)
    ics_204_id: Optional[int] = Field(default=None, foreign_key="ics_204.id", ondelete="CASCADE")
    name: str
    number: str
    location: str
    equipment_tools_remarks: str

    ics_204: Optional["Ics204"] = Relationship(back_populates="ics_204_personnel_assigned")


class Ics204EquipmentAssigned(SQLModel, table=True):
    __tablename__ = "ics_204_equipment_assigned"

    id: int = Field(default=None, primary_key=True)
    ics_204_id: Optional[int] = Field(default=None, foreign_key="ics_204.id", ondelete="CASCADE")
    kind: str
    quantity: int
    type_specification: str
    number: str
    location: str
    remarks: str

    ics_204: Optional["Ics204"] = Relationship(back_populates="ics_204_equipment_assigned")


class Ics204PreparationRULeader(SQLModel, table=True):
    __tablename__ = "ics_204_preparation_ru_leader"

    id: int = Field(default=None, primary_key=True)
    ics_204_id: Optional[int] = Field(default=None, foreign_key="ics_204.id", ondelete="CASCADE")
    resources_unit_leader_id: Optional[int] = Field(
        default=None, foreign_key="resources_unit_leader.id", ondelete="CASCADE"
    )
    is_prepared: bool
    date_prepared: Optional[date]
    time_prepared: Optional[time] = Field(sa_column=Field(sa_type=Time))

    resources_unit_leader : Optional["ResourcesUnitLeader"] = Relationship(
        back_populates="ics_204_preparation_ru_leader"
    )
    ics_204: Optional["Ics204"] = Relationship(back_populates="ics_204_preparation_ru_leader")


class Ics204PreparationOSChief(SQLModel, table=True):
    __tablename__ = "ics_204_preparation_os_chief"

    id: int = Field(default=None, primary_key=True)
    ics_204_id: Optional[int] = Field(default=None, foreign_key="ics_204.id", ondelete="CASCADE")
    operation_section_chief_id: Optional[int] = Field(
        default=None, foreign_key="operation_section_chief.id", ondelete="CASCADE"
    )
    is_prepared: bool
    date_prepared: Optional[date]
    time_prepared: Optional[time] = Field(sa_column=Field(sa_type=Time))

    operation_section_chief : Optional["OperationSectionChief"] = Relationship(
        back_populates="ics_204_preparation_os_chief"
    )
    ics_204: Optional["Ics204"] = Relationship(back_populates="ics_204_preparation_os_chief")