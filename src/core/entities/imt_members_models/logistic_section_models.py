from typing import List

from sqlmodel import Relationship

from src.core.entities.base_imt_models import BaseImtMember
from src.core.entities.ics_201_models import Ics201Chart
from src.core.entities.ics_203_models import Ics203
from src.core.entities.ics_205_models import Ics205Preparation
from src.core.entities.ics_206_models import Ics206Preparation
from src.core.entities.roster_models import ImtRoster


class LogisticSectionChief(BaseImtMember, table=True):
    __tablename__ = "logistic_section_chief"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="logistic_section_chief",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="logistic_section_chief",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="logistic_section_chief",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class CommunicationUnitLeader(BaseImtMember, table=True):
    __tablename__ = "communication_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="communication_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="communication_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="communication_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_205_preparation: List[Ics205Preparation] = Relationship(
        back_populates="communication_unit_leader", 
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class MedicalUnitLeader(BaseImtMember, table=True):
    __tablename__ = "medical_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="medical_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="medical_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="medical_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_206_preparation: List[Ics206Preparation] = Relationship(
        back_populates="medical_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class FoodUnitLeader(BaseImtMember, table=True):
    __tablename__ = "food_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="food_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="food_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="food_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class FacilityUnitLeader(BaseImtMember, table=True):
    __tablename__ = "facility_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="facility_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="facility_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="facility_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class SupplyUnitLeader(BaseImtMember, table=True):
    __tablename__ = "supply_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="supply_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="supply_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="supply_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class TransportationUnitLeader(BaseImtMember, table=True):
    __tablename__ = "transportation_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="transportation_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="transportation_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="transportation_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
