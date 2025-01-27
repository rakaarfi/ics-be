from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_206_models import Ics206Preparation
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException


router = APIRouter()

# Dependency to get the repository
def get_repository(session: AsyncSession = Depends(get_session)) -> BaseRepository:
    return BaseRepository(session)


# Endpoint to create
@router.post("/create/", summary="Create Ics 206 Preparation", description="Create a new Ics 206 Preparation")
async def create_ics_206_preparation(
    item: Ics206Preparation, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_item(Ics206Preparation, item)


# Endpoint to read all
@router.get("/read/")
async def read_ics_206_preparation(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(Ics206Preparation)


# Endpoint to read by id
@router.get("/read/{id}")
async def read_ics_206_preparation_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(Ics206Preparation, id)
    except NotFoundException as e:
        raise e
    

# Endpoint to update
@router.put("/update/{id}")
async def update_ics_206_preparation(
    updated_data: Ics206Preparation, id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.update_item(Ics206Preparation, id, updated_data)
    except NotFoundException as e:
        raise e


# Endpoint to delete
@router.delete("/delete/{id}")
async def delete_ics_206_preparation(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(Ics206Preparation, id)
    except NotFoundException as e:
        raise e
    
    
# Endpoint to read all with pagination
@router.get("/read-paginated/", response_model=PaginationResponse[List[Ics206Preparation]])
async def read_ics_206_preparation_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    return await repo.read_paginated_items(Ics206Preparation, page, limit, condition)


# Endpoint untuk read by ics_206_id
@router.get("/read-by-ics-206-id/{ics_206_id}")
async def read_ics_206_preparation_by_ics_206_id(
    ics_206_id: int, repo: BaseRepository = Depends(get_repository)
):
    condition = Ics206Preparation.ics_206_id == ics_206_id
    return await repo.read_items_by_condition(Ics206Preparation, condition)
