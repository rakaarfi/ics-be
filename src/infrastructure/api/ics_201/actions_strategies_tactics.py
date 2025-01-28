from datetime import time
from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, func

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.ics_201_models import Ics201ActionsStrategiesTactics
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException


# Define a new model to allow the creation of multiple entries in a single API request
class Ics201ActionsStrategiesTacticsBase(SQLModel):
    time_initiated: time
    actions: str
    ics_201_id: Optional[int] = None


class Ics201ActionsStrategiesTacticsCreate(SQLModel):
    datas: List[Ics201ActionsStrategiesTacticsBase]


class Ics201ActionsStrategiesTacticsDelete(BaseModel):
    ids: list[int]


router = APIRouter()

# Dependency to get the repository
def get_repository(session: AsyncSession = Depends(get_session)) -> BaseRepository:
    return BaseRepository(session)


# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Actions Strategies Tactics",
    description="Create a new Actions Strategies Tactics",
)
async def create_actions_strategies_tactics(
    item: Ics201ActionsStrategiesTacticsCreate, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_items(Ics201ActionsStrategiesTactics, item.datas)


# Endpoint untuk read
@router.get("/read/")
async def read_actions_strategies_tactics(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(Ics201ActionsStrategiesTactics)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_actions_strategies_tactics_by_id(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.read_item_by_id(Ics201ActionsStrategiesTactics, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk update
@router.put("/update/{id}")
async def update_actions_strategies_tactics(
    updated_data: Ics201ActionsStrategiesTactics,
    id: int,
    repo: BaseRepository = Depends(get_repository),
):
    try:
        return await repo.update_item(Ics201ActionsStrategiesTactics, id, updated_data)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_actions_strategies_tactics(
    id: int, repo: BaseRepository = Depends(get_repository)
):
    try:
        return await repo.delete_item(Ics201ActionsStrategiesTactics, id)
    except NotFoundException as e:
        raise e
    

# Endpoint untuk delete multiple
@router.delete("/delete-many/")
async def delete_multiple_actions(
    ids: Ics201ActionsStrategiesTacticsDelete, repo: BaseRepository = Depends(get_repository),
):
    return await repo.delete_items_by_ids(Ics201ActionsStrategiesTactics, ids.ids)


# Endpoint untuk read paginated
@router.get(
    "/read-paginated/", response_model=PaginationResponse[Ics201ActionsStrategiesTactics]
)
async def read_actions_strategies_tactics_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None

    if search:
        search_lower = f"%{search.lower()}%"
        condition = func.lower(Ics201ActionsStrategiesTactics.actions).like(
            search_lower
        ) | func.lower(
            func.to_char(Ics201ActionsStrategiesTactics.time_initiated, "HH24:MI")
        ).like(
            search_lower
        )

    return await repo.read_paginated_items(
        Ics201ActionsStrategiesTactics, page, limit, condition
    )


# Endpoint untuk read by ics_201_id
@router.get(
    "/read-by-ics-id/{ics_201_id}", response_model=List[Ics201ActionsStrategiesTactics]
)
async def read_actions_strategies_tactics_by_ics_id(
    ics_201_id: int, repo: BaseRepository = Depends(get_repository),
):
    condition = Ics201ActionsStrategiesTactics.ics_201_id == ics_201_id
    return await repo.read_items_by_condition(Ics201ActionsStrategiesTactics, condition)
