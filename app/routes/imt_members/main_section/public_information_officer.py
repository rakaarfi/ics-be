from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models.imt_members.main_section import PublicInformationOfficer
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
    summary="Create Public Information Officer", 
    description="Create a new Public Information Officer"
)
async def create_public_information_officer(
    item: PublicInformationOfficer, 
    session: AsyncSession = Depends(get_session)
):
    return await create_item(PublicInformationOfficer, item, session)


# Endpoint untuk read
@router.get("/read/")
async def read_public_information_officer(session: AsyncSession = Depends(get_session)):
    return await read_items(PublicInformationOfficer, session)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_public_information_officer_by_id(
    id: int, 
    session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(PublicInformationOfficer, id, session)


# Endpoint untuk update
@router.put("/update/{id}")
async def update_public_information_officer(
    update_data: PublicInformationOfficer,
    id: int,
    session: AsyncSession = Depends(get_session)
):
    return await update_item(PublicInformationOfficer, id, update_data, session)


# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_public_information_officer(
    id: int, 
    session: AsyncSession = Depends(get_session)
):
    return await delete_item(PublicInformationOfficer, id, session)


# Endpoint untuk read paginated
@router.get("/read-paginated/", 
            response_model=PaginationResponse[List[PublicInformationOfficer]])
async def read_public_information_officer_paginated(
    page: int = 1, 
    limit: int = 10, 
    search: str = "",
    session: AsyncSession = Depends(get_session)
):
    condition = None
    
    if search:
        condition = imt_members_search_condition(search, PublicInformationOfficer)
    
    return await read_paginated_items(PublicInformationOfficer, page, limit, session, condition)
