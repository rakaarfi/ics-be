from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func, select

from app.config.database import get_session
from app.crud.crud import (create_item, delete_item, read_item_by_id,
                           read_items, read_paginated_items, update_item)
from app.models.ics_201_models import Ics201
from app.models.incident_data_models import IncidentData
from app.models.pagination_models import PaginationResponse

router = APIRouter()


# Endpoint untuk create
@router.post("/create/", summary="Create Ics 201", description="Create a new Ics 201")
async def create_ics_201(item: Ics201, session: AsyncSession = Depends(get_session)):
    return await create_item(Ics201, item, session)


# Endpoint untuk read
@router.get("/read/")
async def read_ics_201(session: AsyncSession = Depends(get_session)):
    return await read_items(Ics201, session)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_ics_201_by_id(id: int, session: AsyncSession = Depends(get_session)):
    return await read_item_by_id(Ics201, id, session)


# Endpoint untuk update
@router.put("/update/{id}")
async def update_ics_201(
    update_data: Ics201, id: int, session: AsyncSession = Depends(get_session)
):
    return await update_item(Ics201, id, update_data, session)


# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_ics_201(id: int, session: AsyncSession = Depends(get_session)):
    return await delete_item(Ics201, id, session)


# Endpoint untuk read paginated
@router.get("/read-paginated/", response_model=PaginationResponse[List[Ics201]])
async def read_ics_201_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    session: AsyncSession = Depends(get_session),
):
    condition = None

    if search:
        search_lower = f"%{search.lower()}%"

        # Create a subquery for IncidentData.name
        subquery = select(IncidentData.id).where(
            func.lower(IncidentData.name).like(search_lower)
        )

        condition = (
            Ics201.incident_id.in_(subquery)
            | func.lower(func.to_char(Ics201.date_initiated, "YYYY-MM-DD")).like(
                search_lower
            )
            | func.lower(func.to_char(Ics201.time_initiated, "HH24:MI")).like(
                search_lower
            )
            | func.lower(Ics201.map_sketch).like(search_lower)
            | func.lower(Ics201.situation_summary).like(search_lower)
            | func.lower(Ics201.objectives).like(search_lower)
        )

    return await read_paginated_items(Ics201, page, limit, session, condition)
