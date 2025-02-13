from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.imt_members_models.main_section_models import PublicInformationOfficer
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
    summary="Create Public Information Officer",
    description="Create a new Public Information Officer",
)
async def create_public_information_officer(
    item: PublicInformationOfficer, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_item(PublicInformationOfficer, item)

# Endpoint untuk read
@router.get("/read/")
async def read_public_information_officer(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(PublicInformationOfficer)

# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_public_information_officer_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(PublicInformationOfficer, id)
    except NotFoundException as e:
        raise e

# Endpoint untuk update
@router.put("/update/{id}")
async def update_public_information_officer(
    update_data: PublicInformationOfficer,
    id: int,
    repo: BaseRepository = Depends(get_repository),
):
    try:
        return await repo.update_item(PublicInformationOfficer, id, update_data)
    except NotFoundException as e:
        raise e

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_public_information_officer(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(PublicInformationOfficer, id)
    except NotFoundException as e:
        raise e

# Endpoint untuk read paginated
@router.get(
    "/read-paginated/",
    response_model=PaginationResponse[List[PublicInformationOfficer]],
)
async def read_public_information_officer_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    if search:
        condition = imt_members_search_condition(search, PublicInformationOfficer)

    return await repo.read_paginated_items(
        PublicInformationOfficer, page, limit, condition
    )
