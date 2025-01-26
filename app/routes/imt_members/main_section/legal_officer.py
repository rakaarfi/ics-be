from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.crud.crud import (create_item, delete_item, read_item_by_id,
                           read_items, read_paginated_items, update_item)
from app.models.imt_members_models.main_section_models import LegalOfficer
from app.models.pagination_models import PaginationResponse
from app.utils.utils import imt_members_search_condition

router = APIRouter()


# Endpoint untuk create
@router.post("/create/")
async def create_legal_officer(
    item: LegalOfficer, session: AsyncSession = Depends(get_session)
):
    return await create_item(LegalOfficer, item, session)


# Endpoint untuk read
@router.get("/read/")
async def read_legal_officer(session: AsyncSession = Depends(get_session)):
    return await read_items(LegalOfficer, session)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_legal_officer_by_id(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(LegalOfficer, id, session)


# Endpoint untuk update
@router.put("/update/{id}")
async def update_legal_officer(
    update_data: LegalOfficer, id: int, session: AsyncSession = Depends(get_session)
):
    return await update_item(LegalOfficer, id, update_data, session)


# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_legal_officer(id: int, session: AsyncSession = Depends(get_session)):
    return await delete_item(LegalOfficer, id, session)


# Endpoint untuk pagination
@router.get("/read-paginated/", response_model=PaginationResponse[List[LegalOfficer]])
async def read_legal_officer_with_pagination(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    session: AsyncSession = Depends(get_session),
):
    condition = None

    if search:
        condition = imt_members_search_condition(search, LegalOfficer)

    return await read_paginated_items(LegalOfficer, page, limit, session, condition)
