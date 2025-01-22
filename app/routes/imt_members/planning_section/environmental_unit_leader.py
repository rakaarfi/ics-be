from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models.imt_members.planning_section import EnvironmentalUnitLeader
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
    summary="Create Environmental Unit Leader", 
    description="Create a new Environmental Unit Leader"
)
async def create_environmental_unit_leader(
    item: EnvironmentalUnitLeader, 
    session: AsyncSession = Depends(get_session)
):
    return await create_item(EnvironmentalUnitLeader, item, session)


# Endpoint untuk read
@router.get("/read/")    
async def read_environmental_unit_leader(session: AsyncSession = Depends(get_session)):
    return await read_items(EnvironmentalUnitLeader, session)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_environmental_unit_leader_by_id(
    id: int, 
    session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(EnvironmentalUnitLeader, id, session)


# Endpoint untuk update
@router.put("/update/{id}") 
async def update_environmental_unit_leader(
    update_data: EnvironmentalUnitLeader,
    id: int,
    session: AsyncSession = Depends(get_session)
):
    return await update_item(EnvironmentalUnitLeader, id, update_data, session)


# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_environmental_unit_leader(
    id: int, 
    session: AsyncSession = Depends(get_session)
):
    return await delete_item(EnvironmentalUnitLeader, id, session)


# Endpoint untuk read paginated
@router.get("/read-paginated/", 
            response_model=PaginationResponse[List[EnvironmentalUnitLeader]])
async def read_environmental_unit_leader_paginated(
    page: int = 1, 
    limit: int = 10, 
    search: str = "",
    session: AsyncSession = Depends(get_session)
):
    condition = None
    
    if search:
        condition = imt_members_search_condition(search, EnvironmentalUnitLeader)
    
    return await read_paginated_items(EnvironmentalUnitLeader, page, limit, session, condition)
