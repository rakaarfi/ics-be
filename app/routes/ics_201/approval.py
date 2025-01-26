from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.config.database import get_session
from app.crud.crud import (create_item, delete_item, read_item_by_id,
                           read_items, read_paginated_items, update_item)
from app.models.ics_201_models import Ics201Approval
from app.models.pagination_models import PaginationResponse

router = APIRouter()


# Endpoint untuk create
@router.post(
    "/create/",
    summary="Create Ics 201 Approval",
    description="Create a new Ics 201 Approval",
)
async def create_ics_201_approval(
    item: Ics201Approval, session: AsyncSession = Depends(get_session)
):
    return await create_item(Ics201Approval, item, session)


# Endpoint untuk read
@router.get("/read/")
async def read_ics_201_approval(session: AsyncSession = Depends(get_session)):
    return await read_items(Ics201Approval, session)


# Endpoint untuk read by id
@router.get("/read/{id}")
async def read_ics_201_approval_by_id(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await read_item_by_id(Ics201Approval, id, session)


# Endpoint untuk update
@router.put("/update/{id}")
async def update_ics_201_approval(
    updated_data: Ics201Approval, id: int, session: AsyncSession = Depends(get_session)
):
    return await update_item(Ics201Approval, id, updated_data, session)


# Endpoint untuk delete
@router.delete("/delete/{id}")
async def delete_ics_201_approval(
    id: int, session: AsyncSession = Depends(get_session)
):
    return await delete_item(Ics201Approval, id, session)


# Endpoint untuk read paginated
@router.get("/read-paginated/", response_model=PaginationResponse[List[Ics201Approval]])
async def read_ics_201_approval_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    session: AsyncSession = Depends(get_session),
):
    condition = None

    return await read_paginated_items(Ics201Approval, page, limit, session, condition)


# Endpoint untuk read by ics_201_id
@router.get("/read-by-ics-201-id/{ics_201_id}", response_model=List[Ics201Approval])
async def read_ics_201_approval_by_ics_201_id(
    ics_201_id: int, session: AsyncSession = Depends(get_session)
):
    # Query the database for records with the specified ics_201_id
    statement = select(Ics201Approval).where(Ics201Approval.ics_201_id == ics_201_id)
    results = await session.execute(statement)
    ics_201_approval = results.scalars().all()

    # Return the list of records
    return ics_201_approval
