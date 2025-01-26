from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.crud.crud import (create_item, delete_item, read_item_by_id,
                           read_items, read_paginated_items, update_item)
from app.models.imt_members_models.logistic_section_models import LogisticSectionChief
from app.models.pagination_models import PaginationResponse
from app.utils.utils import imt_members_search_condition

router = APIRouter()


# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Logistic Section Chief",
    description="Create a new Logistic Section Chief",
)
async def create_logistic_section_chief(
    item: LogisticSectionChief, session: AsyncSession = Depends(get_session)
):
    return await create_item(LogisticSectionChief, item, session)


# Endpoint untuk read
@router.get("/read/")
async def read_logistic_section_chief(session: AsyncSession = Depends(get_session)):
    return await read_items(LogisticSectionChief, session)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_logistic_section_chief_by_id(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(LogisticSectionChief, id, session)


# Endpoint untuk update
@router.put("/update/{id}")
async def update_logistic_section_chief(
    update_data: LogisticSectionChief,
    id: int,
    session: AsyncSession = Depends(get_session),
):
    return await update_item(LogisticSectionChief, id, update_data, session)


# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_logistic_section_chief(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await delete_item(LogisticSectionChief, id, session)


# Endpoint untuk read paginated
@router.get(
    "/read-paginated/", response_model=PaginationResponse[List[LogisticSectionChief]]
)
async def read_logistic_section_chief_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    session: AsyncSession = Depends(get_session),
):
    condition = None

    if search:
        condition = imt_members_search_condition(search, LogisticSectionChief)

    return await read_paginated_items(
        LogisticSectionChief, page, limit, session, condition
    )
