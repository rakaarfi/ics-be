from datetime import time
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, func, select

from app.config.database import get_session
from app.crud.crud import (delete_item, read_item_by_id,
                           read_items, read_paginated_items, update_item)
from app.models.ics_201_models import ActionsStrategiesTactics
from app.models.pagination_models import PaginationResponse


# Define a new model to allow the creation of multiple entries in a single API request
class ActionsStrategiesTacticsBase(SQLModel):
    time_initiated: time
    actions: str
    ics_201_id: Optional[int] = None


class ActionsStrategiesTacticsCreate(SQLModel):
    datas: List[ActionsStrategiesTacticsBase]


class ActionsStrategiesTacticsDelete(BaseModel):
    ids: list[int]


router = APIRouter()


# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Actions Strategies Tactics",
    description="Create a new Actions Strategies Tactics",
)
async def create_actions_strategies_tactics(
    item: ActionsStrategiesTacticsCreate, session: AsyncSession = Depends(get_session)
):
    created_data = []
    for data in item.datas:
        new_data = ActionsStrategiesTactics(**data.model_dump())
        session.add(new_data)
        created_data.append(new_data)
    await session.commit()
    return created_data


# Endpoint untuk read
@router.get("/read/")
async def read_actions_strategies_tactics(session: AsyncSession = Depends(get_session)):
    return await read_items(ActionsStrategiesTactics, session)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_actions_strategies_tactics_by_id(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(ActionsStrategiesTactics, id, session)


# Endpoint untuk update
@router.put("/update/{id}")
async def update_actions_strategies_tactics(
    updated_data: ActionsStrategiesTactics,
    id: int,
    session: AsyncSession = Depends(get_session),
):
    return await update_item(ActionsStrategiesTactics, id, updated_data, session)


# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_actions_strategies_tactics(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await delete_item(ActionsStrategiesTactics, id, session)


# Endpoint untuk delete multiple
async def delete_actions_by_ids(session, ids):
    await session.execute(
        delete(ActionsStrategiesTactics).where(ActionsStrategiesTactics.id.in_(ids))
    )
    await session.commit()


@router.delete("/delete-many/")
async def delete_multiple_actions(
    ids: ActionsStrategiesTacticsDelete, session: AsyncSession = Depends(get_session)
):
    print("Received IDs for deletion:", ids.ids)
    if not ids.ids:
        raise HTTPException(status_code=400, detail="No IDs provided")
    await delete_actions_by_ids(session, ids.ids)
    return {"message": "Actions deleted successfully"}


# Endpoint untuk read paginated
@router.get(
    "/read-paginated/", response_model=PaginationResponse[ActionsStrategiesTactics]
)
async def read_actions_strategies_tactics_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    session: AsyncSession = Depends(get_session),
):
    condition = None

    if search:
        search_lower = f"%{search.lower()}%"
        condition = func.lower(ActionsStrategiesTactics.actions).like(
            search_lower
        ) | func.lower(
            func.to_char(ActionsStrategiesTactics.time_initiated, "HH24:MI")
        ).like(
            search_lower
        )

    return await read_paginated_items(
        ActionsStrategiesTactics, page, limit, session, condition
    )


# Endpoint untuk read by ics_201_id
@router.get(
    "/read-by-ics-id/{ics_201_id}", response_model=List[ActionsStrategiesTactics]
)
async def read_actions_strategies_tactics_by_ics_id(
    ics_201_id: int, session: AsyncSession = Depends(get_session)
):
    # Query the database for records with the specified ics_201_id
    statement = select(ActionsStrategiesTactics).where(
        ActionsStrategiesTactics.ics_201_id == ics_201_id
    )
    results = await session.execute(statement)
    actions_strategies_tactics = results.scalars().all()

    # Return the list of records
    return actions_strategies_tactics
