from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.crud.crud import (create_item, delete_item, read_item_by_id,
                           read_items, read_paginated_items, update_item)
from app.models.imt_members_models.logistic_section_models import CommunicationUnitLeader
from app.models.pagination_models import PaginationResponse
from app.utils.utils import imt_members_search_condition

router = APIRouter()


# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Communication Unit Leader",
    description="Create a new Communication Unit Leader",
)
async def create_communication_unit_leader(
    item: CommunicationUnitLeader, session: AsyncSession = Depends(get_session)
):
    return await create_item(CommunicationUnitLeader, item, session)


# Endpoint untuk read
@router.get("/read/")
async def read_communication_unit_leader(session: AsyncSession = Depends(get_session)):
    return await read_items(CommunicationUnitLeader, session)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_communication_unit_leader_by_id(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(CommunicationUnitLeader, id, session)


# Endpoint untuk update
@router.put("/update/{id}")
async def update_communication_unit_leader(
    update_data: CommunicationUnitLeader,
    id: int,
    session: AsyncSession = Depends(get_session),
):
    return await update_item(CommunicationUnitLeader, id, update_data, session)


# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_communication_unit_leader(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await delete_item(CommunicationUnitLeader, id, session)


# Endpoint untuk pagination
@router.get(
    "/read-paginated/", response_model=PaginationResponse[List[CommunicationUnitLeader]]
)
async def read_communication_unit_leader_with_pagination(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    session: AsyncSession = Depends(get_session),
):
    condition = None

    if search:
        condition = imt_members_search_condition(search, CommunicationUnitLeader)

    return await read_paginated_items(
        CommunicationUnitLeader, page, limit, session, condition
    )
