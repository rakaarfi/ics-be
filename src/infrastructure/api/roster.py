from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import func

from src.infrastructure.config.database import get_session
from src.infrastructure.database.repositories.base_repository import BaseRepository
from src.core.entities.roster_models import ImtRoster
from src.core.entities.pagination_models import PaginationResponse
from src.core.exceptions import NotFoundException

router = APIRouter()

# Dependency untuk mendapatkan repository
def get_repository(session: AsyncSession = Depends(get_session)):
    return BaseRepository(session)


@router.post(
    "/create/", summary="Create Imt Roster", description="Create a new Imt Roster"
)
async def create_imt_roster(
    item: ImtRoster, repo: BaseRepository = Depends(get_repository)
):
    return await repo.create_item(ImtRoster, item)


@router.get("/read/")
async def read_imt_roster(repo: BaseRepository = Depends(get_repository)):
    return await repo.read_items(ImtRoster)


@router.get("/read/{id}")
async def read_imt_roster_by_id(id: int, repo: BaseRepository = Depends(get_repository)):
    try:
        return await repo.read_item_by_id(ImtRoster, id)
    except NotFoundException as e:
        raise e
    

@router.put("/update/{id}")
async def update_imt_roster(
    update_data: ImtRoster, id: int, repo: BaseRepository = Depends(get_repository)
):
    return await repo.update_item(ImtRoster, id, update_data)


@router.delete("/delete/{id}")
async def delete_imt_roster(id: int, repo: BaseRepository = Depends(get_repository)):
    return await repo.delete_item(ImtRoster, id)


@router.get("/read-paginated/", response_model=PaginationResponse[List[ImtRoster]])
async def read_imt_roster_paginated(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    repo: BaseRepository = Depends(get_repository),
):
    condition = None
    if search:
        search_lower = f"%{search.lower()}%"
        condition = (
            func.lower(ImtRoster.remark).like(search_lower)
            | func.lower(func.to_char(ImtRoster.date_from, "YYYY-MM-DD")).like(
                search_lower
            )
            | func.lower(func.to_char(ImtRoster.date_to, "YYYY-MM-DD")).like(
                search_lower
            )
        )

    return await repo.read_paginated_items(ImtRoster, page, limit, condition)