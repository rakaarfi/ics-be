from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_205_models import Ics205Preparation
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException


router = APIRouter()

# Dependency to get the repository
def get_repository(session: AsyncSession = Depends(get_session)) -> BaseRepository:
    return BaseRepository(session)


# Endpoint to create
@router.post("/create/", summary="Create Ics 205 Preparation", description="Create a new Ics 205 Preparation")
async def create_ics_205_preparation(
    item: Ics205Preparation, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_item(Ics205Preparation, item)


# Endpoint to read all
@router.get("/read/")
async def read_ics_205_preparation(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(Ics205Preparation)


# Endpoint to read by id
@router.get("/read/{id}")
async def read_ics_205_preparation_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(Ics205Preparation, id)
    except NotFoundException as e:
        raise e
    

# Endpoint to update
@router.put("/update/{id}")
async def update_ics_205_preparation(
    updated_data: Ics205Preparation, id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.update_item(Ics205Preparation, id, updated_data)
    except NotFoundException as e:
        raise e


# Endpoint to delete
@router.delete("/delete/{id}")
async def delete_ics_205_preparation(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(Ics205Preparation, id)
    except NotFoundException as e:
        raise e
    
    
# Endpoint to read all with pagination
@router.get("/read-paginated/", response_model=PaginationResponse[List[Ics205Preparation]])
async def read_ics_205_preparation_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    return await repo.read_paginated_items(Ics205Preparation, page, limit, condition)


# Endpoint untuk read by ics_205_id
@router.get("/read-by-ics-205-id/{ics_205_id}")
async def read_ics_205_preparation_by_ics_205_id(
    ics_205_id: int, repo: BaseRepository = Depends(get_repository)
):
    condition = Ics205Preparation.ics_205_id == ics_205_id
    return await repo.read_items_by_condition(Ics205Preparation, condition)
