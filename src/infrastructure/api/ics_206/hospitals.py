from typing import List, Optional

from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, func

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_206_models import Hospitals
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException


# Define a new model to allow the creation of multiple entries in a single API request
class HospitalsBase(SQLModel):
    ics_206_id: Optional[int] = None
    name: str
    location: str
    number: str
    is_paramedic: Optional[bool]
    

class HospitalsCreate(SQLModel):
    datas: List[HospitalsBase]
    

class HospitalsDelete(BaseModel):
    ids: list[int]
    
    
router = APIRouter()

    
# Dependency to get the repository
def get_repository(session: AsyncSession = Depends(get_session)) -> BaseRepository:
    return BaseRepository(session)


# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Hospitals",
    description="Create a new Hospitals",
)
async def create_hospitals(
    item: HospitalsCreate, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_items(Hospitals, item.datas)


# Endpoint untuk read
@router.get("/read/")
async def read_hospitals(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(Hospitals)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_hospitals_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(Hospitals, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk update
@router.put("/update/{id}")
async def update_hospitals(
    updated_data: Hospitals,
    id: int,
    repo: BaseRepository = Depends(get_repository),
):
    try:
        return await repo.update_item(Hospitals, id, updated_data)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_hospitals(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(Hospitals, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete multiple
@router.delete("/delete-many/")
async def delete_multiple_hospitals(
    ids: HospitalsDelete, repo: BaseRepository = Depends(get_repository),
):
    return await repo.delete_items_by_ids(Hospitals, ids.ids)


# Endpoint untuk read paginated
@router.get(
    "/read-paginated/", response_model=PaginationResponse[Hospitals]
)
async def read_hospitals_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    if search:
        search_lower = f"%{search.lower()}%"
        condition = func.lower(Hospitals.name).like(
            search_lower
        ) | func.lower(Hospitals.address).like(
            search_lower
        ) | func.lower(Hospitals.number).like(
            search_lower
        ) | func.lower(Hospitals.air_travel_time).like(
            search_lower
        ) | func.lower(Hospitals.ground_travel_time).like(
            search_lower
        ) | func.lower(Hospitals.level_trauma_center).like(
            search_lower
        )
        
    return await repo.read_paginated_items(
        Hospitals, page, limit, condition
    )


# Endpoint untuk read by ics_206_id
@router.get(
    "/read-by-ics-id/{ics_206_id}", response_model=List[Hospitals]
)
async def read_hospitals_by_ics_id(
    ics_206_id: int, repo: BaseRepository = Depends(get_repository),
):
    condition = Hospitals.ics_206_id == ics_206_id
    return await repo.read_items_by_condition(Hospitals, condition)
