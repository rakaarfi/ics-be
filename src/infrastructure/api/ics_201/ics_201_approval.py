from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_201_models import Ics201Approval
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException


router = APIRouter()

# Dependency to get the repository
def get_repository(session: AsyncSession = Depends(get_session)) -> BaseRepository:
    return BaseRepository(session)


# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Ics 201 Approval",
    description="Create a new Ics 201 Approval",
)
async def create_ics_201_approval(
    item: Ics201Approval, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_item(Ics201Approval, item)


# Endpoint untuk read
@router.get("/read/")
async def read_ics_201_approval(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(Ics201Approval)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_ics_201_approval_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(Ics201Approval, id)
    except NotFoundException as e:
        raise e


# Endpoint untuk update
@router.put("/update/{id}")
async def update_ics_201_approval(
    updated_data: Ics201Approval, id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.update_item(Ics201Approval, id, updated_data)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_ics_201_approval(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(Ics201Approval, id)
    except NotFoundException as e:
        raise e


# Endpoint untuk read paginated
@router.get("/read-paginated/", response_model=PaginationResponse[List[Ics201Approval]])
async def read_ics_201_approval_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    return await repo.read_paginated_items(Ics201Approval, page, limit, condition)


# Endpoint untuk read by ics_201_id
@router.get("/read-by-ics-id/{ics_201_id}", response_model=List[Ics201Approval])
async def read_ics_201_approval_by_ics_201_id(
    ics_201_id: int, repo: BaseRepository = Depends(get_repository)
):
    condition = Ics201Approval.ics_201_id == ics_201_id
    return await repo.read_items_by_condition(Ics201Approval, condition)
