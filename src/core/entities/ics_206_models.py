from typing import List, Optional
from datetime import date, time

from sqlalchemy import Time
from sqlmodel import Field, Relationship, SQLModel


class Ics206(SQLModel, table=True):
    __tablename__ = "ics_206"

    id: int = Field(default=None, primary_key=True)
    operational_period_id: Optional[int] = Field(
        default=None, foreign_key="operational_period.id", ondelete="CASCADE"
    )
    special_medical_procedures: str
    is_utilized: Optional[bool]

    ics_206_medical_aid_station: List["Ics206MedicalAidStation"] = Relationship(
        back_populates="ics_206",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    ics_206_transportation: List["Ics206Transportation"] = Relationship(
        back_populates="ics_206",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    ics_206_hospitals: List["Ics206Hospitals"] = Relationship(
        back_populates="ics_206", 
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    ics_206_preparation: Optional["Ics206Preparation"] = Relationship(
        back_populates="ics_206",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    ics_206_approval: Optional["Ics206Approval"] = Relationship(
        back_populates="ics_206",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    operational_period: Optional["OperationalPeriod"] = Relationship(
        back_populates="ics_206"
    )


class Ics206MedicalAidStation(SQLModel, table=True):
    __tablename__ = "ics_206_medical_aid_station"

    id: int = Field(default=None, primary_key=True)
    ics_206_id: Optional[int] = Field(default=None, foreign_key="ics_206.id", ondelete="CASCADE")
    name: str
    location: str
    number: str
    is_paramedic: Optional[bool]

    ics_206: Optional["Ics206"] = Relationship(back_populates="ics_206_medical_aid_station")


class Ics206Transportation(SQLModel, table=True):
    __tablename__ = "ics_206_transportation"

    id: int = Field(default=None, primary_key=True)
    ics_206_id: Optional[int] = Field(default=None, foreign_key="ics_206.id", ondelete="CASCADE")
    ambulance_sercvice: str
    location: str
    number: str
    is_als: Optional[bool]
    is_bls: Optional[bool]

    ics_206: Optional["Ics206"] = Relationship(back_populates="ics_206_transportation")


class Ics206Hospitals(SQLModel, table=True):
    __tablename__ = "ics_206_hospitals"

    id: int = Field(default=None, primary_key=True)
    ics_206_id: Optional[int] = Field(default=None, foreign_key="ics_206.id", ondelete="CASCADE")
    name: str
    address: str
    number: str
    air_travel_time: Optional[str]
    ground_travel_time: Optional[str]
    is_trauma_center: Optional[bool]
    level_trauma_center: Optional[str]
    is_burn_center: Optional[bool]
    is_helipad: Optional[bool]

    ics_206: Optional["Ics206"] = Relationship(back_populates="ics_206_hospitals")


class Ics206Preparation(SQLModel, table=True):
    __tablename__ = "ics_206_preparation"

    id: int = Field(default=None, primary_key=True)
    ics_206_id: Optional[int] = Field(default=None, foreign_key="ics_206.id", ondelete="CASCADE")
    medical_unit_leader_id: Optional[int] = Field(
        default=None, foreign_key="medical_unit_leader.id", ondelete="CASCADE"
    )
    is_prepared: bool
    date_prepared: Optional[date]
    time_prepared: Optional[time] = Field(sa_column=Field(sa_type=Time))

    medical_unit_leader: Optional["MedicalUnitLeader"] = Relationship(
        back_populates="ics_206_preparation"
    )
    ics_206: Optional["Ics206"] = Relationship(back_populates="ics_206_preparation")


class Ics206Approval(SQLModel, table=True):
    __tablename__ = "ics_206_approval"

    id: int = Field(default=None, primary_key=True)
    ics_206_id: Optional[int] = Field(default=None, foreign_key="ics_206.id", ondelete="CASCADE")
    safety_officer_id: Optional[int] = Field(
        default=None, foreign_key="safety_officer.id", ondelete="CASCADE"
    )
    is_approved: bool
    date_approved: Optional[date]
    time_approved: Optional[time] = Field(sa_column=Field(sa_type=Time))

    safety_officer: Optional["SafetyOfficer"] = Relationship(
        back_populates="ics_206_approval"
    )
    ics_206: Optional["Ics206"] = Relationship(back_populates="ics_206_approval")
