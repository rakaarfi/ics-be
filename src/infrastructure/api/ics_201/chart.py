from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_201_models import IcsChart
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException

router = APIRouter()

# Dependency to get the repository
def get_repository(session: AsyncSession = Depends(get_session)) -> BaseRepository:
    return BaseRepository(session)


# Endpoint untuk create
@router.post(
    "/create/", summary="Create Ics Chart", description="Create a new Ics Chart"
)
async def create_ics_chart(
    item: IcsChart, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_item(IcsChart, item)


# Endpoint untuk read
@router.get("/read/")
async def read_ics_chart(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(IcsChart)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_ics_chart_by_id(id: int, repo: BaseRepository = Depends(get_repository)):
    try:
        return await repo.read_item_by_id(IcsChart, id)
    except NotFoundException as e:
        raise e


# Endpoint untuk update
@router.put("/update/{id}")
async def update_ics_chart(
    update_data: IcsChart, id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.update_item(IcsChart, id, update_data)
    except NotFoundException as e:
        raise e


# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_ics_chart(id: int, repo: BaseRepository = Depends(get_repository)):
    try:
        return await repo.delete_item(IcsChart, id)
    except NotFoundException as e:
        raise e


# Endpoint untuk read paginated
@router.get("/read-paginated/", response_model=PaginationResponse[List[IcsChart]])
async def read_ics_chart_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    return await repo.read_paginated_items(IcsChart, page, limit, condition)


# Endpoint untuk read by ics_201_id
@router.get("/read-by-ics-id/{ics_201_id}", response_model=List[IcsChart])
async def read_ics_chart_by_ics_id(
    ics_201_id: int, repo: BaseRepository = Depends(get_repository)
):
    condition = IcsChart.ics_201_id == ics_201_id
    return await repo.read_items_by_condition(IcsChart, condition)
