from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.imt_members_models.planning_section_models import DemobilizationUnitLeader
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
    summary="Create Demobilization Unit Leader",
    description="Create a new Demobilization Unit Leader",
)
async def create_demobilization_unit_leader(
    item: DemobilizationUnitLeader, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_item(DemobilizationUnitLeader, item)


# Endpoint untuk read
@router.get("/read/")
async def read_demobilization_unit_leader(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(DemobilizationUnitLeader)

# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_demobilization_unit_leader_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    return await repo.read_item_by_id(DemobilizationUnitLeader, id)


# Endpoint untuk update
@router.put("/update/{id}")
async def update_demobilization_unit_leader(
    update_data: DemobilizationUnitLeader,
    id: int,
    repo: BaseRepository = Depends(get_repository),
):
    try:
        return await repo.update_item(DemobilizationUnitLeader, id, update_data)
    except NotFoundException as e:
        raise e
    
    
# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_demobilization_unit_leader(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(DemobilizationUnitLeader, id)
    except NotFoundException as e:
        raise e
    
    
# Endpoint untuk read paginated
@router.get(
    "/read-paginated/",
    response_model=PaginationResponse[List[DemobilizationUnitLeader]],
)
async def read_demobilization_unit_leader_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    if search:
        condition = imt_members_search_condition(search, DemobilizationUnitLeader)

    return await repo.read_paginated_items(
        DemobilizationUnitLeader, page, limit, condition
    )
