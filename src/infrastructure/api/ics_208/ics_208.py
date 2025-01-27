from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func, select

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_208_models import Ics208
from src.core.entities.incident_data_models import IncidentData, OperationalPeriod
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException


router = APIRouter()

# Dependency to get the repository
def get_repository(session: AsyncSession = Depends(get_session)) -> BaseRepository:
    return BaseRepository(session)

# Endpoint to create
@router.post("/create/", summary="Create Ics 208", description="Create a new Ics 208")
async def create_ics_208(item: Ics208, repo: BaseRepository = Depends(get_repository)):
    return await repo.create_item(Ics208, item)


# Endpoint to read all
@router.get("/read/")
async def read_ics_208(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(Ics208)


# Endpoint to read by id
@router.get("/read/{id}")
async def read_ics_208_by_id(id: int, repo: BaseRepository = Depends(get_repository)):
    try:
        return await repo.read_item_by_id(Ics208, id)
    except NotFoundException as e:
        raise e
    
    
# Endpoint to update by id
@router.put("/update/{id}")
async def update_ics_208(
    update_data: Ics208, id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.update_item(Ics208, id, update_data)
    except NotFoundException as e:
        raise e
    
    
# Endpoint to delete by id
@router.delete("/delete/{id}")
async def delete_ics_208(id: int, repo: BaseRepository = Depends(get_repository)):
    try:
        return await repo.delete_item(Ics208, id)
    except NotFoundException as e:
        raise e
    
    
# Endpoint to read all with pagination
@router.get(
    "/read-paginated/",
    response_model=PaginationResponse[List[Ics208]],
)
async def read_ics_208_with_pagination(
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
            Ics208.operational_period_id.in_(subquery)
        )
        
    return await repo.read_paginated_items(Ics208, page, limit, condition)
