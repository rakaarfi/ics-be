from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func, select

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_204_models import Ics204
from src.core.entities.incident_data_models import IncidentData, OperationalPeriod
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException


router = APIRouter()

# Dependency to get the repository
def get_repository(session: AsyncSession = Depends(get_session)) -> BaseRepository:
    return BaseRepository(session)


# Endpoint untuk create
@router.post("/create/", summary="Create Ics 204", description="Create a new Ics 204")
async def create_ics_204(item: Ics204, repo: BaseRepository = Depends(get_repository)):
    return await repo.create_item(Ics204, item)


# Endpoint untuk read
@router.get("/read/")
async def read_ics_204(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(Ics204)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_ics_204_by_id(id: int, repo: BaseRepository = Depends(get_repository)):
    try:
        return await repo.read_item_by_id(Ics204, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk update
@router.put("/update/{id}")
async def update_ics_204(
    update_data: Ics204, id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.update_item(Ics204, id, update_data)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_ics_204(id: int, repo: BaseRepository = Depends(get_repository)):
    try:
        return await repo.delete_item(Ics204, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk read paginated
@router.get("/read-paginated/", response_model=PaginationResponse[List[Ics204]])
async def read_ics_204_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    if search:
        search_lower = f"%{search.lower()}%"

        # Create a subquery for IncidentData.name
        inner_query = select(IncidentData.id).where(
            func.lower(IncidentData.name).like(search_lower)
        )
        
        # Create the subquery to filter operational_period_id
        subquery = select(OperationalPeriod.id).where(
            OperationalPeriod.incident_id.in_(inner_query)
        )

        condition = (
            Ics204.operational_period_id.in_(subquery)
            | func.lower(Ics204.operation_section_chief_name).like(search_lower)
            | func.lower(Ics204.operation_section_chief_number).like(search_lower)
            | func.lower(Ics204.branch_director_name).like(search_lower)
            | func.lower(Ics204.branch_director_number).like(search_lower)
            | func.lower(Ics204.division_supervisor_name).like(search_lower)
            | func.lower(Ics204.division_supervisor_number).like(search_lower)
            | func.lower(Ics204.branch).like(search_lower)
            | func.lower(Ics204.division).like(search_lower)
            | func.lower(Ics204.staging_area).like(search_lower)
            | func.lower(Ics204.work_assignment).like(search_lower)
            | func.lower(Ics204.special_instructions).like(search_lower)
            | func.lower(Ics204.radio_channel_number).like(search_lower)
            | func.lower(Ics204.frequency).like(search_lower)
            | func.lower(Ics204.communication_mode).like(search_lower)
            | func.lower(Ics204.mobile_phone).like(search_lower)
        )

    return await repo.read_paginated_items(Ics204, page, limit, condition)
