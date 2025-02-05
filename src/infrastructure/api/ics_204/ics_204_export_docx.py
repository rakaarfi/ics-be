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

from src.core.entities.ics_204_models import (
    Ics204,
    Ics204EquipmentAssigned,
    Ics204PersonnelAssigned,
    Ics204PreparationOSChief,
    Ics204PreparationRULeader
)
from src.core.entities.imt_members_models.main_section_models import OperationSectionChief
from src.core.entities.imt_members_models.planning_section_models import ResourcesUnitLeader
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
    template_path = "src/infrastructure/templates/ics_204.docx"

    # Ambil data Ics201
    ics_204 = await read_item_by_id(Ics204, item_id=id, session=session)
    context = ics_204.model_dump()
    ics_204_id = ics_204.id
    
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
    
    ocs_id = ics_204.operation_section_chief_id
    # Ambil Operational Section terkait
    operation_section_chief = await read_item_by_id(OperationSectionChief, item_id=ocs_id, session=session)
    context['osc_name'] = operation_section_chief.name
    context['ocs_number'] = operation_section_chief.mobile_phone
    
    # Ambil Personnel Assigned terkait
    ics_204_personnel = await read_items_by_condition(Ics204PersonnelAssigned, Ics204PersonnelAssigned.ics_204_id == ics_204_id, session=session)
    ics_204_personnel_list = [p.model_dump() for p in ics_204_personnel]
    context['personnel_assigned'] = ics_204_personnel_list
    
    # Ambil Equipment Assigned terkait
    ics_204_equipment = await read_items_by_condition(Ics204EquipmentAssigned, Ics204EquipmentAssigned.ics_204_id == ics_204_id, session=session)
    ics_204_equipment_list = [e.model_dump() for e in ics_204_equipment]
    context['equipment_assigned'] = ics_204_equipment_list

    # Ambil OSC Preparation terkait
    ics_204_preparations_osc = await read_items_by_condition(Ics204PreparationOSChief, Ics204PreparationOSChief.ics_204_id == ics_204_id, session=session)
    if ics_204_preparations_osc and len(ics_204_preparations_osc) > 0:
        operation_section_chief_id = ics_204_preparations_osc[0].operation_section_chief_id
        prepared_name = await read_item_by_id(OperationSectionChief, item_id=operation_section_chief_id, session=session)
        context["osc_prepared_name"] = prepared_name.name
        context["osc_is_prepared"] = "✓" if ics_204_preparations_osc[0].is_prepared else "✗"
        context['osc_date_prepared'] = format_date_to_sentence(ics_204_preparations_osc[0].date_prepared.strftime("%Y-%m-%d"))
        context['osc_time_prepared'] = ics_204_preparations_osc[0].time_prepared.strftime("%H:%M")
    else:
        # Jika tidak ada data, set nilai default agar tidak menyebabkan error
        context["osc_prepared_name"] = None
        context["osc_is_prepared"] = None
        context["osc_date_prepared"] = None
        context["osc_time_prepared"] = None
    
    # Ambil RUL Preparation terkait
    ics_204_preparations_rul = await read_items_by_condition(Ics204PreparationRULeader, Ics204PreparationRULeader.ics_204_id == ics_204_id, session=session)
    if ics_204_preparations_rul and len(ics_204_preparations_rul) > 0:
        resources_unit_leader_id = ics_204_preparations_rul[0].resources_unit_leader_id
        prepared_name = await read_item_by_id(ResourcesUnitLeader, item_id=resources_unit_leader_id, session=session)
        context["rul_prepared_name"] = prepared_name.name
        context["rul_is_prepared"] = "✓" if ics_204_preparations_rul[0].is_prepared else "✗"
        context['rul_date_prepared'] = format_date_to_sentence(ics_204_preparations_rul[0].date_prepared.strftime("%Y-%m-%d"))
        context['rul_time_prepared'] = ics_204_preparations_rul[0].time_prepared.strftime("%H:%M")
    else:
        # Jika tidak ada data, set nilai default agar tidak menyebabkan error
        context["rul_prepared_name"] = None
        context["rul_is_prepared"] = None
        context["rul_date_prepared"] = None
        context["rul_time_prepared"] = None
    
    # Tentukan apakah ada data OSC dan RUL
    osc_exists = len(ics_204_preparations_osc) > 0
    rul_exists = len(ics_204_preparations_rul) > 0

    # Buat daftar untuk menampung data yang akan dimunculkan
    prepared_data = []

    if osc_exists:
        prepared_data.append({
            "name": context["osc_prepared_name"],
            "position": "Operation Section Chief",
            "signature": context["osc_is_prepared"]
        })

    if rul_exists:
        prepared_data.append({
            "name": context["rul_prepared_name"],
            "position": "Resources Unit Leader",
            "signature": context["rul_is_prepared"]
        })

    # Tentukan tanggal/jam yang akan ditampilkan
    if osc_exists and rul_exists:
        # Jika keduanya ada, gunakan tanggal/jam dari OSC
        context['date_prepared'] = context['osc_date_prepared']
        context['time_prepared'] = context['osc_time_prepared']
    elif osc_exists:
        # Jika hanya OSC, gunakan data dari OSC
        context['date_prepared'] = context['osc_date_prepared']
        context['time_prepared'] = context['osc_time_prepared']
    elif rul_exists:
        # Jika hanya RUL, gunakan data dari RUL
        context['date_prepared'] = context['rul_date_prepared']
        context['time_prepared'] = context['rul_time_prepared']
    else:
        # Jika tidak ada data, kosongkan
        context['date_prepared'] = "N/A"
        context['time_prepared'] = "N/A"

    # Tambahkan prepared_data ke context untuk digunakan di template
    context['prepared_data'] = prepared_data

    # Muat template
    doc = DocxTemplate(template_path)

    # Render docxtpl
    doc.render(context)

    output_stream = BytesIO()
    doc.save(output_stream)
    output_stream.seek(0)  # Kembalikan pointer ke awal stream
    
    return StreamingResponse(
        output_stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename=ics_204_{id}.docx"}
    )
