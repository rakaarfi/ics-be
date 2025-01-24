# from sqlmodel import select, SQLModel, func, Session
# from fastapi import HTTPException
# from typing import Type, List
# from datetime import datetime

# from app.utils.utils import paginate_query, build_pagination_response

# def convert_string_to_date_time(item: SQLModel | dict) -> SQLModel:
#     """
#     Utility function to convert string dates and times to `date` and `time` objects.
#     Can handle both SQLModel and dict inputs.
#     """
#     # If input is dict, convert to SQLModel first
#     if isinstance(item, dict):
#         return item
    
#     date_fields = [
#         'join_date', 'exit_date', 'date_from', 'date_to', 
#         'date_incident'
#     ]
#     time_fields = [
#         'time_incident', 'time_from', 'time_to'
#     ]
    
#     for field in date_fields:
#         if hasattr(item, field) and isinstance(getattr(item, field), str):
#             try:
#                 setattr(item, field, datetime.strptime(getattr(item, field), "%Y-%m-%d").date())
#             except ValueError as e:
#                 raise HTTPException(
#                     status_code=400,
#                     detail=f"Invalid format for field '{field}'. Expected format: YYYY-MM-DD. Error: {str(e)}",
#                 )
                
#     for field in time_fields:
#         if hasattr(item, field) and isinstance(getattr(item, field), str):
#             try:
#                 setattr(item, field, datetime.strptime(getattr(item, field), "%H:%M").time())
#             except ValueError as e:
#                 raise HTTPException(
#                     status_code=400,
#                     detail=f"Invalid format for field '{field}'. Expected format: HH:MM. Error: {str(e)}",
#                 )
                
#     return item


# def create_item(
#     model: Type[SQLModel], 
#     item: dict, 
#     session: Session
# ):
#     # Convert string dates and times to `date` and `time` objects
#     item = convert_string_to_date_time(item)
        
#     # Convert string IDs to integers
#     for field in item.__fields__:
#         if field.endswith('_id') and isinstance(getattr(item, field), str):
#             try:
#                 setattr(item, field, int(getattr(item, field)))
#             except ValueError as e:
#                 raise HTTPException(
#                     status_code=400,
#                     detail=f"Invalid ID format for {field}. Expected an integer. Error: {str(e)}"
#                 )
    
#     new_item = model(**item.model_dump())
#     session.add(new_item)
#     session.commit()
#     session.refresh(new_item)
#     return new_item

# def read_items(
#     model: Type[SQLModel], 
#     session: Session
# ):

#     query = select(model).order_by(model.id)
#     items = session.execute(query).scalars().all()
#     return items

# def read_item_by_id(
#     model: Type[SQLModel], 
#     item_id: int, 
#     session: Session
# ):
    
#     item = session.get(model, item_id)
#     if not item:
#         raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
#     return item

# def update_item(
#     model: Type[SQLModel], 
#     item_id: int, 
#     update_data: dict, 
#     session: Session
# ):
#     # Convert string dates and times to `date` and `time` objects
#     update_data = convert_string_to_date_time(update_data)
        
#     for field in update_data.__fields__:
#         if field.endswith('_id') and isinstance(getattr(update_data, field), str):
#             try:
#                 setattr(update_data, field, int(getattr(update_data, field)))
#             except ValueError as e:
#                 raise HTTPException(
#                     status_code=400,
#                     detail=f"Invalid ID format for {field}. Expected an integer. Error: {str(e)}"
#                 )
        
#     item = session.get(model, item_id)
    
#     if not item:
#         raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    
#     # Jika update_data adalah model (bukan dictionary biasa), gunakan model_dump
#     if hasattr(update_data, 'model_dump'):
#         update_data = update_data.model_dump(exclude_unset=True)

#     for key, value in update_data.items():
#         setattr(item, key, value)
        
#     session.add(item)
#     session.commit()
#     session.refresh(item)
#     return item

# def delete_item(
#     model: Type[SQLModel], 
#     item_id: int, 
#     session: Session
# ):
    
#     item = session.get(model, item_id)
#     if not item:
#         raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    
#     session.delete(item)
#     session.commit()
#     return {"message": f"{model.__name__} deleted successfully"}

# def read_paginated_items(
#     model: Type[SQLModel], 
#     page: int, 
#     limit: int, 
#     search: str,
#     session: Session
# ):
    
#     query = select(model).order_by(model.id)
    
#     if search:
#         search_lower = f"%{search.lower()}%"
#         # Check if the model has the attributes for the first condition
#         if (
#                 hasattr(model, 'name') & 
#                 hasattr(model, 'nf_name') &
#                 hasattr(model, 'role') & 
#                 hasattr(model, 'office_phone') & 
#                 hasattr(model, 'mobile_phone')
#             ):
#             condition = (
#                 func.lower(model.name).like(search_lower) |
#                 func.lower(model.nf_name).like(search_lower) |
#                 func.lower(model.role).like(search_lower) |
#                 func.lower(model.office_phone).like(search_lower) |
#                 func.lower(model.mobile_phone).like(search_lower)
#             )
#         # Check if the model has the attributes for the second condition
#         elif (
#                 hasattr(model, 'date_from') & 
#                 hasattr(model, 'date_to') & 
#                 hasattr(model, 'remark')
#             ):
#             condition = (
#                 func.lower(model.remark).like(search_lower) |
#                 func.lower(func.to_char(model.date_from, 'YYYY-MM-DD')).like(search_lower) |
#                 func.lower(func.to_char(model.date_to, 'YYYY-MM-DD')).like(search_lower)
#             )
            
#         # Check if the model has the attributes for the third condition
#         elif (
#                 hasattr(model, 'no') & 
#                 hasattr(model, 'name') & 
#                 hasattr(model, 'date_incident') & 
#                 hasattr(model, 'time_incident') & 
#                 hasattr(model, 'timezone') & 
#                 hasattr(model, 'location') & 
#                 hasattr(model, 'description')
#             ):
#             condition = (
#                 func.lower(model.no).like(search_lower) |
#                 func.lower(model.name).like(search_lower) |
#                 func.lower(func.to_char(model.date_incident, 'YYYY-MM-DD')).like(search_lower) |
#                 func.lower(func.to_char(model.time_incident, 'HH24:MI')).like(search_lower) |
#                 func.lower(model.timezone).like(search_lower) |
#                 func.lower(model.location).like(search_lower) |
#                 func.lower(model.description).like(search_lower)
#             )
#         # Default condition
#         else:
#             condition = None
#         if condition is not None:
#             query = query.where(condition)

#     data, total_pages, total_data = paginate_query(
#         statement=query, 
#         session=session, 
#         page=page, 
#         limit=limit
#     )
    
#     return build_pagination_response(data, page, total_pages, total_data)


from sqlmodel import select, SQLModel, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from typing import Type, List, Any, Optional
from datetime import datetime

from app.utils.utils import paginate_query, build_pagination_response


def convert_string_to_date_time(item: SQLModel | dict) -> SQLModel:
    """
    Utility function to convert string dates and times to `date` and `time` objects.
    Can handle both SQLModel and dict inputs.
    """
    
    # If input is dict, convert to SQLModel first
    if isinstance(item, dict):
        return item

    date_fields = [
        'join_date', 'exit_date', 'date_from', 'date_to',
        'date_incident', 'date_initiated', 'date_ordered', 'date_approved'
    ]
    time_fields = [
        'time_incident', 'time_from', 'time_to', 'time_initiated', 'time_ordered',
        'time_approved'
    ]

    for field in date_fields:
        if hasattr(item, field) and isinstance(getattr(item, field), str):
            try:
                setattr(item, field, datetime.strptime(getattr(item, field), "%Y-%m-%d").date())
            except ValueError as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid format for field '{field}'. Expected format: YYYY-MM-DD. Error: {str(e)}",
                )

    for field in time_fields:
        if hasattr(item, field) and isinstance(getattr(item, field), str):
            try:
                setattr(item, field, datetime.strptime(getattr(item, field), "%H:%M").time())
            except ValueError as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid format for field '{field}'. Expected format: HH:MM. Error: {str(e)}",
                )

    return item


async def create_item(
    model: Type[SQLModel],
    item: dict | SQLModel,  # Terima dict atau SQLModel
    session: AsyncSession
):
    item = convert_string_to_date_time(item)
    
    #     # Convert string IDs to integers
    for field in item.__fields__:
        if field.endswith('_id') and isinstance(getattr(item, field), str):
            try:
                setattr(item, field, int(getattr(item, field)))
            except ValueError as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid ID format for {field}. Expected an integer. Error: {str(e)}"
                )
    
    if isinstance(item, SQLModel):
        item_data = item.model_dump()  # Hanya panggil model_dump() jika item adalah SQLModel
    else:
        item_data = item  # Jika item sudah dict, langsung gunakan

    new_item = model(**item_data)  # Gunakan item_data di sini
    session.add(new_item)
    await session.commit()
    await session.refresh(new_item)
    return new_item


async def read_items(
    model: Type[SQLModel],
    session: AsyncSession
):
    query = select(model).order_by(model.id)
    result = await session.execute(query)
    items = result.scalars().all()
    return items


async def read_item_by_id(
    model: Type[SQLModel],
    item_id: int,
    session: AsyncSession
):
    item = await session.get(model, item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return item


async def update_item(
    model: Type[SQLModel],
    item_id: int,
    update_data: dict,
    session: AsyncSession
):
    update_data = convert_string_to_date_time(update_data)
    
    for field in update_data.__fields__:
        if field.endswith('_id') and isinstance(getattr(update_data, field), str):
            try:
                setattr(update_data, field, int(getattr(update_data, field)))
            except ValueError as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid ID format for {field}. Expected an integer. Error: {str(e)}"
                )

    item = await session.get(model, item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")

    if hasattr(update_data, 'model_dump'):
        update_data = update_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(item, key, value)

    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item


async def delete_item(
    model: Type[SQLModel],
    item_id: int,
    session: AsyncSession
):
    item = await session.get(model, item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")

    await session.delete(item)
    await session.commit()
    return {"message": f"{model.__name__} deleted successfully"}


async def read_paginated_items(
    model: Type[SQLModel],
    page: int,
    limit: int,
    session: AsyncSession,
    condition: Optional[Any] = None
):
    query = select(model).order_by(model.id)

    # Search condition
    if condition is not None:
        query = query.where(condition)

    data, total_pages, total_data = await paginate_query(
        statement=query,
        session=session,
        page=page,
        limit=limit
    )

    return build_pagination_response(data, page, total_pages, total_data)
