from datetime import date, time
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, func, select

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_201_models import Ics201ResourceSummary
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException


# Define a new model to allow the creation of multiple entries in a single API request
class Ics201ResourceSummaryBase(SQLModel):
    resource: str
    resource_identified: str
    date_ordered: date
    time_ordered: time
    eta: str
    is_arrived: bool
    notes: str
    ics_201_id: Optional[int] = None


class Ics201ResourceSummaryCreate(SQLModel):
    datas: List[Ics201ResourceSummaryBase]


class Ics201ResourceSummaryDelete(BaseModel):
    ids: list[int]


router = APIRouter()

# Dependency to get the repository
def get_repository(session: AsyncSession = Depends(get_session)) -> BaseRepository:
    return BaseRepository(session)


# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Resource Summary",
    description="Create a new Resource Summary",
)
async def create_resource_summary(
    item: Ics201ResourceSummaryCreate, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_items(Ics201ResourceSummary, item.datas)


# Endpoint untuk read
@router.get("/read/")
async def read_resource_summary(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(Ics201ResourceSummary)

# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_resource_summary_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(Ics201ResourceSummary, id)
    except NotFoundException as e:
        raise e
    
    
# Endpoint untuk update
@router.put("/update/{id}")
async def update_resource_summary(
    updated_data: Ics201ResourceSummary, id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.update_item(Ics201ResourceSummary, id, updated_data)
    except NotFoundException as e:
        raise e

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_resource_summary(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(Ics201ResourceSummary, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete multiple
@router.delete("/delete-many/")
async def delete_multiple_resource_summary(
    ids: Ics201ResourceSummaryDelete, repo: BaseRepository = Depends(get_repository)
):
    return await repo.delete_items_by_ids(Ics201ResourceSummary, ids.ids)


# Endpoint untuk read paginated
@router.get(
    "/read-paginated/", response_model=PaginationResponse[List[Ics201ResourceSummary]]
)
async def read_resource_summary_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    if search:
        search_lower = f"%{search.lower()}%"
        condition = (
            func.lower(Ics201ResourceSummary.resource).like(search_lower)
            | func.lower(Ics201ResourceSummary.resource_identified).like(search_lower)
            | func.lower(func.to_char(Ics201ResourceSummary.date_ordered, "YYYY-MM-DD")).like(
                search_lower
            )
            | func.lower(func.to_char(Ics201ResourceSummary.time_ordered, "HH24:MI")).like(
                search_lower
            )
            | func.lower(Ics201ResourceSummary.eta).like(search_lower)
            | func.lower(Ics201ResourceSummary.notes).like(search_lower)
        )

    return await repo.read_paginated_items(Ics201ResourceSummary, page, limit, condition)


# Endpoint untuk read by ics_201_id
@router.get("/read-by-ics-id/{ics_201_id}", response_model=List[Ics201ResourceSummary])
async def read_resource_summary_by_ics_201_id(
    ics_201_id: int, repo: BaseRepository = Depends(get_repository)
):
    condition = Ics201ResourceSummary.ics_201_id == ics_201_id
    return await repo.read_items_by_condition(Ics201ResourceSummary, condition)
