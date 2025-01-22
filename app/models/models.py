from sqlmodel import SQLModel
from typing import Generic, TypeVar


# Model untuk Pagination
T = TypeVar("T")
class PaginationResponse(SQLModel, Generic[T]):
    data: T
    current_page: int
    total_pages: int
    total_data: int
    