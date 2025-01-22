from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from sqlmodel import func, select
from typing import List

from app.models.ics_201 import IcsChart
from app.config.database import get_session
from app.models.models import PaginationResponse
from app.crud.crud import (
    create_item, read_items, read_item_by_id,
    update_item, delete_item, read_paginated_items
)


router = APIRouter()

# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Ics Chart",
    description="Create a new Ics Chart"
)
async def create_ics_chart(
    item: IcsChart,
    session: AsyncSession = Depends(get_session)
):
    return await create_item(IcsChart, item, session)


# Endpoint untuk read
@router.get("/read/")
async def read_ics_chart(session: AsyncSession = Depends(get_session)):
    return await read_items(IcsChart, session)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_ics_chart_by_id(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(IcsChart, id, session)


# Endpoint untuk update
@router.put("/update/{id}")
async def update_ics_chart(
    update_data: IcsChart,
    id: int,
    session: AsyncSession = Depends(get_session)
):
    return await update_item(IcsChart, id, update_data, session)


# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_ics_chart(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    return await delete_item(IcsChart, id, session)


# Endpoint untuk read paginated
@router.get(
    "/read-paginated/",
    response_model=PaginationResponse[List[IcsChart]]
)
async def read_ics_chart_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    session: AsyncSession = Depends(get_session)
):
    condition = None
    
    return await read_paginated_items(
        IcsChart,
        page,
        limit,
        session,
        condition
    )
    

# Endpoint untuk read by ics_201_id
@router.get(
    "/read-by-ics-id/{ics_201_id}",
    response_model=List[IcsChart])
async def read_ics_chart_by_ics_id(
    ics_201_id: int,
    session: AsyncSession = Depends(get_session)
):
    # Query the database for records with the specified ics_201_id
    statement = select(IcsChart).where(IcsChart.ics_201_id == ics_201_id)
    results = await session.execute(statement)
    ics_chart = results.scalars().all()
    
    # Return the list of records
    return ics_chart