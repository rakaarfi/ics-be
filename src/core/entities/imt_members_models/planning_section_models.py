from typing import List, Optional

from sqlmodel import Relationship

from src.core.entities.base_imt_models import BaseImtMember
from src.core.entities.ics_201_models import Ics201Chart
from src.core.entities.ics_202_models import Ics202Preparation
from src.core.entities.ics_203_models import Ics203, Ics203Preparation
from src.core.entities.roster_models import ImtRoster


class PlanningSectionChief(BaseImtMember, table=True):
    __tablename__ = "planning_section_chief"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="planning_section_chief",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="planning_section_chief",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_202_preparation: Optional[Ics202Preparation] = Relationship(
        back_populates="planning_section_chief",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="planning_section_chief",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class SituationUnitLeader(BaseImtMember, table=True):
    __tablename__ = "situation_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="situation_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="situation_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="situation_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class ResourcesUnitLeader(BaseImtMember, table=True):
    __tablename__ = "resources_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="resources_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="resources_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="resources_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203_preparation: Optional[Ics203Preparation] = Relationship(
        back_populates="resources_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class DocumentationUnitLeader(BaseImtMember, table=True):
    __tablename__ = "documentation_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="documentation_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="documentation_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="documentation_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class DemobilizationUnitLeader(BaseImtMember, table=True):
    __tablename__ = "demobilization_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="demobilization_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="demobilization_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="demobilization_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class EnvironmentalUnitLeader(BaseImtMember, table=True):
    __tablename__ = "environmental_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="environmental_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="environmental_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="environmental_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class TechnicalSpecialist(BaseImtMember, table=True):
    __tablename__ = "technical_specialist"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="technical_specialist",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="technical_specialist",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="technical_specialist",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
