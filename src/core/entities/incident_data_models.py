from datetime import date, time
from typing import List, Optional

from sqlalchemy import Time
from pydantic import field_validator
from sqlmodel import Column, Field, Relationship, SQLModel

from src.core.entities.ics_201_models import Ics201
from src.core.entities.ics_202_models import Ics202
from src.core.entities.ics_203_models import Ics203
from src.core.entities.ics_204_models import Ics204
from src.core.entities.ics_205_models import Ics205
from src.core.entities.ics_206_models import Ics206
from src.core.entities.ics_208_models import Ics208


class IncidentData(SQLModel, table=True):
    __tablename__ = "incident_data"

    id: int = Field(default=None, primary_key=True)
    no: str
    name: str
    date_incident: date
    time_incident: time = Field(sa_column=Column(Time))
    timezone: str
    location: str
    description: str

    # Relasi ke OperationalPeriod
    operational_period: List["OperationalPeriod"] = Relationship(
        back_populates="incident_data",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201: List["Ics201"] = Relationship(
        back_populates="incident_data",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class OperationalPeriod(SQLModel, table=True):
    __tablename__ = "operational_period"

    id: int = Field(default=None, primary_key=True)
    incident_id: Optional[int] = Field(default=None, foreign_key="incident_data.id", ondelete="CASCADE")
    date_from: date
    time_from: time = Field(sa_column=Field(sa_type=Time))
    date_to: date
    time_to: time = Field(sa_column=Field(sa_type=Time))
    remarks: str

    # Relasi ke IncidentData
    incident_data: Optional[IncidentData] = Relationship(
        back_populates="operational_period"
    )

    ics_202: List["Ics202"] = Relationship(
        back_populates="operational_period", 
        sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    ics_203: List["Ics203"] = Relationship(
        back_populates="operational_period", 
        sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    ics_204: List["Ics204"] = Relationship(
        back_populates="operational_period", 
        sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    ics_205: List["Ics205"] = Relationship(
        back_populates="operational_period", 
        sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    ics_206: List["Ics206"] = Relationship(
        back_populates="operational_period", 
        sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    ics_208: List["Ics208"] = Relationship(
        back_populates="operational_period", 
        sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    
    @field_validator("date_to")
    @classmethod
    def check_date_to(cls, value: date, values) -> date:
        if value and "date_from" in values.data and value > values.data["date_from"]:
            raise ValueError("Date to cannot be earlier than date from")
        return value
