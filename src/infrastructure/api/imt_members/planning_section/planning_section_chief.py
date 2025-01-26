from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.imt_members_models.planning_section_models import PlanningSectionChief
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
    summary="Create Planning Section Chief",
    description="Create a new Planning Section Chief",
)
async def create_planning_section_chief(
    item: PlanningSectionChief, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_item(PlanningSectionChief, item)

# Endpoint untuk read
@router.get("/read/")
async def read_planning_section_chief(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(PlanningSectionChief)

# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_planning_section_chief_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(PlanningSectionChief, id)
    except NotFoundException as e:
        raise e

# Endpoint untuk update
@router.put("/update/{id}")
async def update_planning_section_chief(
    update_data: PlanningSectionChief,
    id: int,
    repo: BaseRepository = Depends(get_repository),
):
    try:
        return await repo.update_item(PlanningSectionChief, id, update_data)
    except NotFoundException as e:
        raise e

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_planning_section_chief(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(PlanningSectionChief, id)
    except NotFoundException as e:
        raise e

# Endpoint untuk read paginated
@router.get(
    "/read-paginated/", response_model=PaginationResponse[List[PlanningSectionChief]]
)
async def read_planning_section_chief_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    if search:
        condition = imt_members_search_condition(search, PlanningSectionChief)

    return await repo.read_paginated_items(
        PlanningSectionChief, page, limit, condition
    )
