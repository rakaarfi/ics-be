from fastapi.exceptions import HTTPException
from sqlmodel import select, func, SQLModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Tuple, List, Any, Type


async def paginate_query(
    statement,
    session: AsyncSession,
    page: int,
    limit: int,
    scalar: bool = True
) -> Tuple[list, int, int]:
    """
    Paginates a SQLAlchemy query and returns a tuple of (paginated data, total data, total pages).

    Args:
        statement (Select): The SQLAlchemy query to be paginated.
        session (AsyncSession): The SQLAlchemy session to use.
        page (int): The page number to retrieve.
        limit (int): The limit of items per page.
        scalar (bool, optional): Whether to return a scalar value. Defaults to True. If False, returns a list.

    Returns:
        Tuple[list, int, int]: A tuple of (paginated data, total data, total pages).
    """
    if page < 1:
        raise HTTPException(status_code=400, detail="Page number must be greater than 0")
    if limit < 1:
        raise HTTPException(status_code=400, detail="Limit must be greater than 0")

    offset = (page - 1) * limit
    paginated_query = statement.offset(offset).limit(limit)

    if scalar:
        raw_data_result = await session.execute(paginated_query)
        raw_data = raw_data_result.scalars().all()  # Mengembalikan satu kolom
    else:
        raw_data_result = await session.execute(paginated_query)
        raw_data = raw_data_result.all()  # Mengembalikan banyak kolom

    query_count = select(func.count()).select_from(statement.subquery())
    """
    SELECT COUNT(*) FROM (subquery)
    atau
    SELECT COUNT(*) FROM (
        SELECT ... FROM ... WHERE ...
    )
    Membuat query untuk menghitung jumlah total baris dari hasil subquery
    """
    result_count = await session.execute(query_count)
    total_data = result_count.scalars().one()  # Mengambil hasil tunggal (jumlah total baris)

    total_pages = (total_data + limit - 1) // limit
    return raw_data, total_pages, total_data


def build_pagination_response(
    data: List[Any],
    page: int,
    total_pages: int,
    total_data: int
) -> dict:
    """
    Build a standardized response for paginated data.

    :param data: Paginated data list.
    :param page: Current page number.
    :param total_pages: Total number of pages.
    :param total_data: Total number of data.
    :return: Pagination response dictionary.
    """
    return {
        "data": data,
        "current_page": page,
        "total_pages": total_pages,
        "total_data": total_data
    }
    
    
def imt_members_search_condition(search: str, model: Type[SQLModel],):
    search_lower = f"%{search.lower()}%"
    condition = (
        func.lower(model.name).like(search_lower) |
        func.lower(model.nf_name).like(search_lower) |
        func.lower(model.role).like(search_lower) |
        func.lower(model.office_phone).like(search_lower) |
        func.lower(model.mobile_phone).like(search_lower)
    )
    return condition
