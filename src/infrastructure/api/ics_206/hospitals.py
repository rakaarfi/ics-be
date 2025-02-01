from typing import List, Optional

from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, func

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_206_models import Ics206Hospitals
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException


# Define a new model to allow the creation of multiple entries in a single API request
class Ics206HospitalsBase(SQLModel):
    ics_206_id: Optional[int] = None
    name: str
    address: str
    number: str
    air_travel_time: Optional[str]
    ground_travel_time: Optional[str]
    is_trauma_center: Optional[bool]
    level_trauma_center: Optional[str]
    is_burn_center: Optional[bool]
    is_helipad: Optional[bool]
    

class Ics206HospitalsCreate(SQLModel):
    datas: List[Ics206HospitalsBase]
    

class Ics206HospitalsDelete(BaseModel):
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
    item: Ics206HospitalsCreate, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_items(Ics206Hospitals, item.datas)


# Endpoint untuk read
@router.get("/read/")
async def read_hospitals(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(Ics206Hospitals)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_hospitals_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(Ics206Hospitals, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk update
@router.put("/update/{id}")
async def update_hospitals(
    updated_data: Ics206Hospitals,
    id: int,
    repo: BaseRepository = Depends(get_repository),
):
    try:
        return await repo.update_item(Ics206Hospitals, id, updated_data)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_hospitals(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(Ics206Hospitals, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete multiple
@router.delete("/delete-many/")
async def delete_multiple_hospitals(
    ids: Ics206HospitalsDelete, repo: BaseRepository = Depends(get_repository),
):
    return await repo.delete_items_by_ids(Ics206Hospitals, ids.ids)


# Endpoint untuk read paginated
@router.get(
    "/read-paginated/", response_model=PaginationResponse[Ics206Hospitals]
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
        condition = func.lower(Ics206Hospitals.name).like(
            search_lower
        ) | func.lower(Ics206Hospitals.address).like(
            search_lower
        ) | func.lower(Ics206Hospitals.number).like(
            search_lower
        ) | func.lower(Ics206Hospitals.air_travel_time).like(
            search_lower
        ) | func.lower(Ics206Hospitals.ground_travel_time).like(
            search_lower
        ) | func.lower(Ics206Hospitals.level_trauma_center).like(
            search_lower
        )
        
    return await repo.read_paginated_items(
        Ics206Hospitals, page, limit, condition
    )


# Endpoint untuk read by ics_206_id
@router.get(
    "/read-by-ics-id/{ics_206_id}", response_model=List[Ics206Hospitals]
)
async def read_hospitals_by_ics_id(
    ics_206_id: int, repo: BaseRepository = Depends(get_repository),
):
    condition = Ics206Hospitals.ics_206_id == ics_206_id
    return await repo.read_items_by_condition(Ics206Hospitals, condition)
