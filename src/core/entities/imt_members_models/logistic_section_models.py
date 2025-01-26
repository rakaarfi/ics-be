from typing import List

from sqlmodel import Relationship

from src.core.entities.base_imt_models import BaseImtMember
from src.core.entities.ics_201_models import IcsChart
from src.core.entities.ics_203_models import Ics203
from src.core.entities.ics_205_models import Ics205Preparation
from src.core.entities.ics_206_models import Ics206Preparation
from src.core.entities.roster_models import ImtRoster


class LogisticSectionChief(BaseImtMember, table=True):
    __tablename__ = "logistic_section_chief"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="logistic_section_chief")
    ics_chart: List[IcsChart] = Relationship(back_populates="logistic_section_chief")
    ics_203: List[Ics203] = Relationship(back_populates="logistic_section_chief")


class CommunicationUnitLeader(BaseImtMember, table=True):
    __tablename__ = "communication_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="communication_unit_leader"
    )
    ics_chart: List[IcsChart] = Relationship(back_populates="communication_unit_leader")
    ics_203: List[Ics203] = Relationship(back_populates="communication_unit_leader")
    ics_205_preparation: List[Ics205Preparation] = Relationship(
        back_populates="communication_unit_leader"
    )


class MedicalUnitLeader(BaseImtMember, table=True):
    __tablename__ = "medical_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="medical_unit_leader")
    ics_chart: List[IcsChart] = Relationship(back_populates="medical_unit_leader")
    ics_203: List[Ics203] = Relationship(back_populates="medical_unit_leader")
    ics_206_preparation: List[Ics206Preparation] = Relationship(
        back_populates="medical_unit_leader"
    )


class FoodUnitLeader(BaseImtMember, table=True):
    __tablename__ = "food_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="food_unit_leader")
    ics_chart: List[IcsChart] = Relationship(back_populates="food_unit_leader")
    ics_203: List[Ics203] = Relationship(back_populates="food_unit_leader")


class FacilityUnitLeader(BaseImtMember, table=True):
    __tablename__ = "facility_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="facility_unit_leader")
    ics_chart: List[IcsChart] = Relationship(back_populates="facility_unit_leader")
    ics_203: List[Ics203] = Relationship(back_populates="facility_unit_leader")


class SupplyUnitLeader(BaseImtMember, table=True):
    __tablename__ = "supply_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="supply_unit_leader")
    ics_chart: List[IcsChart] = Relationship(back_populates="supply_unit_leader")
    ics_203: List[Ics203] = Relationship(back_populates="supply_unit_leader")


class TransportationUnitLeader(BaseImtMember, table=True):
    __tablename__ = "transportation_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="transportation_unit_leader"
    )
    ics_chart: List[IcsChart] = Relationship(
        back_populates="transportation_unit_leader"
    )
    ics_203: List[Ics203] = Relationship(back_populates="transportation_unit_leader")
