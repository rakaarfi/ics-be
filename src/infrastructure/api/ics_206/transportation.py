from typing import List, Optional

from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, func

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_206_models import Transportation
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException


# Define a new model to allow the creation of multiple entries in a single API request
class TransportationBase(SQLModel):
    ics_206_id: Optional[int] = None
    ambulance_sercvice: str
    location: str
    number: str
    is_als: Optional[bool]
    is_bls: Optional[bool]
    

class TransportationCreate(SQLModel):
    datas: List[TransportationBase]
    

class TransportationDelete(BaseModel):
    ids: list[int]
    
    
router = APIRouter()

    
# Dependency to get the repository
def get_repository(session: AsyncSession = Depends(get_session)) -> BaseRepository:
    return BaseRepository(session)


# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Transportation",
    description="Create a new Transportation",
)
async def create_transportation(
    item: TransportationCreate, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_items(Transportation, item.datas)


# Endpoint untuk read
@router.get("/read/")
async def read_transportation(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(Transportation)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_transportation_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(Transportation, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk update
@router.put("/update/{id}")
async def update_transportation(
    updated_data: Transportation,
    id: int,
    repo: BaseRepository = Depends(get_repository),
):
    try:
        return await repo.update_item(Transportation, id, updated_data)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_transportation(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(Transportation, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete multiple
@router.delete("/delete-many/")
async def delete_multiple_transportation(
    ids: TransportationDelete, repo: BaseRepository = Depends(get_repository),
):
    return await repo.delete_items_by_ids(Transportation, ids.ids)


# Endpoint untuk read paginated
@router.get(
    "/read-paginated/", response_model=PaginationResponse[Transportation]
)
async def read_transportation_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    if search:
        search_lower = f"%{search.lower()}%"
        condition = func.lower(Transportation.ambulance_sercvice).like(
            search_lower
        ) | func.lower(Transportation.location).like(
            search_lower
        ) | func.lower(Transportation.number).like(
            search_lower
        )
        
    return await repo.read_paginated_items(
        Transportation, page, limit, condition
    )


# Endpoint untuk read by ics_206_id
@router.get(
    "/read-by-ics-id/{ics_206_id}", response_model=List[Transportation]
)
async def read_transportation_by_ics_id(
    ics_206_id: int, repo: BaseRepository = Depends(get_repository),
):
    condition = Transportation.ics_206_id == ics_206_id
    return await repo.read_items_by_condition(Transportation, condition)
