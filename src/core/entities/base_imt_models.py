from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class BaseImtMember(SQLModel, table=False):
    id: int = Field(default=None, primary_key=True)
    name: str
    nf_name: str
    role: str
    office_phone: str
    mobile_phone: str
    join_date: date
    exit_date: Optional[date]
