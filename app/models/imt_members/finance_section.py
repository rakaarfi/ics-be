from sqlmodel import Relationship
from typing import List

from app.models.base_imt import BaseImtMember
from app.models.roster import ImtRoster
from app.models.ics_201 import IcsChart


class FinanceSectionChief(BaseImtMember, table=True):
    __tablename__ = "finance_section_chief"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="finance_section_chief")
    ics_chart: List[IcsChart] = Relationship(back_populates="finance_section_chief")
    
    
class ProcurementUnitLeader(BaseImtMember, table=True):
    __tablename__ = "procurement_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="procurement_unit_leader")
    ics_chart: List[IcsChart] = Relationship(back_populates="procurement_unit_leader")
    
    
class CompensationClaimUnitLeader(BaseImtMember, table=True):
    __tablename__ = "compensation_claim_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="compensation_claim_unit_leader")
    ics_chart: List[IcsChart] = Relationship(back_populates="compensation_claim_unit_leader")
    
    
class CostUnitLeader(BaseImtMember, table=True):
    __tablename__ = "cost_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="cost_unit_leader")
    ics_chart: List[IcsChart] = Relationship(back_populates="cost_unit_leader")
    
    
class TimeUnitLeader(BaseImtMember, table=True):
    __tablename__ = "time_unit_leader"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="time_unit_leader")
    ics_chart: List[IcsChart] = Relationship(back_populates="time_unit_leader")
    