from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.config.database import get_session
from app.models.imt_members_models.finance_section_models import *
from app.models.imt_members_models.logistic_section_models import *
from app.models.imt_members_models.main_section_models import *
from app.models.imt_members_models.planning_section_models import *
from app.models.roster_models import ImtRoster, ImtRosterTable

router = APIRouter()


@router.get("/{id}", response_model=ImtRosterTable)
async def read_roster_tables(id: int, session: AsyncSession = Depends(get_session)):
    # Query construction remains the same
    statement = (
        select(
            ImtRoster.id.label("imtroster_id"),
            ImtRoster.date_from.label("date_from"),
            ImtRoster.date_to.label("date_to"),
            ImtRoster.remark.label("remark"),
            IncidentCommander.name.label("incident_commander_name"),
            IncidentCommander.office_phone.label("incident_commander_office_phone"),
            IncidentCommander.mobile_phone.label("incident_commander_mobile_phone"),
            DeputyIncidentCommander.name.label("deputy_incident_commander_name"),
            DeputyIncidentCommander.office_phone.label(
                "deputy_incident_commander_office_phone"
            ),
            DeputyIncidentCommander.mobile_phone.label(
                "deputy_incident_commander_mobile_phone"
            ),
            SafetyOfficer.name.label("safety_officer_name"),
            SafetyOfficer.office_phone.label("safety_officer_office_phone"),
            SafetyOfficer.mobile_phone.label("safety_officer_mobile_phone"),
            PublicInformationOfficer.name.label("public_information_officer_name"),
            PublicInformationOfficer.office_phone.label(
                "public_information_officer_office_phone"
            ),
            PublicInformationOfficer.mobile_phone.label(
                "public_information_officer_mobile_phone"
            ),
            LiaisonOfficer.name.label("liaison_officer_name"),
            LiaisonOfficer.office_phone.label("liaison_officer_office_phone"),
            LiaisonOfficer.mobile_phone.label("liaison_officer_mobile_phone"),
            LegalOfficer.name.label("legal_officer_name"),
            LegalOfficer.office_phone.label("legal_officer_office_phone"),
            LegalOfficer.mobile_phone.label("legal_officer_mobile_phone"),
            HumanCapitalOfficer.name.label("human_capital_officer_name"),
            HumanCapitalOfficer.office_phone.label(
                "human_capital_officer_office_phone"
            ),
            HumanCapitalOfficer.mobile_phone.label(
                "human_capital_officer_mobile_phone"
            ),
            OperationSectionChief.name.label("operation_section_chief_name"),
            OperationSectionChief.office_phone.label(
                "operation_section_chief_office_phone"
            ),
            OperationSectionChief.mobile_phone.label(
                "operation_section_chief_mobile_phone"
            ),
            PlanningSectionChief.name.label("planning_section_chief_name"),
            PlanningSectionChief.office_phone.label(
                "planning_section_chief_office_phone"
            ),
            PlanningSectionChief.mobile_phone.label(
                "planning_section_chief_mobile_phone"
            ),
            SituationUnitLeader.name.label("situation_unit_leader_name"),
            SituationUnitLeader.office_phone.label(
                "situation_unit_leader_office_phone"
            ),
            SituationUnitLeader.mobile_phone.label(
                "situation_unit_leader_mobile_phone"
            ),
            ResourcesUnitLeader.name.label("resources_unit_leader_name"),
            ResourcesUnitLeader.office_phone.label(
                "resources_unit_leader_office_phone"
            ),
            ResourcesUnitLeader.mobile_phone.label(
                "resources_unit_leader_mobile_phone"
            ),
            DocumentationUnitLeader.name.label("documentation_unit_leader_name"),
            DocumentationUnitLeader.office_phone.label(
                "documentation_unit_leader_office_phone"
            ),
            DocumentationUnitLeader.mobile_phone.label(
                "documentation_unit_leader_mobile_phone"
            ),
            DemobilizationUnitLeader.name.label("demobilization_unit_leader_name"),
            DemobilizationUnitLeader.office_phone.label(
                "demobilization_unit_leader_office_phone"
            ),
            DemobilizationUnitLeader.mobile_phone.label(
                "demobilization_unit_leader_mobile_phone"
            ),
            EnvironmentalUnitLeader.name.label("environmental_unit_leader_name"),
            EnvironmentalUnitLeader.office_phone.label(
                "environmental_unit_leader_office_phone"
            ),
            EnvironmentalUnitLeader.mobile_phone.label(
                "environmental_unit_leader_mobile_phone"
            ),
            TechnicalSpecialist.name.label("technical_specialist_name"),
            TechnicalSpecialist.office_phone.label("technical_specialist_office_phone"),
            TechnicalSpecialist.mobile_phone.label("technical_specialist_mobile_phone"),
            LogisticSectionChief.name.label("logistic_section_chief_name"),
            LogisticSectionChief.office_phone.label(
                "logistic_section_chief_office_phone"
            ),
            LogisticSectionChief.mobile_phone.label(
                "logistic_section_chief_mobile_phone"
            ),
            CommunicationUnitLeader.name.label("communication_unit_leader_name"),
            CommunicationUnitLeader.office_phone.label(
                "communication_unit_leader_office_phone"
            ),
            CommunicationUnitLeader.mobile_phone.label(
                "communication_unit_leader_mobile_phone"
            ),
            MedicalUnitLeader.name.label("medical_unit_leader_name"),
            MedicalUnitLeader.office_phone.label("medical_unit_leader_office_phone"),
            MedicalUnitLeader.mobile_phone.label("medical_unit_leader_mobile_phone"),
            FoodUnitLeader.name.label("food_unit_leader_name"),
            FoodUnitLeader.office_phone.label("food_unit_leader_office_phone"),
            FoodUnitLeader.mobile_phone.label("food_unit_leader_mobile_phone"),
            FacilityUnitLeader.name.label("facility_unit_leader_name"),
            FacilityUnitLeader.office_phone.label("facility_unit_leader_office_phone"),
            FacilityUnitLeader.mobile_phone.label("facility_unit_leader_mobile_phone"),
            SupplyUnitLeader.name.label("supply_unit_leader_name"),
            SupplyUnitLeader.office_phone.label("supply_unit_leader_office_phone"),
            SupplyUnitLeader.mobile_phone.label("supply_unit_leader_mobile_phone"),
            TransportationUnitLeader.name.label("transportation_unit_leader_name"),
            TransportationUnitLeader.office_phone.label(
                "transportation_unit_leader_office_phone"
            ),
            TransportationUnitLeader.mobile_phone.label(
                "transportation_unit_leader_mobile_phone"
            ),
            FinanceSectionChief.name.label("finance_section_chief_name"),
            FinanceSectionChief.office_phone.label(
                "finance_section_chief_office_phone"
            ),
            FinanceSectionChief.mobile_phone.label(
                "finance_section_chief_mobile_phone"
            ),
            ProcurementUnitLeader.name.label("procurement_unit_leader_name"),
            ProcurementUnitLeader.office_phone.label(
                "procurement_unit_leader_office_phone"
            ),
            ProcurementUnitLeader.mobile_phone.label(
                "procurement_unit_leader_mobile_phone"
            ),
            CompensationClaimUnitLeader.name.label(
                "compensation_claim_unit_leader_name"
            ),
            CompensationClaimUnitLeader.office_phone.label(
                "compensation_claim_unit_leader_office_phone"
            ),
            CompensationClaimUnitLeader.mobile_phone.label(
                "compensation_claim_unit_leader_mobile_phone"
            ),
            CostUnitLeader.name.label("cost_unit_leader_name"),
            CostUnitLeader.office_phone.label("cost_unit_leader_office_phone"),
            CostUnitLeader.mobile_phone.label("cost_unit_leader_mobile_phone"),
            TimeUnitLeader.name.label("time_unit_leader_name"),
            TimeUnitLeader.office_phone.label("time_unit_leader_office_phone"),
            TimeUnitLeader.mobile_phone.label("time_unit_leader_mobile_phone"),
        )
        .join(ImtRoster.incident_commander)
        .join(ImtRoster.deputy_incident_commander)
        .join(ImtRoster.safety_officer)
        .join(ImtRoster.public_information_officer)
        .join(ImtRoster.liaison_officer)
        .join(ImtRoster.legal_officer)
        .join(ImtRoster.human_capital_officer)
        .join(ImtRoster.operation_section_chief)
        .join(ImtRoster.planning_section_chief)
        .join(ImtRoster.situation_unit_leader)
        .join(ImtRoster.resources_unit_leader)
        .join(ImtRoster.documentation_unit_leader)
        .join(ImtRoster.demobilization_unit_leader)
        .join(ImtRoster.environmental_unit_leader)
        .join(ImtRoster.technical_specialist)
        .join(ImtRoster.logistic_section_chief)
        .join(ImtRoster.communication_unit_leader)
        .join(ImtRoster.medical_unit_leader)
        .join(ImtRoster.food_unit_leader)
        .join(ImtRoster.facility_unit_leader)
        .join(ImtRoster.supply_unit_leader)
        .join(ImtRoster.transportation_unit_leader)
        .join(ImtRoster.finance_section_chief)
        .join(ImtRoster.procurement_unit_leader)
        .join(ImtRoster.compensation_claim_unit_leader)
        .join(ImtRoster.cost_unit_leader)
        .join(ImtRoster.time_unit_leader)
        .where(ImtRoster.id == id)
    )

    result = await session.execute(statement)
    data = result.first()

    if not data:
        raise HTTPException(status_code=404, detail="Item not found")

    return data
