from datetime import date, time
from typing import Optional

from sqlalchemy import Time
from sqlmodel import Field, Relationship, SQLModel


class Ics203(SQLModel, table=True):
    __tablename__ = "ics_203"

    id: int = Field(default=None, primary_key=True)
    operational_period_id: Optional[int] = Field(
        default=None, foreign_key="operational_period.id"
    )

    ics_203_preparation: Optional["Ics203Preparation"] = Relationship(
        back_populates="ics_203",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    operational_period: Optional["OperationalPeriod"] = Relationship(
        back_populates="ics_203"
    )

    # Foreign keys for main_section.py
    incident_commander_id: Optional[int] = Field(
        default=None, foreign_key="incident_commander.id", ondelete="CASCADE"
    )
    deputy_incident_commander_id: Optional[int] = Field(
        default=None, foreign_key="deputy_incident_commander.id", ondelete="CASCADE"
    )
    safety_officer_id: Optional[int] = Field(
        default=None, foreign_key="safety_officer.id", ondelete="CASCADE"
    )
    public_information_officer_id: Optional[int] = Field(
        default=None, foreign_key="public_information_officer.id", ondelete="CASCADE"
    )
    liaison_officer_id: Optional[int] = Field(
        default=None, foreign_key="liaison_officer.id", ondelete="CASCADE"
    )
    legal_officer_id: Optional[int] = Field(
        default=None, foreign_key="legal_officer.id", ondelete="CASCADE"
    )
    human_capital_officer_id: Optional[int] = Field(
        default=None, foreign_key="human_capital_officer.id", ondelete="CASCADE"
    )
    operation_section_chief_id: Optional[int] = Field(
        default=None, foreign_key="operation_section_chief.id", ondelete="CASCADE"
    )

    # Foreign keys for planning_section.py
    planning_section_chief_id: Optional[int] = Field(
        default=None, foreign_key="planning_section_chief.id", ondelete="CASCADE"
    )
    situation_unit_leader_id: Optional[int] = Field(
        default=None, foreign_key="situation_unit_leader.id", ondelete="CASCADE"
    )
    resources_unit_leader_id: Optional[int] = Field(
        default=None, foreign_key="resources_unit_leader.id", ondelete="CASCADE"
    )
    documentation_unit_leader_id: Optional[int] = Field(
        default=None, foreign_key="documentation_unit_leader.id", ondelete="CASCADE"
    )
    demobilization_unit_leader_id: Optional[int] = Field(
        default=None, foreign_key="demobilization_unit_leader.id", ondelete="CASCADE"
    )
    environmental_unit_leader_id: Optional[int] = Field(
        default=None, foreign_key="environmental_unit_leader.id", ondelete="CASCADE"
    )
    technical_specialist_id: Optional[int] = Field(
        default=None, foreign_key="technical_specialist.id", ondelete="CASCADE"
    )

    # Foreign keys for logistic_section.py
    logistic_section_chief_id: Optional[int] = Field(
        default=None, foreign_key="logistic_section_chief.id", ondelete="CASCADE"
    )
    communication_unit_leader_id: Optional[int] = Field(
        default=None, foreign_key="communication_unit_leader.id", ondelete="CASCADE"
    )
    medical_unit_leader_id: Optional[int] = Field(
        default=None, foreign_key="medical_unit_leader.id", ondelete="CASCADE"
    )
    food_unit_leader_id: Optional[int] = Field(
        default=None, foreign_key="food_unit_leader.id", ondelete="CASCADE"
    )
    facility_unit_leader_id: Optional[int] = Field(
        default=None, foreign_key="facility_unit_leader.id", ondelete="CASCADE"
    )
    supply_unit_leader_id: Optional[int] = Field(
        default=None, foreign_key="supply_unit_leader.id", ondelete="CASCADE"
    )
    transportation_unit_leader_id: Optional[int] = Field(
        default=None, foreign_key="transportation_unit_leader.id", ondelete="CASCADE"
    )

    # Foreign keys for finance_section.py
    finance_section_chief_id: Optional[int] = Field(
        default=None, foreign_key="finance_section_chief.id", ondelete="CASCADE"
    )
    procurement_unit_leader_id: Optional[int] = Field(
        default=None, foreign_key="procurement_unit_leader.id", ondelete="CASCADE"
    )
    compensation_claim_unit_leader_id: Optional[int] = Field(
        default=None, foreign_key="compensation_claim_unit_leader.id", ondelete="CASCADE"
    )
    cost_unit_leader_id: Optional[int] = Field(
        default=None, foreign_key="cost_unit_leader.id", ondelete="CASCADE"
    )
    time_unit_leader_id: Optional[int] = Field(
        default=None, foreign_key="time_unit_leader.id", ondelete="CASCADE"
    )

    # Relationships to tables in main_section.py
    incident_commander: Optional["IncidentCommander"] = Relationship(
        back_populates="ics_203"
    )
    deputy_incident_commander: Optional["DeputyIncidentCommander"] = Relationship(
        back_populates="ics_203"
    )
    safety_officer: Optional["SafetyOfficer"] = Relationship(back_populates="ics_203")
    public_information_officer: Optional["PublicInformationOfficer"] = Relationship(
        back_populates="ics_203"
    )
    liaison_officer: Optional["LiaisonOfficer"] = Relationship(back_populates="ics_203")
    legal_officer: Optional["LegalOfficer"] = Relationship(back_populates="ics_203")
    human_capital_officer: Optional["HumanCapitalOfficer"] = Relationship(
        back_populates="ics_203"
    )
    operation_section_chief: Optional["OperationSectionChief"] = Relationship(
        back_populates="ics_203"
    )

    # Relationships to tables in planning_section.py
    planning_section_chief: Optional["PlanningSectionChief"] = Relationship(
        back_populates="ics_203"
    )
    situation_unit_leader: Optional["SituationUnitLeader"] = Relationship(
        back_populates="ics_203"
    )
    resources_unit_leader: Optional["ResourcesUnitLeader"] = Relationship(
        back_populates="ics_203"
    )
    documentation_unit_leader: Optional["DocumentationUnitLeader"] = Relationship(
        back_populates="ics_203"
    )
    demobilization_unit_leader: Optional["DemobilizationUnitLeader"] = Relationship(
        back_populates="ics_203"
    )
    environmental_unit_leader: Optional["EnvironmentalUnitLeader"] = Relationship(
        back_populates="ics_203"
    )
    technical_specialist: Optional["TechnicalSpecialist"] = Relationship(
        back_populates="ics_203"
    )

    # Relationships to tables in logistic_section.py
    logistic_section_chief: Optional["LogisticSectionChief"] = Relationship(
        back_populates="ics_203"
    )
    communication_unit_leader: Optional["CommunicationUnitLeader"] = Relationship(
        back_populates="ics_203"
    )
    medical_unit_leader: Optional["MedicalUnitLeader"] = Relationship(
        back_populates="ics_203"
    )
    food_unit_leader: Optional["FoodUnitLeader"] = Relationship(
        back_populates="ics_203"
    )
    facility_unit_leader: Optional["FacilityUnitLeader"] = Relationship(
        back_populates="ics_203"
    )
    supply_unit_leader: Optional["SupplyUnitLeader"] = Relationship(
        back_populates="ics_203"
    )
    transportation_unit_leader: Optional["TransportationUnitLeader"] = Relationship(
        back_populates="ics_203"
    )

    # Relationships to tables in finance_section.py
    finance_section_chief: Optional["FinanceSectionChief"] = Relationship(
        back_populates="ics_203"
    )
    procurement_unit_leader: Optional["ProcurementUnitLeader"] = Relationship(
        back_populates="ics_203"
    )
    compensation_claim_unit_leader: Optional["CompensationClaimUnitLeader"] = (
        Relationship(back_populates="ics_203")
    )
    cost_unit_leader: Optional["CostUnitLeader"] = Relationship(
        back_populates="ics_203"
    )
    time_unit_leader: Optional["TimeUnitLeader"] = Relationship(
        back_populates="ics_203"
    )


class Ics203Preparation(SQLModel, table=True):
    __tablename__ = "ics_203_preparation"

    id: int = Field(default=None, primary_key=True)
    ics_203_id: Optional[int] = Field(default=None, foreign_key="ics_203.id", ondelete="CASCADE")
    resources_unit_leader_id: Optional[int] = Field(
        default=None, foreign_key="resources_unit_leader.id", ondelete="CASCADE"
    )
    is_prepared: bool
    date_prepared: Optional[date]
    time_prepared: Optional[time] = Field(sa_column=Field(sa_type=Time))

    ics_203: Optional["Ics203"] = Relationship(back_populates="ics_203_preparation")
    resources_unit_leader: Optional["ResourcesUnitLeader"] = Relationship(
        back_populates="ics_203_preparation"
    )
