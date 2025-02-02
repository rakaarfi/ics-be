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

from src.core.entities.ics_208_models import (
    Ics208,
    Ics208Preparation,
)
from src.core.entities.imt_members_models.main_section_models import SafetyOfficer
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
    template_path = "src/infrastructure/templates/ics_208.docx"
    # output_path = f"src/infrastructure/templates/ics_208_{id}.docx"

    # Ambil data Ics201
    ics_208 = await read_item_by_id(Ics208, item_id=id, session=session)
    context = ics_208.model_dump()
    ics_208_id = ics_208.id
    context['is_required'] = '✓' if context['is_required'] else '✗'
    
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

    # Ambil Preparation terkait
    ics_208_preparations = await read_items_by_condition(Ics208Preparation, Ics208Preparation.ics_208_id == ics_208_id, session=session)
    safety_officer_id = ics_208_preparations[0].safety_officer_id
    prepared_name = await read_item_by_id(SafetyOfficer, item_id=safety_officer_id, session=session)
    context["prepared_name"] = prepared_name.name
    context["is_prepared"] = "✓" if ics_208_preparations[0].is_prepared else "✗"
    context['date_prepared'] = format_date_to_sentence(ics_208_preparations[0].date_prepared.strftime("%Y-%m-%d"))
    context['time_prepared'] = ics_208_preparations[0].time_prepared.strftime("%H:%M")
        
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
        headers={"Content-Disposition": f"attachment; filename=ics_208_{id}.docx"}
    )
    
    return FileResponse(
        output_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=f"ics_208_{id}.docx",
    )
