from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.crud.crud import (create_item, delete_item, read_item_by_id,
                           read_items, read_paginated_items, update_item)
from app.models.imt_members_models.planning_section_models import DemobilizationUnitLeader
from app.models.pagination_models import PaginationResponse
from app.utils.utils import imt_members_search_condition

router = APIRouter()


# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Demobilization Unit Leader",
    description="Create a new Demobilization Unit Leader",
)
async def create_demobilization_unit_leader(
    item: DemobilizationUnitLeader, session: AsyncSession = Depends(get_session)
):
    return await create_item(DemobilizationUnitLeader, item, session)


# Endpoint untuk read
@router.get("/read/")
async def read_demobilization_unit_leader(session: AsyncSession = Depends(get_session)):
    return await read_items(DemobilizationUnitLeader, session)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_demobilization_unit_leader_by_id(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(DemobilizationUnitLeader, id, session)


# Endpoint untuk update
@router.put("/update/{id}")
async def update_demobilization_unit_leader(
    update_data: DemobilizationUnitLeader,
    id: int,
    session: AsyncSession = Depends(get_session),
):
    return await update_item(DemobilizationUnitLeader, id, update_data, session)


# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_demobilization_unit_leader(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await delete_item(DemobilizationUnitLeader, id, session)


# Endpoint untuk read paginated
@router.get(
    "/read-paginated/",
    response_model=PaginationResponse[List[DemobilizationUnitLeader]],
)
async def read_demobilization_unit_leader_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    session: AsyncSession = Depends(get_session),
):
    condition = None

    if search:
        condition = imt_members_search_condition(search, DemobilizationUnitLeader)

    return await read_paginated_items(
        DemobilizationUnitLeader, page, limit, session, condition
    )
