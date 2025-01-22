from sqlmodel import Relationship
from typing import List

from app.models.base_imt import BaseImtMember
from app.models.roster import ImtRoster
from app.models.ics_201 import IcsChart


class LogisticSectionChief(BaseImtMember, table=True):
    __tablename__ = "logistic_section_chief"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="logistic_section_chief")
    ics_chart: List[IcsChart] = Relationship(back_populates="logistic_section_chief")


class CommunicationUnitLeader(BaseImtMember, table=True):
    __tablename__ = "communication_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="communication_unit_leader")
    ics_chart: List[IcsChart] = Relationship(back_populates="communication_unit_leader")
    
    
class MedicalUnitLeader(BaseImtMember, table=True):
    __tablename__ = "medical_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="medical_unit_leader")
    ics_chart: List[IcsChart] = Relationship(back_populates="medical_unit_leader")
    
    
class FoodUnitLeader(BaseImtMember, table=True):
    __tablename__ = "food_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="food_unit_leader")
    ics_chart: List[IcsChart] = Relationship(back_populates="food_unit_leader")
    
    
class FacilityUnitLeader(BaseImtMember, table=True):
    __tablename__ = "facility_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="facility_unit_leader")
    ics_chart: List[IcsChart] = Relationship(back_populates="facility_unit_leader")
    
    
class SupplyUnitLeader(BaseImtMember, table=True):
    __tablename__ = "supply_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="supply_unit_leader")
    ics_chart: List[IcsChart] = Relationship(back_populates="supply_unit_leader")
    
    
class TransportationUnitLeader(BaseImtMember, table=True):
    __tablename__ = "transportation_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="transportation_unit_leader")
    ics_chart: List[IcsChart] = Relationship(back_populates="transportation_unit_leader")
