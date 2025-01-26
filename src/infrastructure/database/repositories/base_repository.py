from typing import Any, Optional, Type, List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select, delete

from src.core.exceptions import NotFoundException, BadRequestException
from src.infrastructure.utils.utils import (
    build_pagination_response,
    paginate_query,
    convert_string_to_date_time,
)


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_item(
        self,
        model: Type[SQLModel],
        item: dict | SQLModel,
    ):
        item = convert_string_to_date_time(item)

        #     # Convert string IDs to integers
        for field in item.__fields__:
            if field.endswith("_id") and isinstance(getattr(item, field), str):
                try:
                    setattr(item, field, int(getattr(item, field)))
                except ValueError as e:
                    raise BadRequestException(
                        detail=f"Invalid ID format for {field}. Expected an integer. Error: {str(e)}"
                    )

        if isinstance(item, SQLModel):
            item_data = (
                item.model_dump()
            )
        else:
            item_data = item

        new_item = model(**item_data)
        self.session.add(new_item)
        await self.session.commit()
        await self.session.refresh(new_item)
        return new_item


    async def read_items(self, model: Type[SQLModel]):
        query = select(model).order_by(model.id)
        result = await self.session.execute(query)
        items = result.scalars().all()
        return items


    async def read_item_by_id(self, model: Type[SQLModel], item_id: int):
        item = await self.session.get(model, item_id)
        if not item:
            raise NotFoundException(f"{model.__name__} not found")
        return item


    async def update_item(
        self, model: Type[SQLModel], item_id: int, update_data: dict
    ):
        update_data = convert_string_to_date_time(update_data)

        for field in update_data.__fields__:
            if field.endswith("_id") and isinstance(getattr(update_data, field), str):
                try:
                    setattr(update_data, field, int(getattr(update_data, field)))
                except ValueError as e:
                    raise BadRequestException(
                        detail=f"Invalid ID format for {field}. Expected an integer. Error: {str(e)}"
                    )

        item = await self.session.get(model, item_id)
        if not item:
            raise NotFoundException(f"{model.__name__} not found")

        if hasattr(update_data, "model_dump"):
            update_data = update_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(item, key, value)

        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item


    async def delete_item(self, model: Type[SQLModel], item_id: int):
        item = await self.session.get(model, item_id)
        if not item:
            raise NotFoundException(f"{model.__name__} not found")

        await self.session.delete(item)
        await self.session.commit()
        return {"message": f"{model.__name__} deleted successfully"}


    async def read_paginated_items(
        self,
        model: Type[SQLModel],
        page: int,
        limit: int,
        condition: Optional[Any] = None,
    ):
        query = select(model).order_by(model.id)

        # Search condition
        if condition is not None:
            query = query.where(condition)

        data, total_pages, total_data = await paginate_query(
            statement=query, session=self.session, page=page, limit=limit
        )

        return build_pagination_response(data, page, total_pages, total_data)
    
    async def read_items_by_condition(self, model: Type[SQLModel], condition: Any):
        query = select(model).where(condition)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def delete_items_by_ids(self, model: Type[SQLModel], ids: List[int]):
        await self.session.execute(delete(model).where(model.id.in_(ids)))
        await self.session.commit()
        return {"message": f"{len(ids)} items deleted successfully"}
    
    async def create_items(self, model: Type[SQLModel], items: List[dict | SQLModel]):
        """
        Membuat banyak item sekaligus.
        """
        created_data = []
        for item in items:
            if isinstance(item, SQLModel):
                item_data = item.model_dump()
            else:
                item_data = item
            new_item = model(**item_data)
            self.session.add(new_item)
            created_data.append(new_item)
        await self.session.commit()
        return created_data
