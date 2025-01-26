from datetime import date, time
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, func, select

from app.config.database import get_session
from app.crud.crud import (delete_item, read_item_by_id,
                           read_items, read_paginated_items, update_item)
from app.models.ics_201_models import ResourceSummary
from app.models.pagination_models import PaginationResponse


# Define a new model to allow the creation of multiple entries in a single API request
class ResourceSummaryBase(SQLModel):
    resource: str
    resource_identified: str
    date_ordered: date
    time_ordered: time
    eta: str
    is_arrived: bool
    notes: str
    ics_201_id: Optional[int] = None


class ResourceSummaryCreate(SQLModel):
    datas: List[ResourceSummaryBase]


class ResourceSummaryDelete(BaseModel):
    ids: list[int]


router = APIRouter()


# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Resource Summary",
    description="Create a new Resource Summary",
)
async def create_resource_summary(
    item: ResourceSummaryCreate, session: AsyncSession = Depends(get_session)
):
    created_data = []
    for data in item.datas:
        new_data = ResourceSummary(**data.model_dump())
        session.add(new_data)
        created_data.append(new_data)
    await session.commit()
    return created_data


# Endpoint untuk read
@router.get("/read/")
async def read_resource_summary(session: AsyncSession = Depends(get_session)):
    return await read_items(ResourceSummary, session)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_resource_summary_by_id(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(ResourceSummary, id, session)


# Endpoint untuk update
@router.put("/update/{id}")
async def update_resource_summary(
    updated_data: ResourceSummary, id: int, session: AsyncSession = Depends(get_session)
):
    return await update_item(ResourceSummary, id, updated_data, session)


# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_resource_summary(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await delete_item(ResourceSummary, id, session)


# Endpoint untuk delete multiple
async def delete_resource_summary_by_ids(session, ids):
    await session.execute(delete(ResourceSummary).where(ResourceSummary.id.in_(ids)))
    await session.commit()


@router.delete("/delete-many/")
async def delete_multiple_resource_summary(
    ids: ResourceSummaryDelete, session: AsyncSession = Depends(get_session)
):
    print("Received IDs for deletion:", ids.ids)
    if not ids.ids:
        raise HTTPException(status_code=400, detail="No IDs provided")
    await delete_resource_summary_by_ids(session, ids.ids)
    return {"message": "Resource Summary deleted successfully"}


# Endpoint untuk read paginated
@router.get(
    "/read-paginated/", response_model=PaginationResponse[List[ResourceSummary]]
)
async def read_resource_summary_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    session: AsyncSession = Depends(get_session),
):
    condition = None

    if search:
        search_lower = f"%{search.lower()}%"
        condition = (
            func.lower(ResourceSummary.resource).like(search_lower)
            | func.lower(ResourceSummary.resource_identified).like(search_lower)
            | func.lower(func.to_char(ResourceSummary.date_ordered, "YYYY-MM-DD")).like(
                search_lower
            )
            | func.lower(func.to_char(ResourceSummary.time_ordered, "HH24:MI")).like(
                search_lower
            )
            | func.lower(ResourceSummary.eta).like(search_lower)
            | func.lower(ResourceSummary.notes).like(search_lower)
        )

    return await read_paginated_items(ResourceSummary, page, limit, session, condition)


# Endpoint untuk read by ics_201_id
@router.get("/read-by-ics-201-id/{ics_201_id}", response_model=List[ResourceSummary])
async def read_resource_summary_by_ics_201_id(
    ics_201_id: int, session: AsyncSession = Depends(get_session)
):
    # Query the database for records with the specified ics_201_id
    statement = select(ResourceSummary).where(ResourceSummary.ics_201_id == ics_201_id)
    results = await session.execute(statement)
    resource_summary = results.scalars().all()

    # Return the list of records
    return resource_summary
