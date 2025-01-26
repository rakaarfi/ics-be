from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.crud.crud import (create_item, delete_item, read_item_by_id,
                           read_items, read_paginated_items, update_item)
from app.models.imt_members_models.planning_section_models import PlanningSectionChief
from app.models.pagination_models import PaginationResponse
from app.utils.utils import imt_members_search_condition

router = APIRouter()


# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Planning Section Chief",
    description="Create a new Planning Section Chief",
)
async def create_planning_section_chief(
    item: PlanningSectionChief, session: AsyncSession = Depends(get_session)
):
    return await create_item(PlanningSectionChief, item, session)


# Endpoint untuk read
@router.get("/read/")
async def read_planning_section_chief(session: AsyncSession = Depends(get_session)):
    return await read_items(PlanningSectionChief, session)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_planning_section_chief_by_id(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(PlanningSectionChief, id, session)


# Endpoint untuk update
@router.put("/update/{id}")
async def update_planning_section_chief(
    update_data: PlanningSectionChief,
    id: int,
    session: AsyncSession = Depends(get_session),
):
    return await update_item(PlanningSectionChief, id, update_data, session)


# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_planning_section_chief(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await delete_item(PlanningSectionChief, id, session)


# Endpoint untuk read paginated
@router.get(
    "/read-paginated/", response_model=PaginationResponse[List[PlanningSectionChief]]
)
async def read_planning_section_chief_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    session: AsyncSession = Depends(get_session),
):
    condition = None

    if search:
        condition = imt_members_search_condition(search, PlanningSectionChief)

    return await read_paginated_items(
        PlanningSectionChief, page, limit, session, condition
    )
