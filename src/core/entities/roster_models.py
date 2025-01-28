from datetime import date
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class ImtRoster(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    date_from: date
    date_to: date
    remark: str

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

    # Relasi ke setiap tabel di main_section.py
    incident_commander: Optional["IncidentCommander"] = Relationship(
        back_populates="imt_rosters"
    )
    deputy_incident_commander: Optional["DeputyIncidentCommander"] = Relationship(
        back_populates="imt_rosters"
    )
    safety_officer: Optional["SafetyOfficer"] = Relationship(
        back_populates="imt_rosters"
    )
    public_information_officer: Optional["PublicInformationOfficer"] = Relationship(
        back_populates="imt_rosters"
    )
    liaison_officer: Optional["LiaisonOfficer"] = Relationship(
        back_populates="imt_rosters"
    )
    legal_officer: Optional["LegalOfficer"] = Relationship(back_populates="imt_rosters")
    human_capital_officer: Optional["HumanCapitalOfficer"] = Relationship(
        back_populates="imt_rosters"
    )
    operation_section_chief: Optional["OperationSectionChief"] = Relationship(
        back_populates="imt_rosters"
    )

    # Relasi ke setiap tabel di planning_section.py
    planning_section_chief: Optional["PlanningSectionChief"] = Relationship(
        back_populates="imt_rosters"
    )
    situation_unit_leader: Optional["SituationUnitLeader"] = Relationship(
        back_populates="imt_rosters"
    )
    resources_unit_leader: Optional["ResourcesUnitLeader"] = Relationship(
        back_populates="imt_rosters"
    )
    documentation_unit_leader: Optional["DocumentationUnitLeader"] = Relationship(
        back_populates="imt_rosters"
    )
    demobilization_unit_leader: Optional["DemobilizationUnitLeader"] = Relationship(
        back_populates="imt_rosters"
    )
    environmental_unit_leader: Optional["EnvironmentalUnitLeader"] = Relationship(
        back_populates="imt_rosters"
    )
    technical_specialist: Optional["TechnicalSpecialist"] = Relationship(
        back_populates="imt_rosters"
    )

    # Relasi ke setiap tabel di logistic_section.py
    logistic_section_chief: Optional["LogisticSectionChief"] = Relationship(
        back_populates="imt_rosters"
    )
    communication_unit_leader: Optional["CommunicationUnitLeader"] = Relationship(
        back_populates="imt_rosters"
    )
    medical_unit_leader: Optional["MedicalUnitLeader"] = Relationship(
        back_populates="imt_rosters"
    )
    food_unit_leader: Optional["FoodUnitLeader"] = Relationship(
        back_populates="imt_rosters"
    )
    facility_unit_leader: Optional["FacilityUnitLeader"] = Relationship(
        back_populates="imt_rosters"
    )
    supply_unit_leader: Optional["SupplyUnitLeader"] = Relationship(
        back_populates="imt_rosters"
    )
    transportation_unit_leader: Optional["TransportationUnitLeader"] = Relationship(
        back_populates="imt_rosters"
    )

    # Relasi ke setiap tabel di finance_section.py
    finance_section_chief: Optional["FinanceSectionChief"] = Relationship(
        back_populates="imt_rosters"
    )
    procurement_unit_leader: Optional["ProcurementUnitLeader"] = Relationship(
        back_populates="imt_rosters"
    )
    compensation_claim_unit_leader: Optional["CompensationClaimUnitLeader"] = (
        Relationship(back_populates="imt_rosters")
    )
    cost_unit_leader: Optional["CostUnitLeader"] = Relationship(
        back_populates="imt_rosters"
    )
    time_unit_leader: Optional["TimeUnitLeader"] = Relationship(
        back_populates="imt_rosters"
    )


# Model untuk Roster Table
class ImtRosterTable(SQLModel):
    imtroster_id: int
    date_from: date
    date_to: date
    remark: str

    incident_commander_name: str
    incident_commander_office_phone: str
    incident_commander_mobile_phone: str

    deputy_incident_commander_name: str
    deputy_incident_commander_office_phone: str
    deputy_incident_commander_mobile_phone: str

    safety_officer_name: str
    safety_officer_office_phone: str
    safety_officer_mobile_phone: str

    public_information_officer_name: str
    public_information_officer_office_phone: str
    public_information_officer_mobile_phone: str

    liaison_officer_name: str
    liaison_officer_office_phone: str
    liaison_officer_mobile_phone: str

    legal_officer_name: str
    legal_officer_office_phone: str
    legal_officer_mobile_phone: str

    human_capital_officer_name: str
    human_capital_officer_office_phone: str
    human_capital_officer_mobile_phone: str

    operation_section_chief_name: str
    operation_section_chief_office_phone: str
    operation_section_chief_mobile_phone: str

    planning_section_chief_name: str
    planning_section_chief_office_phone: str
    planning_section_chief_mobile_phone: str

    situation_unit_leader_name: str
    situation_unit_leader_office_phone: str
    situation_unit_leader_mobile_phone: str

    resources_unit_leader_name: str
    resources_unit_leader_office_phone: str
    resources_unit_leader_mobile_phone: str

    documentation_unit_leader_name: str
    documentation_unit_leader_office_phone: str
    documentation_unit_leader_mobile_phone: str

    demobilization_unit_leader_name: str
    demobilization_unit_leader_office_phone: str
    demobilization_unit_leader_mobile_phone: str

    environmental_unit_leader_name: str
    environmental_unit_leader_office_phone: str
    environmental_unit_leader_mobile_phone: str

    technical_specialist_name: str
    technical_specialist_office_phone: str
    technical_specialist_mobile_phone: str

    logistic_section_chief_name: str
    logistic_section_chief_office_phone: str
    logistic_section_chief_mobile_phone: str

    communication_unit_leader_name: str
    communication_unit_leader_office_phone: str
    communication_unit_leader_mobile_phone: str

    medical_unit_leader_name: str
    medical_unit_leader_office_phone: str
    medical_unit_leader_mobile_phone: str

    food_unit_leader_name: str
    food_unit_leader_office_phone: str
    food_unit_leader_mobile_phone: str

    facility_unit_leader_name: str
    facility_unit_leader_office_phone: str
    facility_unit_leader_mobile_phone: str

    supply_unit_leader_name: str
    supply_unit_leader_office_phone: str
    supply_unit_leader_mobile_phone: str

    transportation_unit_leader_name: str
    transportation_unit_leader_office_phone: str
    transportation_unit_leader_mobile_phone: str

    finance_section_chief_name: str
    finance_section_chief_office_phone: str
    finance_section_chief_mobile_phone: str

    procurement_unit_leader_name: str
    procurement_unit_leader_office_phone: str
    procurement_unit_leader_mobile_phone: str

    compensation_claim_unit_leader_name: str
    compensation_claim_unit_leader_office_phone: str
    compensation_claim_unit_leader_mobile_phone: str

    cost_unit_leader_name: str
    cost_unit_leader_office_phone: str
    cost_unit_leader_mobile_phone: str

    time_unit_leader_name: str
    time_unit_leader_office_phone: str
    time_unit_leader_mobile_phone: str
