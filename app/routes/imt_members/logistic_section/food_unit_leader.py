from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models.imt_members.logistic_section import FoodUnitLeader
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
    summary="Create Food Unit Leader", 
    description="Create a new Food Unit Leader"
)
async def create_food_unit_leader(
    item: FoodUnitLeader, 
    session: AsyncSession = Depends(get_session)
):
    return await create_item(FoodUnitLeader, item, session)

# Endpoint untuk read
@router.get("/read/")
async def read_food_unit_leader(session: AsyncSession = Depends(get_session)):
    return await read_items(FoodUnitLeader, session)

# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_food_unit_leader_by_id(
    id: int, 
    session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(FoodUnitLeader, id, session)

# Endpoint untuk update
@router.put("/update/{id}")
async def update_food_unit_leader(
    update_data: FoodUnitLeader,
    id: int,
    session: AsyncSession = Depends(get_session)
):
    return await update_item(FoodUnitLeader, id, update_data, session)

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_food_unit_leader(
    id: int, 
    session: AsyncSession = Depends(get_session)
):
    return await delete_item(FoodUnitLeader, id, session)

# Endpoint untuk read paginated
@router.get("/read-paginated/", 
            response_model=PaginationResponse[List[FoodUnitLeader]])
async def read_food_unit_leader_paginated(
    page: int = 1, 
    limit: int = 10, 
    search: str = "",
    session: AsyncSession = Depends(get_session)
):
    condition = None
    
    if search:
        condition = imt_members_search_condition(search, FoodUnitLeader)
    
    return await read_paginated_items(FoodUnitLeader, page, limit, session, condition)