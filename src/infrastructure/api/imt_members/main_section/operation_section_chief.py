from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.imt_members_models.main_section_models import OperationSectionChief
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
    summary="Create Operation Section Chief",
    description="Create a new Operation Section Chief",
)
async def create_operation_section_chief(
    item: OperationSectionChief, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_item(OperationSectionChief, item)

# Endpoint untuk read
@router.get("/read/")
async def read_operation_section_chief(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(OperationSectionChief)

# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_operation_section_chief_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(OperationSectionChief, id)
    except NotFoundException as e:
        raise e

# Endpoint untuk update
@router.put("/update/{id}")
async def update_operation_section_chief(
    update_data: OperationSectionChief,
    id: int,
    repo: BaseRepository = Depends(get_repository),
):
    try:
        return await repo.update_item(OperationSectionChief, id, update_data)
    except NotFoundException as e:
        raise e

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_operation_section_chief(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(OperationSectionChief, id)
    except NotFoundException as e:
        raise e

# Endpoint untuk read paginated
@router.get(
    "/read-paginated/", response_model=PaginationResponse[List[OperationSectionChief]]
)
async def read_operation_section_chief_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    if search:
        condition = imt_members_search_condition(search, OperationSectionChief)

    return await repo.read_paginated_items(
        OperationSectionChief, page, limit, condition
    )
