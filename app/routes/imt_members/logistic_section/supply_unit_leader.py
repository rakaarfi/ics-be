from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models.imt_members.logistic_section import SupplyUnitLeader
from app.config.database import get_session
from app.models.models import PaginationResponse
from app.crud.crud import (
    create_item, read_items, read_item_by_id,
    update_item, delete_item, read_paginated_items
)
from app.utils.utils import imt_members_search_condition


router = APIRouter()

# Endpoint untuk create
@router.post(
    "/create/", 
    summary="Create Supply Unit Leader", 
    description="Create a new Supply Unit Leader"
)
async def create_supply_unit_leader(
    item: SupplyUnitLeader, 
    session: AsyncSession = Depends(get_session)
):
    return await create_item(SupplyUnitLeader, item, session)

# Endpoint untuk read
@router.get("/read/")
async def read_supply_unit_leader(session: AsyncSession = Depends(get_session)):
    return await read_items(SupplyUnitLeader, session)

# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_supply_unit_leader_by_id(
    id: int, 
    session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(SupplyUnitLeader, id, session)

# Endpoint untuk update
@router.put("/update/{id}")
async def update_supply_unit_leader(
    update_data: SupplyUnitLeader,
    id: int,
    session: AsyncSession = Depends(get_session)
):
    return await update_item(SupplyUnitLeader, id, update_data, session)

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_supply_unit_leader(
    id: int, 
    session: AsyncSession = Depends(get_session)
):
    return await delete_item(SupplyUnitLeader, id, session)

# Endpoint untuk read paginated
@router.get("/read-paginated/", 
            response_model=PaginationResponse[List[SupplyUnitLeader]])
async def read_supply_unit_leader_paginated(
    page: int = 1, 
    limit: int = 10, 
    search: str = "",
    session: AsyncSession = Depends(get_session)
):
    condition = None
    
    if search:
        condition = imt_members_search_condition(search, SupplyUnitLeader)
    
    return await read_paginated_items(
        SupplyUnitLeader, 
        page, 
        limit, 
        session,
        condition
    )