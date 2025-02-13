import os
from datetime import datetime
from typing import Optional, Type, Any
from io import BytesIO  # Import BytesIO untuk membuat file di memori


from docx.shared import Inches
from docxtpl import (DocxTemplate,  # Menggunakan docxtpl untuk templating
                     InlineImage)
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, SQLModel

from src.core.entities.ics_203_models import Ics203, Ics203Preparation
from src.core.entities.imt_members_models.planning_section_models import *
from src.core.entities.imt_members_models.main_section_models import *
from src.core.entities.imt_members_models.logistic_section_models import *
from src.core.entities.imt_members_models.finance_section_models import *
from src.core.entities.incident_data_models import IncidentData, OperationalPeriod
from src.infrastructure.config.database import get_session
from src.core.exceptions import NotFoundException, BadRequestException


router = APIRouter()

def format_date_to_sentence(date_str):
    # Parse tanggal dari string ke objek datetime
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    # Ambil hari, bulan, dan tahun
    day = date_obj.day
    month = date_obj.strftime("%b")  # Nama bulan (e.g., Jan, Feb)
    year = date_obj.year

    # Tambahkan suffix untuk hari
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]

    # Gabungkan menjadi kalimat
    return f"{day}{suffix} {month} {year}"


async def read_item_by_id(model: Type[SQLModel], item_id: int, session: AsyncSession):
        item = await session.get(model, item_id)
        if not item:
            raise NotFoundException(f"{model.__name__} not found")
        return item
    
async def read_items_by_condition(model: Type[SQLModel], condition: Any, session: AsyncSession):
    query = select(model).where(condition)
    result = await session.execute(query)
    return result.scalars().all()

# Mapping field dengan model yang sesuai
model_mappings = {
    "incident_commander": IncidentCommander,
    "deputy_incident_commander": DeputyIncidentCommander,
    "safety_officer": SafetyOfficer,
    "public_information_officer": PublicInformationOfficer,
    "liaison_officer": LiaisonOfficer,
    "legal_officer": LegalOfficer,
    "human_capital_officer": HumanCapitalOfficer,
    "operation_section_chief": OperationSectionChief,
    "planning_section_chief": PlanningSectionChief,
    "situation_unit_leader": SituationUnitLeader,
    "resources_unit_leader": ResourcesUnitLeader,
    "documentation_unit_leader": DocumentationUnitLeader,
    "demobilization_unit_leader": DemobilizationUnitLeader,
    "environmental_unit_leader": EnvironmentalUnitLeader,
    "technical_specialist": TechnicalSpecialist,
    "logistic_section_chief": LogisticSectionChief,
    "communication_unit_leader": CommunicationUnitLeader,
    "medical_unit_leader": MedicalUnitLeader,
    "food_unit_leader": FoodUnitLeader,
    "facility_unit_leader": FacilityUnitLeader,
    "supply_unit_leader": SupplyUnitLeader,
    "transportation_unit_leader": TransportationUnitLeader,
    "finance_section_chief": FinanceSectionChief,
    "procurement_unit_leader": ProcurementUnitLeader,
    "compensation_claim_unit_leader": CompensationClaimUnitLeader,
    "cost_unit_leader": CostUnitLeader,
    "time_unit_leader": TimeUnitLeader,
}

@router.post("/{id}")
async def export_docx(id: int, session: AsyncSession = Depends(get_session)):
    template_path = "src/infrastructure/templates/ics_207.docx"

    # Ambil data Ics203
    ics_203 = await read_item_by_id(Ics203, item_id=id, session=session)
    context = ics_203.model_dump()
    ics_203_id = ics_203.id
    
    # Ambil data dari model yang sesuai berdasarkan mapping
    for field, model in model_mappings.items():
        model_id = getattr(ics_203, f"{field}_id")
        item = await read_item_by_id(model, item_id=model_id, session=session)
        context[f"{field}_name"] = item.name
    
    operational_period_id = context["operational_period_id"]
    # Ambil operational_period yang terkait
    operational_period = await read_item_by_id(OperationalPeriod, item_id=operational_period_id, session=session)
    context["operational_period"] = operational_period
    context["date_from"] = format_date_to_sentence(operational_period.date_from.strftime("%Y-%m-%d"))
    context["time_from"] = operational_period.time_from.strftime("%H:%M")
    context["date_to"] = format_date_to_sentence(operational_period.date_to.strftime("%Y-%m-%d"))
    context["time_to"] = operational_period.time_to.strftime("%H:%M")

    incident_id = operational_period.incident_id
    # Ambil incident_data yang terkait
    incident_data = await read_item_by_id(IncidentData, item_id=incident_id, session=session)
    context["incident_data"] = incident_data
    context["incident_name"] = incident_data.name

    # Ambil Resources Unit Leader terkait
    ics_203_preparations = await read_items_by_condition(Ics203Preparation, Ics203Preparation.ics_203_id == ics_203_id, session=session)
    resources_unit_leader_id = ics_203_preparations[0].resources_unit_leader_id
    prepared_name = await read_item_by_id(ResourcesUnitLeader, item_id=resources_unit_leader_id, session=session)
    context["prepared_name"] = prepared_name.name
    context["is_prepared"] = "✓" if ics_203_preparations[0].is_prepared else "✗"
    context['date_prepared'] = format_date_to_sentence(ics_203_preparations[0].date_prepared.strftime("%Y-%m-%d"))
    context['time_prepared'] = ics_203_preparations[0].time_prepared.strftime("%H:%M")
        
    # Muat template
    doc = DocxTemplate(template_path)

    # Render docxtpl
    doc.render(context)

    # Simpan hasil
    output_stream = BytesIO()
    doc.save(output_stream)
    output_stream.seek(0)  # Kembalikan pointer ke awal stream
    
    return StreamingResponse(
        output_stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename=ics_206_{id}.docx"}
    )
