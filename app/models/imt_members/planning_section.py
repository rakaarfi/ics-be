from sqlmodel import Relationship
from typing import List

from app.models.base_imt import BaseImtMember
from app.models.roster import ImtRoster
from app.models.ics_201 import IcsChart


class PlanningSectionChief(BaseImtMember, table=True):
    __tablename__ = "planning_section_chief"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="planning_section_chief")
    ics_chart: List[IcsChart] = Relationship(back_populates="planning_section_chief")
    
    
class SituationUnitLeader(BaseImtMember, table=True):
    __tablename__ = "situation_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="situation_unit_leader")
    ics_chart: List[IcsChart] = Relationship(back_populates="situation_unit_leader")
    
    
class ResourcesUnitLeader(BaseImtMember, table=True):
    __tablename__ = "resources_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="resources_unit_leader")
    ics_chart: List[IcsChart] = Relationship(back_populates="resources_unit_leader")
    
    
class DocumentationUnitLeader(BaseImtMember, table=True):
    __tablename__ = "documentation_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="documentation_unit_leader")
    ics_chart: List[IcsChart] = Relationship(back_populates="documentation_unit_leader")
    
    
class DemobilizationUnitLeader(BaseImtMember, table=True):
    __tablename__ = "demobilization_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="demobilization_unit_leader")
    ics_chart: List[IcsChart] = Relationship(back_populates="demobilization_unit_leader")
    
    
class EnvironmentalUnitLeader(BaseImtMember, table=True):
    __tablename__ = "environmental_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="environmental_unit_leader")
    ics_chart: List[IcsChart] = Relationship(back_populates="environmental_unit_leader")
    
    
class TechnicalSpecialist(BaseImtMember, table=True):
    __tablename__ = "technical_specialist"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="technical_specialist")
    ics_chart: List[IcsChart] = Relationship(back_populates="technical_specialist")
    