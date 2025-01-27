from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func, select

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_205_models import Ics205
from src.core.entities.incident_data_models import IncidentData, OperationalPeriod
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException


router = APIRouter()

# Dependency to get the repository
def get_repository(session: AsyncSession = Depends(get_session)) -> BaseRepository:
    return BaseRepository(session)


# Endpoint untuk create
@router.post("/create/", summary="Create Ics 205", description="Create a new Ics 205")
async def create_ics_205(item: Ics205, repo: BaseRepository = Depends(get_repository)):
    return await repo.create_item(Ics205, item)


# Endpoint untuk read
@router.get("/read/")
async def read_ics_205(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(Ics205)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_ics_205_by_id(id: int, repo: BaseRepository = Depends(get_repository)):
    try:
        return await repo.read_item_by_id(Ics205, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk update
@router.put("/update/{id}")
async def update_ics_205(
    update_data: Ics205, id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.update_item(Ics205, id, update_data)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_ics_205(id: int, repo: BaseRepository = Depends(get_repository)):
    try:
        return await repo.delete_item(Ics205, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk read paginated
@router.get("/read-paginated/", response_model=PaginationResponse[List[Ics205]])
async def read_ics_205_paginated(
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
            Ics205.operational_period_id.in_(subquery)
            | func.lower(Ics205.special_instructions).like(search_lower)
        )

    return await repo.read_paginated_items(Ics205, page, limit, condition)
