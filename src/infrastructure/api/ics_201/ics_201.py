from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func, select

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_201_models import Ics201
from src.core.entities.incident_data_models import IncidentData
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException


router = APIRouter()

# Dependency to get the repository
def get_repository(session: AsyncSession = Depends(get_session)) -> BaseRepository:
    return BaseRepository(session)


# Endpoint untuk create
@router.post("/create/", summary="Create Ics 201", description="Create a new Ics 201")
async def create_ics_201(item: Ics201, repo: BaseRepository = Depends(get_repository)):
    return await repo.create_item(Ics201, item)


# Endpoint untuk read
@router.get("/read/")
async def read_ics_201(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(Ics201)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_ics_201_by_id(id: int, repo: BaseRepository = Depends(get_repository)):
    try:
        return await repo.read_item_by_id(Ics201, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk update
@router.put("/update/{id}")
async def update_ics_201(
    update_data: Ics201, id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.update_item(Ics201, id, update_data)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_ics_201(id: int, repo: BaseRepository = Depends(get_repository)):
    try:
        return await repo.delete_item(Ics201, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk read paginated
@router.get("/read-paginated/", response_model=PaginationResponse[List[Ics201]])
async def read_ics_201_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    if search:
        search_lower = f"%{search.lower()}%"

        # Create a subquery for IncidentData.name
        subquery = select(IncidentData.id).where(
            func.lower(IncidentData.name).like(search_lower)
        )

        condition = (
            Ics201.incident_id.in_(subquery)
            | func.lower(func.to_char(Ics201.date_initiated, "YYYY-MM-DD")).like(
                search_lower
            )
            | func.lower(func.to_char(Ics201.time_initiated, "HH24:MI")).like(
                search_lower
            )
            | func.lower(Ics201.map_sketch).like(search_lower)
            | func.lower(Ics201.situation_summary).like(search_lower)
            | func.lower(Ics201.objectives).like(search_lower)
        )

    return await repo.read_paginated_items(Ics201, page, limit, condition)
