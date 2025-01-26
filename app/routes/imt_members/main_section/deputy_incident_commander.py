from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.crud.crud import (create_item, delete_item, read_item_by_id,
                           read_items, read_paginated_items, update_item)
from app.models.imt_members_models.main_section_models import DeputyIncidentCommander
from app.models.pagination_models import PaginationResponse
from app.utils.utils import imt_members_search_condition

router = APIRouter()


# Endpoint untuk create
@router.post("/create/")
async def create_deputy_incident_commander(
    item: DeputyIncidentCommander, session: AsyncSession = Depends(get_session)
):
    return await create_item(DeputyIncidentCommander, item, session)


# Endpoint untuk read
@router.get("/read/")
async def read_deputy_incident_commander(session: AsyncSession = Depends(get_session)):
    return await read_items(DeputyIncidentCommander, session)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_deputy_incident_commander_by_id(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(DeputyIncidentCommander, id, session)


# Endpoint untuk update
@router.put("/update/{id}")
async def update_deputy_incident_commander(
    update_data: DeputyIncidentCommander,
    id: int,
    session: AsyncSession = Depends(get_session),
):
    return await update_item(DeputyIncidentCommander, id, update_data, session)


# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_deputy_incident_commander(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await delete_item(DeputyIncidentCommander, id, session)


# Endpoint untuk pagination
@router.get(
    "/read-paginated/", response_model=PaginationResponse[List[DeputyIncidentCommander]]
)
async def read_deputy_incident_commander_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    session: AsyncSession = Depends(get_session),
):
    condition = None

    if search:
        condition = imt_members_search_condition(search, DeputyIncidentCommander)

    return await read_paginated_items(
        DeputyIncidentCommander, page, limit, session, condition
    )
