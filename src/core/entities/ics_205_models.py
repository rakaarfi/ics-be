from datetime import date, time
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Ics205(SQLModel, table=True):
    __tablename__ = "ics_205"

    id: int = Field(default=None, primary_key=True)
    operational_period_id: Optional[int] = Field(
        default=None, foreign_key="operational_period.id", ondelete="CASCADE"
    )
    special_instructions: str

    ics_205_radio_channel: List["Ics205RadioChannel"] = Relationship(back_populates="ics_205", 
        sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    ics_205_preparation: Optional["Ics205Preparation"] = Relationship(
        back_populates="ics_205", 
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    operational_period: Optional["OperationalPeriod"] = Relationship(
        back_populates="ics_205"
    )


class Ics205RadioChannel(SQLModel, table=True):
    __tablename__ = "ics_205_radio_channel"

    id: int = Field(default=None, primary_key=True)
    ics_205_id: Optional[int] = Field(default=None, foreign_key="ics_205.id", ondelete="CASCADE")
    channel_number: str
    channel_name: str
    frequency: str
    mode: str
    functions: str
    assignment: str
    remarks: str

    ics_205: Optional["Ics205"] = Relationship(back_populates="ics_205_radio_channel")


class Ics205Preparation(SQLModel, table=True):
    __tablename__ = "ics_205_preparation"

    id: int = Field(default=None, primary_key=True)
    ics_205_id: Optional[int] = Field(default=None, foreign_key="ics_205.id", ondelete="CASCADE")
    communication_unit_leader_id: Optional[int] = Field(
        default=None, foreign_key="communication_unit_leader.id", ondelete="CASCADE"
    )
    is_prepared: bool
    date_prepared: Optional[date]
    time_prepared: Optional[time]

    communication_unit_leader: Optional["CommunicationUnitLeader"] = Relationship(
        back_populates="ics_205_preparation"
    )
    ics_205: Optional["Ics205"] = Relationship(back_populates="ics_205_preparation")
