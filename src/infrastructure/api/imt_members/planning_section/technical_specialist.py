from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.imt_members_models.planning_section_models import TechnicalSpecialist
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException
from src.infrastructure.utils.utils import imt_members_search_condition

router = APIRouter()

# Dependency untuk mendapatkan repository
def get_repository(session: AsyncSession = Depends(get_session)):
    return BaseRepository(session)


# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Technical Specialist",
    description="Create a new Technical Specialist",
)
async def create_technical_specialist(
    item: TechnicalSpecialist, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_item(TechnicalSpecialist, item)


# Endpoint untuk read
@router.get("/read/")
async def read_technical_specialist(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(TechnicalSpecialist)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_technical_specialist_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(TechnicalSpecialist, id)
    except NotFoundException as e:
        raise e

# Endpoint untuk update
@router.put("/update/{id}")
async def update_technical_specialist(
    update_data: TechnicalSpecialist,
    id: int,
    repo: BaseRepository = Depends(get_repository),
):
    try:
        return await repo.update_item(TechnicalSpecialist, id, update_data)
    except NotFoundException as e:
        raise e

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_technical_specialist(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(TechnicalSpecialist, id)
    except NotFoundException as e:
        raise e

# Endpoint untuk read paginated
@router.get(
    "/read-paginated/", response_model=PaginationResponse[List[TechnicalSpecialist]]
)
async def read_technical_specialist_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    if search:
        condition = imt_members_search_condition(search, TechnicalSpecialist)

    return await repo.read_paginated_items(
        TechnicalSpecialist, page, limit, condition
    )
