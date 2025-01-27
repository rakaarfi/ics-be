from typing import List, Optional

from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, func

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_204_models import PersonnelAssigned
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException


# Define a new model to allow the creation of multiple entries in a single API request
class PersonnelAssignedBase(SQLModel):
    ics_204_id: Optional[int] = None
    name: str
    number: str
    location: str
    equipment_tools_remarks: str
    

class PersonnelAssignedCreate(SQLModel):
    datas: List[PersonnelAssignedBase]
    

class PersonnelAssignedDelete(BaseModel):
    ids: list[int]
    
    
router = APIRouter()

    
# Dependency to get the repository
def get_repository(session: AsyncSession = Depends(get_session)) -> BaseRepository:
    return BaseRepository(session)


# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Personnel Assigned",
    description="Create a new Personnel Assigned",
)
async def create_personnel_assigned(
    item: PersonnelAssignedCreate, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_items(PersonnelAssigned, item.datas)


# Endpoint untuk read
@router.get("/read/")
async def read_personnel_assigned(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(PersonnelAssigned)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_personnel_assigned_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(PersonnelAssigned, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk update
@router.put("/update/{id}")
async def update_personnel_assigned(
    updated_data: PersonnelAssigned,
    id: int,
    repo: BaseRepository = Depends(get_repository),
):
    try:
        return await repo.update_item(PersonnelAssigned, id, updated_data)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_personnel_assigned(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(PersonnelAssigned, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete multiple
@router.delete("/delete-many/")
async def delete_multiple_personnel_assigned(
    ids: PersonnelAssignedDelete, repo: BaseRepository = Depends(get_repository),
):
    return await repo.delete_items_by_ids(PersonnelAssigned, ids.ids)


# Endpoint untuk read paginated
@router.get(
    "/read-paginated/", response_model=PaginationResponse[PersonnelAssigned]
)
async def read_personnel_assigned_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    if search:
        search_lower = f"%{search.lower()}%"
        condition = func.lower(PersonnelAssigned.name).like(
            search_lower
        ) | func.lower(PersonnelAssigned.number).like(
            search_lower
        ) | func.lower(PersonnelAssigned.location).like(
            search_lower
        ) | func.lower(PersonnelAssigned.equipment_tools_remarks).like(
            search_lower
        )
        

    return await repo.read_paginated_items(
        PersonnelAssigned, page, limit, condition
    )


# Endpoint untuk read by ics_204_id
@router.get(
    "/read-by-ics-id/{ics_204_id}", response_model=List[PersonnelAssigned]
)
async def read_personnel_assigned_by_ics_id(
    ics_204_id: int, repo: BaseRepository = Depends(get_repository),
):
    condition = PersonnelAssigned.ics_204_id == ics_204_id
    return await repo.read_items_by_condition(PersonnelAssigned, condition)
