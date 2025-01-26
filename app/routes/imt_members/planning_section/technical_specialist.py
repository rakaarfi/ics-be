from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.crud.crud import (create_item, delete_item, read_item_by_id,
                           read_items, read_paginated_items, update_item)
from app.models.imt_members_models.planning_section_models import TechnicalSpecialist
from app.models.pagination_models import PaginationResponse
from app.utils.utils import imt_members_search_condition

router = APIRouter()


# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Technical Specialist",
    description="Create a new Technical Specialist",
)
async def create_technical_specialist(
    item: TechnicalSpecialist, session: AsyncSession = Depends(get_session)
):
    return await create_item(TechnicalSpecialist, item, session)


# Endpoint untuk read
@router.get("/read/")
async def read_technical_specialist(session: AsyncSession = Depends(get_session)):
    return await read_items(TechnicalSpecialist, session)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_technical_specialist_by_id(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(TechnicalSpecialist, id, session)


# Endpoint untuk update
@router.put("/update/{id}")
async def update_technical_specialist(
    update_data: TechnicalSpecialist,
    id: int,
    session: AsyncSession = Depends(get_session),
):
    return await update_item(TechnicalSpecialist, id, update_data, session)


# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_technical_specialist(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await delete_item(TechnicalSpecialist, id, session)


# Endpoint untuk read paginated
@router.get(
    "/read-paginated/", response_model=PaginationResponse[List[TechnicalSpecialist]]
)
async def read_technical_specialist_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    session: AsyncSession = Depends(get_session),
):
    condition = None

    if search:
        condition = imt_members_search_condition(search, TechnicalSpecialist)

    return await read_paginated_items(
        TechnicalSpecialist, page, limit, session, condition
    )
