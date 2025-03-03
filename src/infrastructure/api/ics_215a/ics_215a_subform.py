from typing import List, Optional

from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, func

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_215a_models import Ics215ASubForm
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException


# Define a new model to allow the creation of multiple entries in a single API request
class Ics215ASubFormBase(SQLModel):
    ics_215a_id: Optional[int] = None
    incident_area: str
    hazards_risks: str
    mitigations: str
    

class Ics215ASubFormCreate(SQLModel):
    datas: List[Ics215ASubFormBase]
    

class Ics215ASubFormDelete(BaseModel):
    ids: list[int]
    
    
router = APIRouter()

    
# Dependency to get the repository
def get_repository(session: AsyncSession = Depends(get_session)) -> BaseRepository:
    return BaseRepository(session)


# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Equipment Assigned",
    description="Create a new Equipment Assigned",
)
async def create_equipment_assigned(
    item: Ics215ASubFormCreate, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_items(Ics215ASubForm, item.datas)


# Endpoint untuk read
@router.get("/read/")
async def read_equipment_assigned(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(Ics215ASubForm)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_equipment_assigned_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(Ics215ASubForm, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk update
@router.put("/update/{id}")
async def update_equipment_assigned(
    updated_data: Ics215ASubForm,
    id: int,
    repo: BaseRepository = Depends(get_repository),
):
    try:
        return await repo.update_item(Ics215ASubForm, id, updated_data)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_equipment_assigned(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(Ics215ASubForm, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete multiple
@router.delete("/delete-many/")
async def delete_multiple_equimpent_assigned(
    ids: Ics215ASubFormDelete, repo: BaseRepository = Depends(get_repository),
):
    return await repo.delete_items_by_ids(Ics215ASubForm, ids.ids)


# Endpoint untuk read paginated
@router.get(
    "/read-paginated/", response_model=PaginationResponse[Ics215ASubForm]
)
async def read_equipment_assigned_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    if search:
        search_lower = f"%{search.lower()}%"
        condition = func.lower(Ics215ASubForm.kind).like(
            search_lower
        ) | func.lower(Ics215ASubForm.incident_area).like(
            search_lower
        ) | func.lower(Ics215ASubForm.hazards_risks).like(
            search_lower
        ) | func.lower(Ics215ASubForm.mitigations).like(
            search_lower
        )
        
    return await repo.read_paginated_items(
        Ics215ASubForm, page, limit, condition
    )


# Endpoint untuk read by ics_215a_id
@router.get(
    "/read-by-ics-id/{ics_215a_id}", response_model=List[Ics215ASubForm]
)
async def read_equipment_assigned_by_ics_id(
    ics_215a_id: int, repo: BaseRepository = Depends(get_repository),
):
    condition = Ics215ASubForm.ics_215a_id == ics_215a_id
    return await repo.read_items_by_condition(Ics215ASubForm, condition)
