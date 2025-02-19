from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_204_models import Ics204PreparationOSChief
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException


router = APIRouter()

# Dependency to get the repository
def get_repository(session: AsyncSession = Depends(get_session)) -> BaseRepository:
    return BaseRepository(session)


# Endpoint to create
@router.post("/create/", summary="Create Ics 204 Preparation OS Chief", description="Create a new Ics 204 Preparation OS Chief")
async def create_ics_204_preparation_os_chief(
    item: Ics204PreparationOSChief, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_item(Ics204PreparationOSChief, item)


# Endpoint to read all
@router.get("/read/")
async def read_ics_204_preparation_os_chief(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(Ics204PreparationOSChief)


# Endpoint to read by id
@router.get("/read/{id}")
async def read_ics_204_preparation_os_chief_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(Ics204PreparationOSChief, id)
    except NotFoundException as e:
        raise e
    

# Endpoint to update
@router.put("/update/{id}")
async def update_ics_204_preparation_os_chief(
    updated_data: Ics204PreparationOSChief, id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.update_item(Ics204PreparationOSChief, id, updated_data)
    except NotFoundException as e:
        raise e


# Endpoint to delete
@router.delete("/delete/{id}")
async def delete_ics_204_preparation_os_chief(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(Ics204PreparationOSChief, id)
    except NotFoundException as e:
        raise e
    
    
# Endpoint to read all with pagination
@router.get("/read-paginated/", response_model=PaginationResponse[List[Ics204PreparationOSChief]])
async def read_ics_204_preparation_os_chief_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    return await repo.read_paginated_items(Ics204PreparationOSChief, page, limit, condition)


# Endpoint untuk read by ics_204_id
@router.get("/read-by-ics-204-id/{ics_204_id}")
async def read_ics_204_preparation_os_chief_by_ics_204_id(
    ics_204_id: int, repo: BaseRepository = Depends(get_repository)
):
    condition = Ics204PreparationOSChief.ics_204_id == ics_204_id
    return await repo.read_items_by_condition(Ics204PreparationOSChief, condition)
