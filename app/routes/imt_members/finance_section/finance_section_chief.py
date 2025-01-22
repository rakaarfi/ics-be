from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models.imt_members.finance_section import FinanceSectionChief
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
    summary="Create Finance Section Chief", 
    description="Create a new Finance Section Chief"
)
async def create_finance_section_chief(
    item: FinanceSectionChief, 
    session: AsyncSession = Depends(get_session)
):
    return await create_item(FinanceSectionChief, item, session)

# Endpoint untuk read
@router.get("/read/")
async def read_finance_section_chief(session: AsyncSession = Depends(get_session)):
    return await read_items(FinanceSectionChief, session)

# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_finance_section_chief_by_id(
    id: int, 
    session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(FinanceSectionChief, id, session)

# Endpoint untuk update
@router.put("/update/{id}")
async def update_finance_section_chief(
    update_data: FinanceSectionChief,
    id: int,
    session: AsyncSession = Depends(get_session)
):
    return await update_item(FinanceSectionChief, id, update_data, session)

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_finance_section_chief(
    id: int, 
    session: AsyncSession = Depends(get_session)
):
    return await delete_item(FinanceSectionChief, id, session)

# Endpoint untuk read paginated
@router.get("/read-paginated/", 
            response_model=PaginationResponse[List[FinanceSectionChief]])
async def read_finance_section_chief_paginated(
    page: int = 1, 
    limit: int = 10, 
    search: str = "",
    session: AsyncSession = Depends(get_session)
):
    condition = None
    
    if search:
        condition = imt_members_search_condition(search, FinanceSectionChief)
    
    return await read_paginated_items(FinanceSectionChief, page, limit, session, condition)