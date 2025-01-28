from typing import List, Optional

from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, func

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_206_models import Ics206Transportation
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException


# Define a new model to allow the creation of multiple entries in a single API request
class Ics206TransportationBase(SQLModel):
    ics_206_id: Optional[int] = None
    ambulance_sercvice: str
    location: str
    number: str
    is_als: Optional[bool]
    is_bls: Optional[bool]
    

class Ics206TransportationCreate(SQLModel):
    datas: List[Ics206TransportationBase]
    

class Ics206TransportationDelete(BaseModel):
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
    item: Ics206TransportationCreate, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_items(Ics206Transportation, item.datas)


# Endpoint untuk read
@router.get("/read/")
async def read_transportation(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(Ics206Transportation)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_transportation_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(Ics206Transportation, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk update
@router.put("/update/{id}")
async def update_transportation(
    updated_data: Ics206Transportation,
    id: int,
    repo: BaseRepository = Depends(get_repository),
):
    try:
        return await repo.update_item(Ics206Transportation, id, updated_data)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_transportation(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(Ics206Transportation, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete multiple
@router.delete("/delete-many/")
async def delete_multiple_transportation(
    ids: Ics206TransportationDelete, repo: BaseRepository = Depends(get_repository),
):
    return await repo.delete_items_by_ids(Ics206Transportation, ids.ids)


# Endpoint untuk read paginated
@router.get(
    "/read-paginated/", response_model=PaginationResponse[Ics206Transportation]
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
        condition = func.lower(Ics206Transportation.ambulance_sercvice).like(
            search_lower
        ) | func.lower(Ics206Transportation.location).like(
            search_lower
        ) | func.lower(Ics206Transportation.number).like(
            search_lower
        )
        
    return await repo.read_paginated_items(
        Ics206Transportation, page, limit, condition
    )


# Endpoint untuk read by ics_206_id
@router.get(
    "/read-by-ics-id/{ics_206_id}", response_model=List[Ics206Transportation]
)
async def read_transportation_by_ics_id(
    ics_206_id: int, repo: BaseRepository = Depends(get_repository),
):
    condition = Ics206Transportation.ics_206_id == ics_206_id
    return await repo.read_items_by_condition(Ics206Transportation, condition)
