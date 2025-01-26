from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.crud.crud import (create_item, delete_item, read_item_by_id,
                           read_items, read_paginated_items, update_item)
from app.models.imt_members_models.planning_section_models import ResourcesUnitLeader
from app.models.pagination_models import PaginationResponse
from app.utils.utils import imt_members_search_condition

router = APIRouter()


# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Resources Unit Leader",
    description="Create a new Resources Unit Leader",
)
async def create_resources_unit_leader(
    item: ResourcesUnitLeader, session: AsyncSession = Depends(get_session)
):
    return await create_item(ResourcesUnitLeader, item, session)


# Endpoint untuk read
@router.get("/read/")
async def read_resources_unit_leader(session: AsyncSession = Depends(get_session)):
    return await read_items(ResourcesUnitLeader, session)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_resources_unit_leader_by_id(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(ResourcesUnitLeader, id, session)


# Endpoint untuk update
@router.put("/update/{id}")
async def update_resources_unit_leader(
    update_data: ResourcesUnitLeader,
    id: int,
    session: AsyncSession = Depends(get_session),
):
    return await update_item(ResourcesUnitLeader, id, update_data, session)


# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_resources_unit_leader(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await delete_item(ResourcesUnitLeader, id, session)


# Endpoint untuk read paginated
@router.get(
    "/read-paginated/", response_model=PaginationResponse[List[ResourcesUnitLeader]]
)
async def read_resources_unit_leader_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    session: AsyncSession = Depends(get_session),
):
    condition = None

    if search:
        condition = imt_members_search_condition(search, ResourcesUnitLeader)

    return await read_paginated_items(
        ResourcesUnitLeader, page, limit, session, condition
    )
