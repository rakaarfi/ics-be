from typing import Generic, TypeVar

from sqlmodel import SQLModel

# Model untuk Pagination
T = TypeVar("T")


class PaginationResponse(SQLModel, Generic[T]):
    data: T
    current_page: int
    total_pages: int
    total_data: int
