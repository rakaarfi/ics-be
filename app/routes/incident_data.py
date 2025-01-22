from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from sqlmodel import func
from typing import List

from app.models.incident_data import IncidentData
from app.config.database import get_session
from app.models.models import PaginationResponse
from app.crud.crud import (
    create_item, read_items, read_item_by_id,
    update_item, delete_item, read_paginated_items
)

router = APIRouter()

# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Incident Data",
    description="Create a new Incident Data"
)
async def create_incident_data(
    item: IncidentData,
    session: AsyncSession = Depends(get_session)
):
    return await create_item(IncidentData, item, session)

# Endpoint untuk read
@router.get("/read/")
async def read_incident_data(session: AsyncSession = Depends(get_session)):
    return await read_items(IncidentData, session)

# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_incident_data_by_id(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(IncidentData, id, session)

# Endpoint untuk update
@router.put("/update/{id}")
async def update_incident_data(
    update_data: IncidentData,
    id: int,
    session: AsyncSession = Depends(get_session)
):
    return await update_item(IncidentData, id, update_data, session)

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_incident_data(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    return await delete_item(IncidentData, id, session)

# Endpoint untuk pagination
@router.get(
    "/read-paginated/",
    response_model=PaginationResponse[List[IncidentData]]
)
async def read_incident_data_with_pagination(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    session: AsyncSession = Depends(get_session)
):
    condition = None
    
    if search:
        search_lower = f"%{search.lower()}%"
        condition = (
                func.lower(IncidentData.no).like(search_lower) |
                func.lower(IncidentData.name).like(search_lower) |
                func.lower(func.to_char(IncidentData.date_incident, 'YYYY-MM-DD')).like(search_lower) |
                func.lower(func.to_char(IncidentData.time_incident, 'HH24:MI')).like(search_lower) |
                func.lower(IncidentData.timezone).like(search_lower) |
                func.lower(IncidentData.location).like(search_lower) |
                func.lower(IncidentData.description).like(search_lower)
            )
    
    return await read_paginated_items(
        IncidentData,
        page,
        limit,
        session,
        condition
    )