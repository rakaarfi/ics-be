from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.incident_data_models import IncidentData
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException

router = APIRouter()

# Dependency untuk mendapatkan repository
def get_repository(session: AsyncSession = Depends(get_session)):
    return BaseRepository(session)


# Endpoint untuk create
@router.post(
    "/create/", summary="Create Incident Data", description="Create a new Incident Data"
)
async def create_incident_data(
    item: IncidentData, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_item(IncidentData, item)


# Endpoint untuk read
@router.get("/read/")
async def read_incident_data(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(IncidentData)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_incident_data_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(IncidentData, id)
    except NotFoundException as e:
        raise e


# Endpoint untuk update
@router.put("/update/{id}")
async def update_incident_data(
    update_data: IncidentData, 
    id: int, 
    repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.update_item(IncidentData, id, update_data)
    except NotFoundException as e:
        raise e


# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_incident_data(id: int, repo: BaseRepository = Depends(get_repository)):
    try:
        return await repo.delete_item(IncidentData, id)
    except NotFoundException as e:
        raise e


# Endpoint untuk pagination
@router.get("/read-paginated/", response_model=PaginationResponse[List[IncidentData]])
async def read_incident_data_with_pagination(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    if search:
        search_lower = f"%{search.lower()}%"
        condition = (
            func.lower(IncidentData.no).like(search_lower)
            | func.lower(IncidentData.name).like(search_lower)
            | func.lower(func.to_char(IncidentData.date_incident, "YYYY-MM-DD")).like(
                search_lower
            )
            | func.lower(func.to_char(IncidentData.time_incident, "HH24:MI")).like(
                search_lower
            )
            | func.lower(IncidentData.timezone).like(search_lower)
            | func.lower(IncidentData.location).like(search_lower)
            | func.lower(IncidentData.description).like(search_lower)
        )

    return await repo.read_paginated_items(IncidentData, page, limit, condition)
