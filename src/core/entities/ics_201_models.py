from datetime import date, time
from typing import List, Optional

from sqlalchemy import Time
from sqlmodel import Field, Relationship, SQLModel


class Ics201(SQLModel, table=True):
    __tablename__ = "ics_201"

    id: int = Field(default=None, primary_key=True)
    incident_id: Optional[int] = Field(default=None, foreign_key="incident_data.id", ondelete="CASCADE")
    date_initiated: date
    time_initiated: time = Field(sa_column=Field(sa_type=Time))
    map_sketch: Optional[str] = Field(default=None)
    situation_summary: str
    objectives: str

    ics_201_actions_strategies_tactics: List["Ics201ActionsStrategiesTactics"] = Relationship(
        back_populates="ics_201",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_resource_summary: List["Ics201ResourceSummary"] = Relationship(
        back_populates="ics_201",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_approval: List["Ics201Approval"] = Relationship(
        back_populates="ics_201",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    ics_201_chart: "Ics201Chart" = Relationship(
        back_populates="ics_201",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

    incident_data: Optional["IncidentData"] = Relationship(back_populates="ics_201")


class Ics201ActionsStrategiesTactics(SQLModel, table=True):
    __tablename__ = "ics_201_actions_strategies_tactics"

    id: int = Field(default=None, primary_key=True)
    time_initiated: time = Field(sa_column=Field(sa_type=Time))
    actions: str
    ics_201_id: Optional[int] = Field(default=None, foreign_key="ics_201.id", ondelete="CASCADE")

    ics_201: Optional["Ics201"] = Relationship(
        back_populates="ics_201_actions_strategies_tactics"
    )


class Ics201ResourceSummary(SQLModel, table=True):
    __tablename__ = "ics_201_resource_summary"

    id: int = Field(default=None, primary_key=True)
    resource: str
    resource_identified: str
    date_ordered: date
    time_ordered: time
    eta: str
    is_arrived: bool
    notes: str
    ics_201_id: Optional[int] = Field(default=None, foreign_key="ics_201.id", ondelete="CASCADE")

    ics_201: Optional["Ics201"] = Relationship(back_populates="ics_201_resource_summary")


class Ics201Approval(SQLModel, table=True):
    __tablename__ = "ics_201_approval"

    id: int = Field(default=None, primary_key=True)
    ics_201_id: Optional[int] = Field(default=None, foreign_key="ics_201.id", ondelete="CASCADE")
    date_approved: date
    time_approved: time = Field(sa_column=Field(sa_type=Time))
    is_approved: bool


class Ics201Chart(SQLModel, table=True):
    __tablename__ = "ics_201_chart"

    id: int = Field(default=None, primary_key=True)
    ics_201_id: Optional[int] = Field(default=None, foreign_key="ics_201.id", ondelete="CASCADE")

    # Relationships to Ics201
    ics_201: Optional["Ics201"] = Relationship(back_populates="ics_201_chart")

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
        back_populates="ics_201_chart"
    )
    deputy_incident_commander: Optional["DeputyIncidentCommander"] = Relationship(
        back_populates="ics_201_chart"
    )
    safety_officer: Optional["SafetyOfficer"] = Relationship(back_populates="ics_201_chart")
    public_information_officer: Optional["PublicInformationOfficer"] = Relationship(
        back_populates="ics_201_chart"
    )
    liaison_officer: Optional["LiaisonOfficer"] = Relationship(
        back_populates="ics_201_chart"
    )
    legal_officer: Optional["LegalOfficer"] = Relationship(back_populates="ics_201_chart")
    human_capital_officer: Optional["HumanCapitalOfficer"] = Relationship(
        back_populates="ics_201_chart"
    )
    operation_section_chief: Optional["OperationSectionChief"] = Relationship(
        back_populates="ics_201_chart"
    )

    # Relationships to tables in planning_section.py
    planning_section_chief: Optional["PlanningSectionChief"] = Relationship(
        back_populates="ics_201_chart"
    )
    situation_unit_leader: Optional["SituationUnitLeader"] = Relationship(
        back_populates="ics_201_chart"
    )
    resources_unit_leader: Optional["ResourcesUnitLeader"] = Relationship(
        back_populates="ics_201_chart"
    )
    documentation_unit_leader: Optional["DocumentationUnitLeader"] = Relationship(
        back_populates="ics_201_chart"
    )
    demobilization_unit_leader: Optional["DemobilizationUnitLeader"] = Relationship(
        back_populates="ics_201_chart"
    )
    environmental_unit_leader: Optional["EnvironmentalUnitLeader"] = Relationship(
        back_populates="ics_201_chart"
    )
    technical_specialist: Optional["TechnicalSpecialist"] = Relationship(
        back_populates="ics_201_chart"
    )

    # Relationships to tables in logistic_section.py
    logistic_section_chief: Optional["LogisticSectionChief"] = Relationship(
        back_populates="ics_201_chart"
    )
    communication_unit_leader: Optional["CommunicationUnitLeader"] = Relationship(
        back_populates="ics_201_chart"
    )
    medical_unit_leader: Optional["MedicalUnitLeader"] = Relationship(
        back_populates="ics_201_chart"
    )
    food_unit_leader: Optional["FoodUnitLeader"] = Relationship(
        back_populates="ics_201_chart"
    )
    facility_unit_leader: Optional["FacilityUnitLeader"] = Relationship(
        back_populates="ics_201_chart"
    )
    supply_unit_leader: Optional["SupplyUnitLeader"] = Relationship(
        back_populates="ics_201_chart"
    )
    transportation_unit_leader: Optional["TransportationUnitLeader"] = Relationship(
        back_populates="ics_201_chart"
    )

    # Relationships to tables in finance_section.py
    finance_section_chief: Optional["FinanceSectionChief"] = Relationship(
        back_populates="ics_201_chart"
    )
    procurement_unit_leader: Optional["ProcurementUnitLeader"] = Relationship(
        back_populates="ics_201_chart"
    )
    compensation_claim_unit_leader: Optional["CompensationClaimUnitLeader"] = (
        Relationship(back_populates="ics_201_chart")
    )
    cost_unit_leader: Optional["CostUnitLeader"] = Relationship(
        back_populates="ics_201_chart"
    )
    time_unit_leader: Optional["TimeUnitLeader"] = Relationship(
        back_populates="ics_201_chart"
    )


class IcsChartBase(SQLModel):
    incident_commander_name: str
    deputy_incident_commander_name: str
    safety_officer_name: str
    public_information_officer_name: str
    liaison_officer_name: str
    legal_officer_name: str
    human_capital_officer_name: str
    operation_section_chief_name: str
    planning_section_chief_name: str
    situation_unit_leader_name: str
    resources_unit_leader_name: str
    documentation_unit_leader_name: str
    demobilization_unit_leader_name: str
    environmental_unit_leader_name: str
    technical_specialist_name: str
    logistic_section_chief_name: str
    communication_unit_leader_name: str
    medical_unit_leader_name: str
    food_unit_leader_name: str
    facility_unit_leader_name: str
    supply_unit_leader_name: str
    transportation_unit_leader_name: str
    finance_section_chief_name: str
    procurement_unit_leader_name: str
    compensation_claim_unit_leader_name: str
    cost_unit_leader_name: str
    time_unit_leader_name: str
