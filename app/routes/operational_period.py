from datetime import date, time
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, func, select

from app.config.database import get_session
from app.crud.crud import (delete_item, read_item_by_id,
                           read_items, read_paginated_items, update_item)
from app.models.incident_data_models import IncidentData, OperationalPeriod
from app.models.pagination_models import PaginationResponse


# Define a new model to allow the creation of multiple entries in a single API request
class OperationalPeriodBase(SQLModel):
    incident_id: int
    date_from: date
    time_from: time
    date_to: date
    time_to: time
    remarks: str


class OperationalPeriodCreate(SQLModel):
    periods: List[OperationalPeriodBase]


router = APIRouter()


# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Operational Period",
    description="Create a new Operational Period",
)
async def create_operational_period(
    item: OperationalPeriodCreate, session: AsyncSession = Depends(get_session)
):
    created_data = []
    for period in item.periods:
        new_period = OperationalPeriod(**period.model_dump())
        session.add(new_period)
        created_data.append(new_period)
    await session.commit()
    return created_data


# Endpoint untuk read
@router.get("/read/")
async def read_operational_period(session: AsyncSession = Depends(get_session)):
    return await read_items(OperationalPeriod, session)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_operational_period_by_id(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(OperationalPeriod, id, session)


# Endpoint untuk update
@router.put("/update/{id}")
async def update_operational_period(
    update_data: OperationalPeriod,
    id: int,
    session: AsyncSession = Depends(get_session),
):
    return await update_item(OperationalPeriod, id, update_data, session)


# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_operational_period(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await delete_item(OperationalPeriod, id, session)


# Endpoint untuk pagination
@router.get(
    "/read-paginated/", response_model=PaginationResponse[List[OperationalPeriod]]
)
async def read_operational_period_with_pagination(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    session: AsyncSession = Depends(get_session),
):
    """
    subquery = select(IncidentData.id).where(
            func.lower(IncidentData.name).like(search_lower)
            )
    OperationalPeriod.incident_id.in_(subquery)

    ## Above is equivalent to:

    SELECT operational_period.*
    FROM operational_period
    WHERE operational_period.incident_id IN (
        SELECT incident_data.id
        FROM incident_data
        WHERE LOWER(incident_data.name) LIKE '%nilai_pencarian%'
    )
    """
    condition = None

    if search:
        search_lower = f"%{search.lower()}%"

        # Create a subquery for IncidentData.name
        subquery = select(IncidentData.id).where(
            func.lower(IncidentData.name).like(search_lower)
        )

        condition = (
            OperationalPeriod.incident_id.in_(subquery)
            | func.lower(func.to_char(OperationalPeriod.date_from, "YYYY-MM-DD")).like(
                search_lower
            )
            | func.lower(func.to_char(OperationalPeriod.time_from, "HH24:MI")).like(
                search_lower
            )
            | func.lower(func.to_char(OperationalPeriod.date_to, "YYYY-MM-DD")).like(
                search_lower
            )
            | func.lower(func.to_char(OperationalPeriod.time_to, "HH24:MI")).like(
                search_lower
            )
            | func.lower(OperationalPeriod.remarks).like(search_lower)
        )

    return await read_paginated_items(
        OperationalPeriod, page, limit, session, condition
    )
