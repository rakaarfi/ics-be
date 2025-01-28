import os
from datetime import datetime

from docx.shared import Inches
from docxtpl import (DocxTemplate,  # Menggunakan docxtpl untuk templating
                     InlineImage)
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.infrastructure.config.database import get_session
from src.core.entities.ics_201_models import Ics201Chart, IcsChartBase
from src.core.entities.imt_members_models.finance_section_models import *
from src.core.entities.imt_members_models.logistic_section_models import *
from src.core.entities.imt_members_models.main_section_models import *
from src.core.entities.imt_members_models.planning_section_models import *
from src.infrastructure.api.ics_201.actions_strategies_tactics import \
    read_actions_strategies_tactics_by_ics_id
from src.infrastructure.api.ics_201.chart import read_ics_chart_by_ics_id
from src.infrastructure.api.ics_201.ics_201 import read_ics_201_by_id
from src.infrastructure.api.ics_201.resource_summary import \
    read_resource_summary_by_ics_201_id
from src.infrastructure.api.incident_data import read_incident_data_by_id

router = APIRouter()

def format_date_to_sentence(date_str):
    # Parse tanggal dari string ke objek datetime
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    # Ambil hari, bulan, dan tahun
    day = date_obj.day
    month = date_obj.strftime("%B")  # Nama bulan (e.g., January)
    year = date_obj.year

    # Tambahkan suffix untuk hari
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]

    # Gabungkan menjadi kalimat
    return f"{day}{suffix} {month} {year}"


@router.post("/export_docx/{id}")
async def export_docx(id: int, session: AsyncSession = Depends(get_session)):
    template_path = "docx_template/ics_201.docx"
    output_path = f"docx_template/ics_201_{id}.docx"

    # Ambil data Ics201
    ics_201 = await read_ics_201_by_id(id, session)
    context = ics_201.dict()
    context["date_initiated"] = format_date_to_sentence(
        context["date_initiated"].strftime("%Y-%m-%d")
    )

    incident_id = context["incident_id"]
    # Ambil incident_data yang terkait
    incident_data = await read_incident_data_by_id(id=incident_id, session=session)
    context["incident_data"] = incident_data
    context["incident_name"] = incident_data.name
    context["incident_no"] = incident_data.no

    # Ambil data resource_summary yang terkait
    resource_summaries = await read_resource_summary_by_ics_201_id(id, session)
    resource_summaries_list = [rs.dict() for rs in resource_summaries]

    # Manipulasi is_arrived
    for rs in resource_summaries_list:
        rs["is_arrived"] = "✓" if rs["is_arrived"] else "✗"
        rs["date_ordered"] = format_date_to_sentence(
            rs["date_ordered"].strftime("%Y-%m-%d")
        )
        rs["time_ordered"] = rs["time_ordered"].strftime("%H:%M")

    context["resource_summaries"] = resource_summaries_list

    # Ambil data actions_strategies_tactics yang terkait
    actions_strategies_tactics = await read_actions_strategies_tactics_by_ics_id(
        id, session
    )
    actions_strategies_tactics_list = [ast.dict() for ast in actions_strategies_tactics]

    # Manipulasi time_initiated
    for ast in actions_strategies_tactics_list:
        ast["time_initiated"] = ast["time_initiated"].strftime("%H:%M")

    context["actions_strategies_tactics"] = actions_strategies_tactics_list

    # Ambil data chart yang terkait
    charts = await read_ics_chart_by_ics_id(id, session)
    if charts:
        chart = charts[0]  # Ambil chart pertama dari list
        chart_data = await read_docx_chart(chart.id, session)
        context.update(chart_data.dict())  # Tambahkan data nama ke context
    else:
        raise HTTPException(status_code=404, detail="Chart tidak ditemukan")

    # Direktori tempat gambar disimpan
    image_directory = "src/infrastructure/storage/uploaded_files"
    map_sketch_filename = context.get("map_sketch")

    # Muat template
    doc = DocxTemplate(template_path)

    # Kalau kolom map_sketch ada isinya, jadikan InlineImage
    if map_sketch_filename:
        image_path = os.path.join(image_directory, map_sketch_filename)
        if os.path.exists(image_path):
            context["map_sketch"] = InlineImage(doc, image_path, width=Inches(4.0))
        else:
            # Bila file gambar tidak ditemukan, kosongkan saja atau beri tanda
            context["map_sketch"] = "Gambar tidak ditemukan"

    # Render docxtpl
    doc.render(context)

    # Simpan hasil
    doc.save(output_path)

    return FileResponse(
        output_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=f"ics_201_{id}.docx",
    )


async def read_docx_chart(
    id: int, session: AsyncSession = Depends(get_session)
) -> IcsChartBase:
    # Query construction remains the same
    statement = (
        select(
            IncidentCommander.name.label("incident_commander_name"),
            DeputyIncidentCommander.name.label("deputy_incident_commander_name"),
            SafetyOfficer.name.label("safety_officer_name"),
            PublicInformationOfficer.name.label("public_information_officer_name"),
            LiaisonOfficer.name.label("liaison_officer_name"),
            LegalOfficer.name.label("legal_officer_name"),
            HumanCapitalOfficer.name.label("human_capital_officer_name"),
            OperationSectionChief.name.label("operation_section_chief_name"),
            PlanningSectionChief.name.label("planning_section_chief_name"),
            SituationUnitLeader.name.label("situation_unit_leader_name"),
            ResourcesUnitLeader.name.label("resources_unit_leader_name"),
            DocumentationUnitLeader.name.label("documentation_unit_leader_name"),
            DemobilizationUnitLeader.name.label("demobilization_unit_leader_name"),
            EnvironmentalUnitLeader.name.label("environmental_unit_leader_name"),
            TechnicalSpecialist.name.label("technical_specialist_name"),
            LogisticSectionChief.name.label("logistic_section_chief_name"),
            CommunicationUnitLeader.name.label("communication_unit_leader_name"),
            MedicalUnitLeader.name.label("medical_unit_leader_name"),
            FoodUnitLeader.name.label("food_unit_leader_name"),
            FacilityUnitLeader.name.label("facility_unit_leader_name"),
            SupplyUnitLeader.name.label("supply_unit_leader_name"),
            TransportationUnitLeader.name.label("transportation_unit_leader_name"),
            FinanceSectionChief.name.label("finance_section_chief_name"),
            ProcurementUnitLeader.name.label("procurement_unit_leader_name"),
            CompensationClaimUnitLeader.name.label(
                "compensation_claim_unit_leader_name"
            ),
            CostUnitLeader.name.label("cost_unit_leader_name"),
            TimeUnitLeader.name.label("time_unit_leader_name"),
        )
        .join(Ics201Chart.incident_commander)
        .join(Ics201Chart.deputy_incident_commander)
        .join(Ics201Chart.safety_officer)
        .join(Ics201Chart.public_information_officer)
        .join(Ics201Chart.liaison_officer)
        .join(Ics201Chart.legal_officer)
        .join(Ics201Chart.human_capital_officer)
        .join(Ics201Chart.operation_section_chief)
        .join(Ics201Chart.planning_section_chief)
        .join(Ics201Chart.situation_unit_leader)
        .join(Ics201Chart.resources_unit_leader)
        .join(Ics201Chart.documentation_unit_leader)
        .join(Ics201Chart.demobilization_unit_leader)
        .join(Ics201Chart.environmental_unit_leader)
        .join(Ics201Chart.technical_specialist)
        .join(Ics201Chart.logistic_section_chief)
        .join(Ics201Chart.communication_unit_leader)
        .join(Ics201Chart.medical_unit_leader)
        .join(Ics201Chart.food_unit_leader)
        .join(Ics201Chart.facility_unit_leader)
        .join(Ics201Chart.supply_unit_leader)
        .join(Ics201Chart.transportation_unit_leader)
        .join(Ics201Chart.finance_section_chief)
        .join(Ics201Chart.procurement_unit_leader)
        .join(Ics201Chart.compensation_claim_unit_leader)
        .join(Ics201Chart.cost_unit_leader)
        .join(Ics201Chart.time_unit_leader)
        .where(Ics201Chart.id == id)
    )

    result = await session.execute(statement)
    data = result.first()

    if not data:
        raise HTTPException(status_code=404, detail="Item not found")

    return IcsChartBase(**data._asdict())
