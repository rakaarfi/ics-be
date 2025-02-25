from typing import List, Optional

from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, func

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_206_models import Ics206MedicalAidStation
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException


# Define a new model to allow the creation of multiple entries in a single API request
class Ics206MedicalAidStationBase(SQLModel):
    ics_206_id: Optional[int] = None
    name: str
    location: str
    number: str
    is_paramedic: Optional[bool]
    

class Ics206MedicalAidStationCreate(SQLModel):
    datas: List[Ics206MedicalAidStationBase]
    

class Ics206MedicalAidStationDelete(BaseModel):
    ids: list[int]
    
    
router = APIRouter()

    
# Dependency to get the repository
def get_repository(session: AsyncSession = Depends(get_session)) -> BaseRepository:
    return BaseRepository(session)


# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Medical Aid Station",
    description="Create a new Medical Aid Station",
)
async def create_medical_aid_station(
    item: Ics206MedicalAidStationCreate, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_items(Ics206MedicalAidStation, item.datas)


# Endpoint untuk read
@router.get("/read/")
async def read_medical_aid_station(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(Ics206MedicalAidStation)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_medical_aid_station_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(Ics206MedicalAidStation, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk update
@router.put("/update/{id}")
async def update_medical_aid_station(
    updated_data: Ics206MedicalAidStation,
    id: int,
    repo: BaseRepository = Depends(get_repository),
):
    try:
        return await repo.update_item(Ics206MedicalAidStation, id, updated_data)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_medical_aid_station(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(Ics206MedicalAidStation, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete multiple
@router.delete("/delete-many/")
async def delete_multiple_medical_aid_station(
    ids: Ics206MedicalAidStationDelete, repo: BaseRepository = Depends(get_repository),
):
    return await repo.delete_items_by_ids(Ics206MedicalAidStation, ids.ids)


# Endpoint untuk read paginated
@router.get(
    "/read-paginated/", response_model=PaginationResponse[Ics206MedicalAidStation]
)
async def read_medical_aid_station_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    if search:
        search_lower = f"%{search.lower()}%"
        condition = func.lower(Ics206MedicalAidStation.name).like(
            search_lower
        ) | func.lower(Ics206MedicalAidStation.location).like(
            search_lower
        ) | func.lower(Ics206MedicalAidStation.number).like(
            search_lower
        )
        
    return await repo.read_paginated_items(
        Ics206MedicalAidStation, page, limit, condition
    )


# Endpoint untuk read by ics_206_id
@router.get(
    "/read-by-ics-id/{ics_206_id}", response_model=List[Ics206MedicalAidStation]
)
async def read_medical_aid_station_by_ics_id(
    ics_206_id: int, repo: BaseRepository = Depends(get_repository),
):
    condition = Ics206MedicalAidStation.ics_206_id == ics_206_id
    return await repo.read_items_by_condition(Ics206MedicalAidStation, condition)
