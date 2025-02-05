from typing import List, Optional

from sqlmodel import Relationship

from src.core.entities.base_imt_models import BaseImtMember
from src.core.entities.ics_201_models import Ics201Chart
from src.core.entities.ics_202_models import Ics202Approval
from src.core.entities.ics_203_models import Ics203
from src.core.entities.ics_204_models import Ics204, Ics204PreparationOSChief
from src.core.entities.ics_206_models import Ics206Approval
from src.core.entities.ics_208_models import Ics208Preparation
from src.core.entities.ics_209_models import Ics209, Ics209Approval
from src.core.entities.roster_models import ImtRoster


class IncidentCommander(BaseImtMember, table=True):
    __tablename__ = "incident_commander"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="incident_commander",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="incident_commander",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_202_approval: Optional[Ics202Approval] = Relationship(
        back_populates="incident_commander",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="incident_commander",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_209: Optional[Ics209] = Relationship(
        back_populates="incident_commander",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_209_approval: Optional[Ics209Approval] = Relationship(
        back_populates="incident_commander",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class DeputyIncidentCommander(BaseImtMember, table=True):
    __tablename__ = "deputy_incident_commander"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="deputy_incident_commander",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="deputy_incident_commander",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="deputy_incident_commander",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class SafetyOfficer(BaseImtMember, table=True):
    __tablename__ = "safety_officer"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="safety_officer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="safety_officer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="safety_officer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_206_approval: Optional[Ics206Approval] = Relationship(
        back_populates="safety_officer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_208_preparation: Optional[Ics208Preparation] = Relationship(
        back_populates="safety_officer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class PublicInformationOfficer(BaseImtMember, table=True):
    __tablename__ = "public_information_officer"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="public_information_officer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="public_information_officer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="public_information_officer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class LiaisonOfficer(BaseImtMember, table=True):
    __tablename__ = "liaison_officer"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="liaison_officer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="liaison_officer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="liaison_officer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class LegalOfficer(BaseImtMember, table=True):
    __tablename__ = "legal_officer"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="legal_officer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="legal_officer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="legal_officer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class HumanCapitalOfficer(BaseImtMember, table=True):
    __tablename__ = "human_capital_officer"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="human_capital_officer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="human_capital_officer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="human_capital_officer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class OperationSectionChief(BaseImtMember, table=True):
    __tablename__ = "operation_section_chief"
    imt_rosters: List[ImtRoster] = Relationship(
        back_populates="operation_section_chief",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: List[Ics201Chart] = Relationship(
        back_populates="operation_section_chief",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_203: List[Ics203] = Relationship(
        back_populates="operation_section_chief",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_204: Optional[Ics204] = Relationship(
        back_populates="operation_section_chief",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_204_preparation_os_chief: Optional[Ics204PreparationOSChief] = Relationship(
        back_populates="operation_section_chief",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
