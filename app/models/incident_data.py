from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy import Time
from datetime import date, time
from typing import Optional, List
from app.models.ics_201 import Ics201


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
        back_populates="incident_data"
    )
    ics_201: List["Ics201"] = Relationship(back_populates="incident_data")


class OperationalPeriod(SQLModel, table=True):
    __tablename__ = "operational_period"
    
    id: int = Field(default=None, primary_key=True)
    incident_id : Optional[int] = Field(default=None, foreign_key="incident_data.id")
    date_from: date
    time_from: time = Field(sa_column=Field(sa_type=Time))
    date_to: date
    time_to: time = Field(sa_column=Field(sa_type=Time))
    remarks: str
    
    # Relasi ke IncidentData
    incident_data: Optional[IncidentData] = Relationship(
        back_populates="operational_period"
    )
