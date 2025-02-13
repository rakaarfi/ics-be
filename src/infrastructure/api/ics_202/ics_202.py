from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func, select

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_202_models import Ics202
from src.core.entities.incident_data_models import IncidentData, OperationalPeriod
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException


router = APIRouter()

# Dependency to get the repository
def get_repository(session: AsyncSession = Depends(get_session)) -> BaseRepository:
    return BaseRepository(session)


# Endpoint to create
@router.post("/create/", summary="Create Ics 202", description="Create a new Ics 202")
async def create_ics_202(item: Ics202, repo: BaseRepository = Depends(get_repository)):
    return await repo.create_item(Ics202, item)


# Endpoint to read all
@router.get("/read/")
async def read_ics_202(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(Ics202)


# Endpoint to read by id
@router.get("/read/{id}")
async def read_ics_202_by_id(id: int, repo: BaseRepository = Depends(get_repository)):
    try:
        return await repo.read_item_by_id(Ics202, id)
    except NotFoundException as e:
        raise e
    
    
# Endpoint to update by id
@router.put("/update/{id}")
async def update_ics_202(
    update_data: Ics202, id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.update_item(Ics202, id, update_data)
    except NotFoundException as e:
        raise e
    
    
# Endpoint to delete by id
@router.delete("/delete/{id}")
async def delete_ics_202(id: int, repo: BaseRepository = Depends(get_repository)):
    try:
        return await repo.delete_item(Ics202, id)
    except NotFoundException as e:
        raise e
    
    
# Endpoint to read all with pagination
@router.get(
    "/read-paginated/",
    response_model=PaginationResponse[List[Ics202]],
)
async def read_ics_202_with_pagination(
    page: int = 1, 
    limit: int = 10,
    search: str = "", 
    repo: BaseRepository = Depends(get_repository)
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
            Ics202.operational_period_id.in_(subquery)
            | func.lower(Ics202.objectives).like(search_lower)
            | func.lower(Ics202.command_emphasis).like(search_lower)
            | func.lower(Ics202.safety_plan_location).like(search_lower)
        )
        
    return await repo.read_paginated_items(Ics202, page, limit, condition)
