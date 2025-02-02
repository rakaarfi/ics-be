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

from src.core.entities.ics_202_models import Ics202, Ics202Approval, Ics202Preparation
from src.core.entities.imt_members_models.planning_section_models import PlanningSectionChief
from src.core.entities.imt_members_models.main_section_models import IncidentCommander
from src.core.entities.incident_data_models import IncidentData, OperationalPeriod
from src.infrastructure.config.database import get_session
from src.infrastructure.api.ics_202.ics_202 import read_ics_202_by_id
from src.infrastructure.api.incident_data import read_incident_data_by_id
from src.infrastructure.api.operational_period import read_operational_period_by_id
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

@router.post("/{id}")
async def export_docx(id: int, session: AsyncSession = Depends(get_session)):
    template_path = "src/infrastructure/templates/ics_202.docx"

    # Ambil data Ics201
    ics_202 = await read_item_by_id(Ics202, item_id=id, session=session)
    context = ics_202.model_dump()
    ics_202_id = ics_202.id
    context['is_required'] = "✓" if ics_202.is_required else "✗"
    context['ics_203'] = "✓" if ics_202.ics_203 else "✗"
    context['ics_204'] = "✓" if ics_202.ics_204 else "✗"
    context['ics_205'] = "✓" if ics_202.ics_205 else "✗"
    context['ics_205a'] = "✓" if ics_202.ics_205a else "✗"
    context['ics_206'] = "✓" if ics_202.ics_206 else "✗"
    context['ics_207'] = "✓" if ics_202.ics_207 else "✗"
    context['ics_208'] = "✓" if ics_202.ics_208 else "✗"
    context['map_chart'] = "✓" if ics_202.map_chart else "✗"
    context['weather_tides_currents'] = "✓" if ics_202.weather_tides_currents else "✗"    
    
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

    # Ambil Planning Section Chief terkait
    ics_202_preparations = await read_items_by_condition(Ics202Preparation, Ics202Preparation.ics_202_id == ics_202_id, session=session)
    planning_section_chief_id = ics_202_preparations[0].planning_section_chief_id
    planning_section_chief = await read_item_by_id(PlanningSectionChief, item_id=planning_section_chief_id, session=session)
    context["PSChief_name"] = planning_section_chief.name
    context["is_prepared"] = "✓" if ics_202_preparations[0].is_prepared else "✗"
    
    
    # Ambil Incident Commander terkait
    ics_202_approvals = await read_items_by_condition(Ics202Approval, Ics202Approval.ics_202_id == ics_202_id, session=session)
    incident_commander_id = ics_202_approvals[0].incident_commander_id
    incident_commander = await read_item_by_id(IncidentCommander, item_id=incident_commander_id, session=session)
    context["IC_name"] = incident_commander.name
    context['is_approved'] = "✓" if ics_202_approvals[0].is_approved else "✗"
    context['date_approved'] = format_date_to_sentence(ics_202_approvals[0].date_approved.strftime("%Y-%m-%d"))
    context['time_approved'] = ics_202_approvals[0].time_approved.strftime("%H:%M")
        
    # Muat template
    doc = DocxTemplate(template_path)

    # Render docxtpl
    doc.render(context)

    # Simpan docx
    output_stream = BytesIO()
    doc.save(output_stream)
    output_stream.seek(0)  # Kembalikan pointer ke awal stream
    
    return StreamingResponse(
        output_stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename=ics_206_{id}.docx"}
    )
