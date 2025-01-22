from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models.imt_members.main_section import HumanCapitalOfficer
from app.config.database import get_session
from app.models.models import PaginationResponse
from app.crud.crud import (
    create_item, read_items, read_item_by_id, 
    update_item, delete_item, read_paginated_items
)
from app.utils.utils import imt_members_search_condition


router = APIRouter()

# Endpoint untuk create
@router.post("/create/")
async def create_human_capital_officer(
    item: HumanCapitalOfficer, 
    session: AsyncSession = Depends(get_session)
):
    return await create_item(HumanCapitalOfficer, item, session)


# Endpoint untuk read
@router.get("/read/")
async def read_human_capital_officer(session: AsyncSession = Depends(get_session)):
    return await read_items(HumanCapitalOfficer, session)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_human_capital_officer_by_id(
    id: int, 
    session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(HumanCapitalOfficer, id, session)


# Endpoint untuk update
@router.put("/update/{id}")
async def update_human_capital_officer(
    update_data: HumanCapitalOfficer,
    id: int,
    session: AsyncSession = Depends(get_session)
):
    return await update_item(HumanCapitalOfficer, id, update_data, session)

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_human_capital_officer(
    id: int, 
    session: AsyncSession = Depends(get_session)
):
    return await delete_item(HumanCapitalOfficer, id, session)


# Endpoint untuk read paginated
@router.get(
    "/read-paginated/", 
    response_model=PaginationResponse[List[HumanCapitalOfficer]]
)
async def read_human_capital_officer_paginated(
    page: int = 1, 
    limit: int = 10, 
    search: str = "",
    session: AsyncSession = Depends(get_session)
):
    condition = None
    
    if search:
        condition = imt_members_search_condition(search, HumanCapitalOfficer)
    
    return await read_paginated_items(HumanCapitalOfficer, page, limit, session, condition)
