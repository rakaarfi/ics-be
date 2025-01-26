from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.crud.crud import (create_item, delete_item, read_item_by_id,
                           read_items, read_paginated_items, update_item)
from app.models.imt_members_models.main_section_models import OperationSectionChief
from app.models.pagination_models import PaginationResponse
from app.utils.utils import imt_members_search_condition

router = APIRouter()


# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Operation Section Chief",
    description="Create a new Operation Section Chief",
)
async def create_operation_section_chief(
    item: OperationSectionChief, session: AsyncSession = Depends(get_session)
):
    return await create_item(OperationSectionChief, item, session)


# Endpoint untuk read
@router.get("/read/")
async def read_operation_section_chief(session: AsyncSession = Depends(get_session)):
    return await read_items(OperationSectionChief, session)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_operation_section_chief_by_id(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(OperationSectionChief, id, session)


# Endpoint untuk update
@router.put("/update/{id}")
async def update_operation_section_chief(
    update_data: OperationSectionChief,
    id: int,
    session: AsyncSession = Depends(get_session),
):
    return await update_item(OperationSectionChief, id, update_data, session)


# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_operation_section_chief(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await delete_item(OperationSectionChief, id, session)


# Endpoint untuk read paginated
@router.get(
    "/read-paginated/", response_model=PaginationResponse[List[OperationSectionChief]]
)
async def read_operation_section_chief_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    session: AsyncSession = Depends(get_session),
):
    condition = None

    if search:
        condition = imt_members_search_condition(search, OperationSectionChief)

    return await read_paginated_items(
        OperationSectionChief, page, limit, session, condition
    )
