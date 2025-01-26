from typing import List, Optional

from sqlmodel import Relationship

from src.core.entities.base_imt_models import BaseImtMember
from src.core.entities.ics_201_models import IcsChart
from src.core.entities.ics_202_models import Ics202Preparation
from src.core.entities.ics_203_models import Ics203
from src.core.entities.roster_models import ImtRoster


class PlanningSectionChief(BaseImtMember, table=True):
    __tablename__ = "planning_section_chief"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="planning_section_chief")
    ics_chart: List[IcsChart] = Relationship(back_populates="planning_section_chief")
    ics_202_preparation: Optional[Ics202Preparation] = Relationship(
        back_populates="planning_section_chief"
    )
    ics_203: List[Ics203] = Relationship(back_populates="planning_section_chief")


class SituationUnitLeader(BaseImtMember, table=True):
    __tablename__ = "situation_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="situation_unit_leader")
    ics_chart: List[IcsChart] = Relationship(back_populates="situation_unit_leader")
    ics_203: List[Ics203] = Relationship(back_populates="situation_unit_leader")


class ResourcesUnitLeader(BaseImtMember, table=True):
    __tablename__ = "resources_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="resources_unit_leader")
    ics_chart: List[IcsChart] = Relationship(back_populates="resources_unit_leader")
    ics_203: List[Ics203] = Relationship(back_populates="resources_unit_leader")


class DocumentationUnitLeader(BaseImtMember, table=True):
    __tablename__ = "documentation_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="documentation_unit_leader"
    )
    ics_chart: List[IcsChart] = Relationship(back_populates="documentation_unit_leader")
    ics_203: List[Ics203] = Relationship(back_populates="documentation_unit_leader")


class DemobilizationUnitLeader(BaseImtMember, table=True):
    __tablename__ = "demobilization_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="demobilization_unit_leader"
    )
    ics_chart: List[IcsChart] = Relationship(
        back_populates="demobilization_unit_leader"
    )
    ics_203: List[Ics203] = Relationship(back_populates="demobilization_unit_leader")


class EnvironmentalUnitLeader(BaseImtMember, table=True):
    __tablename__ = "environmental_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="environmental_unit_leader"
    )
    ics_chart: List[IcsChart] = Relationship(back_populates="environmental_unit_leader")
    ics_203: List[Ics203] = Relationship(back_populates="environmental_unit_leader")


class TechnicalSpecialist(BaseImtMember, table=True):
    __tablename__ = "technical_specialist"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="technical_specialist")
    ics_chart: List[IcsChart] = Relationship(back_populates="technical_specialist")
    ics_203: List[Ics203] = Relationship(back_populates="technical_specialist")
