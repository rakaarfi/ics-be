from datetime import date, time
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, func, select

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.incident_data_models import OperationalPeriod, IncidentData
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException


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

# Dependency to get the repository
def get_repository(session: AsyncSession = Depends(get_session)) -> BaseRepository:
    return BaseRepository(session)


# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Operational Period",
    description="Create a new Operational Period",
)
async def create_operational_period(
    item: OperationalPeriodCreate, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_items(OperationalPeriod, item.periods)


# Endpoint untuk read
@router.get("/read/")
async def read_operational_period(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(OperationalPeriod)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_operational_period_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(OperationalPeriod, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk update
@router.put("/update/{id}")
async def update_operational_period(
    update_data: OperationalPeriod,
    id: int,
    repo: BaseRepository = Depends(get_repository),
):
    try:
        return await repo.update_item(OperationalPeriod, id, update_data)
    except NotFoundException as e:
        raise e


# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_operational_period(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(OperationalPeriod, id)
    except NotFoundException as e:
        raise e

# Endpoint untuk pagination
@router.get(
    "/read-paginated/", response_model=PaginationResponse[List[OperationalPeriod]]
)
async def read_operational_period_with_pagination(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
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

    return await repo.read_paginated_items(OperationalPeriod, page, limit, condition)
