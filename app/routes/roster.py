from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func
from typing import List

from app.models.roster import ImtRoster
from app.config.database import get_session
from app.models.models import PaginationResponse
from app.crud.crud import (
    create_item, read_items, read_item_by_id,
    update_item, delete_item, read_paginated_items
)

router = APIRouter()

@router.post("/create/", summary="Create Imt Roster", description="Create a new Imt Roster")
async def create_imt_roster(
    item: ImtRoster,
    session: AsyncSession = Depends(get_session)
):
    return await create_item(ImtRoster, item, session)

@router.get("/read/")
async def read_imt_roster(session: AsyncSession = Depends(get_session)):
    return await read_items(ImtRoster, session)

@router.get("/read/{id}")
async def read_imt_roster_by_id(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(ImtRoster, id, session)

@router.put("/update/{id}")
async def update_imt_roster(
    update_data: ImtRoster,
    id: int,
    session: AsyncSession = Depends(get_session)
):
    return await update_item(ImtRoster, id, update_data, session)

@router.delete("/delete/{id}")
async def delete_imt_roster(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    return await delete_item(ImtRoster, id, session)

@router.get(
    "/read-paginated/",
    response_model=PaginationResponse[List[ImtRoster]]
)
async def read_imt_roster_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    session: AsyncSession = Depends(get_session)
):
    condition = None
    if search:
        search_lower = f"%{search.lower()}%"
        condition = (
                func.lower(ImtRoster.remark).like(search_lower) |
                func.lower(func.to_char(ImtRoster.date_from, 'YYYY-MM-DD')).like(search_lower) |
                func.lower(func.to_char(ImtRoster.date_to, 'YYYY-MM-DD')).like(search_lower)
            )
    
    return await read_paginated_items(
        ImtRoster,
        page,
        limit,
        session,
        condition
    )