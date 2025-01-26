from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.crud.crud import (create_item, delete_item, read_item_by_id,
                           read_items, read_paginated_items, update_item)
from app.models.imt_members_models.main_section_models import SafetyOfficer
from app.models.pagination_models import PaginationResponse
from app.utils.utils import imt_members_search_condition

router = APIRouter()


# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Safety Officer",
    description="Create a new Safety Officer",
)
async def create_safety_officer(
    item: SafetyOfficer, session: AsyncSession = Depends(get_session)
):
    return await create_item(SafetyOfficer, item, session)


# Endpoint untuk read
@router.get("/read/")
async def read_safety_officer(session: AsyncSession = Depends(get_session)):
    return await read_items(SafetyOfficer, session)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_safety_officer_by_id(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(SafetyOfficer, id, session)


# Endpoint untuk update
@router.put("/update/{id}")
async def update_safety_officer(
    update_data: SafetyOfficer, id: int, session: AsyncSession = Depends(get_session)
):
    return await update_item(SafetyOfficer, id, update_data, session)


# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_safety_officer(id: int, session: AsyncSession = Depends(get_session)):
    return await delete_item(SafetyOfficer, id, session)


# Endpoint untuk read paginated
@router.get("/read-paginated/", response_model=PaginationResponse[List[SafetyOfficer]])
async def read_safety_officer_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    session: AsyncSession = Depends(get_session),
):
    condition = None

    if search:
        condition = imt_members_search_condition(search, SafetyOfficer)

    return await read_paginated_items(SafetyOfficer, page, limit, session, condition)
