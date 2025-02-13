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

from src.core.entities.ics_206_models import (
    Ics206,
    Ics206Preparation,
    Ics206Hospitals,
    Ics206Transportation,
    Ics206MedicalAidStation,
    Ics206Approval,
)
from src.core.entities.imt_members_models.main_section_models import SafetyOfficer
from src.core.entities.imt_members_models.logistic_section_models import MedicalUnitLeader
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
    return f"{month} {day}{suffix} {year}"


async def read_item_by_id(model: Type[SQLModel], item_id: int, session: AsyncSession):
        item = await session.get(model, item_id)
        if not item:
            raise NotFoundException(f"{model.__name__} not found")
        return item
    
async def read_items_by_condition(model: Type[SQLModel], condition: Any, session: AsyncSession):
    query = select(model).where(condition)
    result = await session.execute(query)
    return result.scalars().all()

@router.post("/{id}")
async def export_docx(id: int, session: AsyncSession = Depends(get_session)):
    template_path = "src/infrastructure/templates/ics_206.docx"
    # output_path = f"src/infrastructure/templates/ics_206_{id}.docx"

    # Ambil data Ics201
    ics_206 = await read_item_by_id(Ics206, item_id=id, session=session)
    context = ics_206.model_dump()
    ics_206_id = ics_206.id
    context['is_utilized'] = '✓' if context['is_utilized'] else '✗'
    
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
    
    # Ambil Medical Aid Station terkait
    ics_206_medical_aid_stations = await read_items_by_condition(Ics206MedicalAidStation, Ics206MedicalAidStation.ics_206_id == ics_206_id, session=session)
    ics_206_medical_aid_station_list = [mas.model_dump() for mas in ics_206_medical_aid_stations]
    # Manipulasi boolean
    for mas in ics_206_medical_aid_station_list:
        mas['is_paramedic'] = '✓' if mas['is_paramedic'] else '✗'
    context['medical_aid_station'] = ics_206_medical_aid_station_list
    
    # Ambil Transportation terkait
    ics_206_transportations = await read_items_by_condition(Ics206Transportation, Ics206Transportation.ics_206_id == ics_206_id, session=session)
    ics_206_transportation_list = [t.model_dump() for t in ics_206_transportations]
    # Manipulasi boolean
    for t in ics_206_transportation_list:
        t['is_als'] = '✓' if t['is_als'] else '✗'
        t['is_bls'] = '✓' if t['is_bls'] else '✗'
    context['transportation'] = ics_206_transportation_list
    
    # Ambil Hospitals terkait
    ics_206_hospitals = await read_items_by_condition(Ics206Hospitals, Ics206Hospitals.ics_206_id == ics_206_id, session=session)
    ics_206_hospital_list = [h.model_dump() for h in ics_206_hospitals]
    # Manipulasi boolean
    for h in ics_206_hospital_list:
        h['is_trauma_center'] = '✓' if h['is_trauma_center'] else '✗'
        h['is_burn_center'] = '✓' if h['is_burn_center'] else '✗'
        h['is_helipad'] = '✓' if h['is_helipad'] else '✗'
    context['hospitals'] = ics_206_hospital_list

    # Ambil Preparation terkait
    ics_206_preparations = await read_items_by_condition(Ics206Preparation, Ics206Preparation.ics_206_id == ics_206_id, session=session)
    medical_unit_leader_id = ics_206_preparations[0].medical_unit_leader_id
    prepared_name = await read_item_by_id(MedicalUnitLeader, item_id=medical_unit_leader_id, session=session)
    context["prepared_name"] = prepared_name.name
    context["is_prepared"] = "✓" if ics_206_preparations[0].is_prepared else "✗"
    context['date_prepared'] = format_date_to_sentence(ics_206_preparations[0].date_prepared.strftime("%Y-%m-%d"))
    context['time_prepared'] = ics_206_preparations[0].time_prepared.strftime("%H:%M")
    
    # Ambil Approval terkait
    ics_206_approvals = await read_items_by_condition(Ics206Approval, Ics206Approval.ics_206_id == ics_206_id, session=session)
    approval_name = await read_item_by_id(SafetyOfficer, item_id=ics_206_approvals[0].safety_officer_id, session=session)
    context["approval_name"] = approval_name.name
    context["is_approved"] = "✓" if ics_206_approvals[0].is_approved else "✗"
    context['date_approved'] = format_date_to_sentence(ics_206_approvals[0].date_approved.strftime("%Y-%m-%d"))
    context['time_approved'] = ics_206_approvals[0].time_approved.strftime("%H:%M")
        
    # Muat template
    doc = DocxTemplate(template_path)

    # Render docxtpl
    doc.render(context)

    output_stream = BytesIO()
    doc.save(output_stream)
    output_stream.seek(0)  # Kembalikan pointer ke awal stream

    # # Simpan hasil
    # doc.save(output_path)
    
    return StreamingResponse(
        output_stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename=ics_206_{id}.docx"}
    )
    
    return FileResponse(
        output_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=f"ics_206_{id}.docx",
    )
