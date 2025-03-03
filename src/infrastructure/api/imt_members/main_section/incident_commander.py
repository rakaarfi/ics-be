from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.imt_members_models.main_section_models import IncidentCommander
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
    summary="Create Incident Commander",
    description="Create a new Incident Commander",
)
async def create_incident_commander(
    item: IncidentCommander, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_item(IncidentCommander, item)


# Endpoint untuk read
@router.get("/read/")
async def read_incident_commander(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(IncidentCommander)

# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_incident_commander_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(IncidentCommander, id)
    except NotFoundException as e:
        raise e

# Endpoint untuk update
@router.put("/update/{id}")
async def update_incident_commander(
    update_data: IncidentCommander,
    id: int,
    repo: BaseRepository = Depends(get_repository),
):
    try:
        return await repo.update_item(IncidentCommander, id, update_data)
    except NotFoundException as e:
        raise e

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_incident_commander(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(IncidentCommander, id)
    except NotFoundException as e:
        raise e

# Endpoint untuk pagination
@router.get(
    "/read-paginated/", response_model=PaginationResponse[List[IncidentCommander]]
)
async def read_incident_commander_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    if search:
        condition = imt_members_search_condition(search, IncidentCommander)

    return await repo.read_paginated_items(
        IncidentCommander, page, limit, condition
    )
