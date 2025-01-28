from typing import List, Optional

from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, func

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_204_models import Ics204EquipmentAssigned
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException, BadRequestException


# Define a new model to allow the creation of multiple entries in a single API request
class Ics204EquipmentAssignedBase(SQLModel):
    ics_204_id: Optional[int] = None
    kind: str
    quantity: int
    type_specification: str
    number: str
    location: str
    remarks: str
    

class Ics204EquipmentAssignedCreate(SQLModel):
    datas: List[Ics204EquipmentAssignedBase]
    

class Ics204EquipmentAssignedDelete(BaseModel):
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
    item: Ics204EquipmentAssignedCreate, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_items(Ics204EquipmentAssigned, item.datas)


# Endpoint untuk read
@router.get("/read/")
async def read_equipment_assigned(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(Ics204EquipmentAssigned)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_equipment_assigned_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(Ics204EquipmentAssigned, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk update
@router.put("/update/{id}")
async def update_equipment_assigned(
    updated_data: Ics204EquipmentAssigned,
    id: int,
    repo: BaseRepository = Depends(get_repository),
):
    try:
        return await repo.update_item(Ics204EquipmentAssigned, id, updated_data)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_equipment_assigned(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(Ics204EquipmentAssigned, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete multiple
@router.delete("/delete-many/")
async def delete_multiple_equimpent_assigned(
    ids: Ics204EquipmentAssignedDelete, repo: BaseRepository = Depends(get_repository),
):
    return await repo.delete_items_by_ids(Ics204EquipmentAssigned, ids.ids)


# Endpoint untuk read paginated
@router.get(
    "/read-paginated/", response_model=PaginationResponse[Ics204EquipmentAssigned]
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
        condition = func.lower(Ics204EquipmentAssigned.kind).like(
            search_lower
        ) | func.lower(Ics204EquipmentAssigned.type_specification).like(
            search_lower
        ) | func.lower(Ics204EquipmentAssigned.number).like(
            search_lower
        ) | func.lower(Ics204EquipmentAssigned.location).like(
            search_lower
        ) | func.lower(Ics204EquipmentAssigned.remarks).like(
            search_lower
        ) | func.lower(Ics204EquipmentAssigned.quantity).like(
            search_lower
        )
        

    return await repo.read_paginated_items(
        Ics204EquipmentAssigned, page, limit, condition
    )


# Endpoint untuk read by ics_204_id
@router.get(
    "/read-by-ics-id/{ics_204_id}", response_model=List[Ics204EquipmentAssigned]
)
async def read_equipment_assigned_by_ics_id(
    ics_204_id: int, repo: BaseRepository = Depends(get_repository),
):
    condition = Ics204EquipmentAssigned.ics_204_id == ics_204_id
    return await repo.read_items_by_condition(Ics204EquipmentAssigned, condition)
