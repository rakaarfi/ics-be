from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models.imt_members.finance_section import ProcurementUnitLeader
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
    summary="Create Procurement Unit Leader", 
    description="Create a new Procurement Unit Leader"
)
async def create_procurement_unit_leader(
    item: ProcurementUnitLeader, 
    session: AsyncSession = Depends(get_session)
):
    return await create_item(ProcurementUnitLeader, item, session)

# Endpoint untuk read
@router.get("/read/")
async def read_procurement_unit_leader(session: AsyncSession = Depends(get_session)):
    return await read_items(ProcurementUnitLeader, session)

# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_procurement_unit_leader_by_id(
    id: int, 
    session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(ProcurementUnitLeader, id, session)

# Endpoint untuk update
@router.put("/update/{id}")
async def update_procurement_unit_leader(
    update_data: ProcurementUnitLeader,
    id: int,
    session: AsyncSession = Depends(get_session)
):
    return await update_item(ProcurementUnitLeader, id, update_data, session)

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_procurement_unit_leader(
    id: int, 
    session: AsyncSession = Depends(get_session)
):
    return await delete_item(ProcurementUnitLeader, id, session)

# Endpoint untuk read paginated
@router.get("/read-paginated/", 
            response_model=PaginationResponse[List[ProcurementUnitLeader]])
async def read_procurement_unit_leader_paginated(
    page: int = 1, 
    limit: int = 10, 
    search: str = "",
    session: AsyncSession = Depends(get_session)
):
    condition = None
    
    if search:
        condition = imt_members_search_condition(search, ProcurementUnitLeader)
    
    return await read_paginated_items(ProcurementUnitLeader, page, limit, session, condition)