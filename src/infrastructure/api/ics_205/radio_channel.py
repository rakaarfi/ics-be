from typing import List, Optional

from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, func

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_205_models import Ics205RadioChannel
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException


# Define a new model to allow the creation of multiple entries in a single API request
class Ics205RadioChannelBase(SQLModel):
    ics_205_id: Optional[int] = None
    channel_number: str
    channel_name: str
    frequency: str
    mode: str
    functions: str
    assignment: str
    remarks: str
    

class Ics205RadioChannelCreate(SQLModel):
    datas: List[Ics205RadioChannelBase]
    

class Ics205RadioChannelDelete(BaseModel):
    ids: list[int]
    
    
router = APIRouter()

    
# Dependency to get the repository
def get_repository(session: AsyncSession = Depends(get_session)) -> BaseRepository:
    return BaseRepository(session)


# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Radio Channel",
    description="Create a new Radio Channel",
)
async def create_radio_channel(
    item: Ics205RadioChannelCreate, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_items(Ics205RadioChannel, item.datas)


# Endpoint untuk read
@router.get("/read/")
async def read_radio_channel(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(Ics205RadioChannel)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_radio_channel_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(Ics205RadioChannel, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk update
@router.put("/update/{id}")
async def update_radio_channel(
    updated_data: Ics205RadioChannel,
    id: int,
    repo: BaseRepository = Depends(get_repository),
):
    try:
        return await repo.update_item(Ics205RadioChannel, id, updated_data)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_radio_channel(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(Ics205RadioChannel, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete multiple
@router.delete("/delete-many/")
async def delete_multiple_radio_channel(
    ids: Ics205RadioChannelDelete, repo: BaseRepository = Depends(get_repository),
):
    return await repo.delete_items_by_ids(Ics205RadioChannel, ids.ids)


# Endpoint untuk read paginated
@router.get(
    "/read-paginated/", response_model=PaginationResponse[Ics205RadioChannel]
)
async def read_radio_channel_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    if search:
        search_lower = f"%{search.lower()}%"
        condition = func.lower(Ics205RadioChannel.kind).like(
            search_lower
        ) | func.lower(Ics205RadioChannel.channel_number).like(
            search_lower
        ) | func.lower(Ics205RadioChannel.channel_name).like(
            search_lower
        ) | func.lower(Ics205RadioChannel.frequency).like(
            search_lower
        ) | func.lower(Ics205RadioChannel.mode).like(
            search_lower
        ) | func.lower(Ics205RadioChannel.functions).like(
            search_lower
        ) | func.lower(Ics205RadioChannel.assignment).like(
            search_lower
        ) | func.lower(Ics205RadioChannel.remarks).like(
            search_lower
        )
        

    return await repo.read_paginated_items(
        Ics205RadioChannel, page, limit, condition
    )


# Endpoint untuk read by ics_205_id
@router.get(
    "/read-by-ics-id/{ics_205_id}", response_model=List[Ics205RadioChannel]
)
async def read_radio_channel_by_ics_id(
    ics_205_id: int, repo: BaseRepository = Depends(get_repository),
):
    condition = Ics205RadioChannel.ics_205_id == ics_205_id
    return await repo.read_items_by_condition(Ics205RadioChannel, condition)
