from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_206_models import Ics206Approval
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException


router = APIRouter()

# Dependency to get the repository
def get_repository(session: AsyncSession = Depends(get_session)) -> BaseRepository:
    return BaseRepository(session)


# Endpoint to create
@router.post("/create/", summary="Create Ics 206 Approval", description="Create a new Ics 206 Approval")
async def create_ics_206_approval(
    item: Ics206Approval, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_item(Ics206Approval, item)


# Endpoint to read all
@router.get("/read/")
async def read_ics_206_approval(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(Ics206Approval)


# Endpoint to read by id
@router.get("/read/{id}")
async def read_ics_206_approval_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(Ics206Approval, id)
    except NotFoundException as e:
        raise e
    

# Endpoint to update
@router.put("/update/{id}")
async def update_ics_206_approval(
    updated_data: Ics206Approval, id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.update_item(Ics206Approval, id, updated_data)
    except NotFoundException as e:
        raise e


# Endpoint to delete
@router.delete("/delete/{id}")
async def delete_ics_206_approval(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(Ics206Approval, id)
    except NotFoundException as e:
        raise e
    
    
# Endpoint to read all with pagination
@router.get("/read-paginated/", response_model=PaginationResponse[List[Ics206Approval]])
async def read_ics_206_approval_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    return await repo.read_paginated_items(Ics206Approval, page, limit, condition)


# Endpoint untuk read by ics_206_id
@router.get("/read-by-ics-206-id/{ics_206_id}")
async def read_ics_206_approval_by_ics_206_id(
    ics_206_id: int, repo: BaseRepository = Depends(get_repository)
):
    condition = Ics206Approval.ics_206_id == ics_206_id
    return await repo.read_items_by_condition(Ics206Approval, condition)
