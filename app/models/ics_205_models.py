from datetime import date, time
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Ics205(SQLModel, table=True):
    __tablename__ = "ics_205"

    id: int = Field(default=None, primary_key=True)
    operational_period_id: Optional[int] = Field(
        default=None, foreign_key="operational_period.id"
    )
    special_instructions: str

    radio_channel: List["RadioChannel"] = Relationship(back_populates="ics_205")
    ics_205_preparation: Optional["Ics205Preparation"] = Relationship(
        back_populates="ics_205"
    )
    operational_period: Optional["OperationalPeriod"] = Relationship(
        back_populates="ics_205"
    )


class RadioChannel(SQLModel, table=True):
    __tablename__ = "radio_channel"

    id: int = Field(default=None, primary_key=True)
    ics_205_id: Optional[int] = Field(default=None, foreign_key="ics_205.id")
    channel_number: str
    channel_name: str
    frequency: str
    mode: str
    functions: str
    assignment: str
    remarks: str

    ics_205: Optional["Ics205"] = Relationship(back_populates="radio_channel")


class Ics205Preparation(SQLModel, table=True):
    __tablename__ = "ics_205_preparation"

    id: int = Field(default=None, primary_key=True)
    ics_205_id: Optional[int] = Field(default=None, foreign_key="ics_205.id")
    communication_unit_leader_id: Optional[int] = Field(
        default=None, foreign_key="communication_unit_leader.id"
    )
    is_prepared: bool
    date_prepared: Optional[date]
    time_prepared: Optional[time]

    communication_unit_leader: Optional["CommunicationUnitLeader"] = Relationship(
        back_populates="ics_205_preparation"
    )
    ics_205: Optional["Ics205"] = Relationship(back_populates="ics_205_preparation")
