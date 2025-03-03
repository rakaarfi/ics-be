from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_215a_models import Ics215APreparationSafetyOfficer
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException


router = APIRouter()

# Dependency to get the repository
def get_repository(session: AsyncSession = Depends(get_session)) -> BaseRepository:
    return BaseRepository(session)


# Endpoint to create
@router.post("/create/", summary="Create Ics 215A Safety Officer", description="Create a new Ics 215A Safety Officer")
async def create_ics_215a_safety_officer(
    item: Ics215APreparationSafetyOfficer, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_item(Ics215APreparationSafetyOfficer, item)


# Endpoint to read all
@router.get("/read/")
async def read_ics_215a_safety_officer(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(Ics215APreparationSafetyOfficer)


# Endpoint to read by id
@router.get("/read/{id}")
async def read_ics_215a_safety_officer_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(Ics215APreparationSafetyOfficer, id)
    except NotFoundException as e:
        raise e
    

# Endpoint to update
@router.put("/update/{id}")
async def update_ics_215a_safety_officer(
    updated_data: Ics215APreparationSafetyOfficer, id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.update_item(Ics215APreparationSafetyOfficer, id, updated_data)
    except NotFoundException as e:
        raise e


# Endpoint to delete
@router.delete("/delete/{id}")
async def delete_ics_215a_safety_officer(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(Ics215APreparationSafetyOfficer, id)
    except NotFoundException as e:
        raise e
    
    
# Endpoint to read all with pagination
@router.get("/read-paginated/", response_model=PaginationResponse[List[Ics215APreparationSafetyOfficer]])
async def read_ics_215a_safety_officer_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    return await repo.read_paginated_items(Ics215APreparationSafetyOfficer, page, limit, condition)


# Endpoint untuk read by ics_215a_id
@router.get("/read-by-ics-215a-id/{ics_215a_id}")
async def read_ics_215a_safety_officer_by_ics_215a_id(
    ics_215a_id: int, repo: BaseRepository = Depends(get_repository)
):
    condition = Ics215APreparationSafetyOfficer.ics_215a_id == ics_215a_id
    return await repo.read_items_by_condition(Ics215APreparationSafetyOfficer, condition)
