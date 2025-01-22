from sqlmodel import Relationship
from typing import List

from app.models.base_imt import BaseImtMember
from app.models.roster import ImtRoster
from app.models.ics_201 import IcsChart


class IncidentCommander(BaseImtMember, table=True):
    __tablename__ = "incident_commander"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="incident_commander")
    ics_chart: List[IcsChart] = Relationship(back_populates="incident_commander")

    
class DeputyIncidentCommander(BaseImtMember, table=True):
    __tablename__ = "deputy_incident_commander"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="deputy_incident_commander")
    ics_chart: List[IcsChart] = Relationship(back_populates="deputy_incident_commander")
    
    
class SafetyOfficer(BaseImtMember, table=True):
    __tablename__ = "safety_officer"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="safety_officer")
    ics_chart: List[IcsChart] = Relationship(back_populates="safety_officer")


class PublicInformationOfficer(BaseImtMember, table=True):
    __tablename__ = "public_information_officer"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="public_information_officer")
    ics_chart: List[IcsChart] = Relationship(back_populates="public_information_officer")


class LiaisonOfficer(BaseImtMember, table=True):
    __tablename__ = "liaison_officer"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="liaison_officer")
    ics_chart: List[IcsChart] = Relationship(back_populates="liaison_officer")
    
    
class LegalOfficer(BaseImtMember, table=True):
    __tablename__ = "legal_officer"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="legal_officer")
    ics_chart: List[IcsChart] = Relationship(back_populates="legal_officer")


class HumanCapitalOfficer(BaseImtMember, table=True):
    __tablename__ = "human_capital_officer"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="human_capital_officer")
    ics_chart: List[IcsChart] = Relationship(back_populates="human_capital_officer")
    
    
class OperationSectionChief(BaseImtMember, table=True):
    __tablename__ = "operation_section_chief"
    imt_rosters: List[ImtRoster] = Relationship(back_populates="operation_section_chief")
    ics_chart: List[IcsChart] = Relationship(back_populates="operation_section_chief")
    