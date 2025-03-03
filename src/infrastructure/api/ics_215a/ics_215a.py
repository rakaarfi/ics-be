from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func, select

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_215a_models import Ics215A
from src.core.entities.incident_data_models import IncidentData, OperationalPeriod
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException


router = APIRouter()

# Dependency to get the repository
def get_repository(session: AsyncSession = Depends(get_session)) -> BaseRepository:
    return BaseRepository(session)


# Endpoint to create
@router.post("/create/", summary="Create Ics 215A", description="Create a new Ics 215A")
async def create_ics_215a(item: Ics215A, repo: BaseRepository = Depends(get_repository)):
    return await repo.create_item(Ics215A, item)


# Endpoint to read all
@router.get("/read/")
async def read_ics_215a(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(Ics215A)


# Endpoint to read by id
@router.get("/read/{id}")
async def read_ics_215a_by_id(id: int, repo: BaseRepository = Depends(get_repository)):
    try:
        return await repo.read_item_by_id(Ics215A, id)
    except NotFoundException as e:
        raise e


# Endpoint to update by id
@router.put("/update/{id}")
async def update_ics_215a(
    update_data: Ics215A, id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.update_item(Ics215A, id, update_data)
    except NotFoundException as e:
        raise e
    

# Endpoint to delete by id
@router.delete("/delete/{id}")
async def delete_ics_215a(id: int, repo: BaseRepository = Depends(get_repository)):
    try:
        return await repo.delete_item(Ics215A, id)
    except NotFoundException as e:
        raise e
    

# Endpoint to read all with pagination
@router.get(
    "/read-paginated/",
    response_model=PaginationResponse[List[Ics215A]],
)
async def read_ics_215a_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    if search:
        search_lower = f"%{search.lower()}%"
        
        # Create a subquery for IncidentData.name
        inner_query = select(IncidentData.id).where(
            func.lower(IncidentData.name).like(search_lower)
        )
        
        # Create the subquery to filter operational_period_id
        subquery = select(OperationalPeriod.id).where(
            OperationalPeriod.incident_id.in_(inner_query)
        )
        
        condition = (
            Ics215A.operational_period_id.in_(subquery)
        )
    
    return await repo.read_paginated_items(Ics215A, page, limit, condition)