from typing import List

from sqlmodel import Relationship

from src.core.entities.base_imt_models import BaseImtMember
from src.core.entities.ics_201_models import Ics201Chart
from src.core.entities.ics_203_models import Ics203
from src.core.entities.roster_models import ImtRoster


class FinanceSectionChief(BaseImtMember, table=True):
    __tablename__ = "finance_section_chief"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="finance_section_chief",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="finance_section_chief",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="finance_section_chief",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},    
    )


class ProcurementUnitLeader(BaseImtMember, table=True):
    __tablename__ = "procurement_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="procurement_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="procurement_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="procurement_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class CompensationClaimUnitLeader(BaseImtMember, table=True):
    __tablename__ = "compensation_claim_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="compensation_claim_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="compensation_claim_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="compensation_claim_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class CostUnitLeader(BaseImtMember, table=True):
    __tablename__ = "cost_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="cost_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="cost_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="cost_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class TimeUnitLeader(BaseImtMember, table=True):
    __tablename__ = "time_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="time_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="time_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="time_unit_leader",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
