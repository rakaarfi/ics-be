from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel
from pydantic import field_validator


class BaseImtMember(SQLModel, table=False):
    """
    Base model for Incident Management Team (IMT) members.
    This model serves as the foundation for all IMT member roles.
    """
    id: int = Field(default=None, primary_key=True, description="Unique identifier for the IMT member.")
    name: str = Field(description="Name of the IMT member.")
    nf_name: str = Field(description="Natural function name of the IMT member.")
    role: str = Field(description="Role of the IMT member.")
    office_phone: str = Field(description="Office phone number of the IMT member.")
    mobile_phone: str = Field(description="Mobile phone number of the IMT member.")
    join_date: date = Field(description="Join date of the IMT member.")
    exit_date: Optional[date] = Field(description="Exit date of the IMT member.")
    
    @field_validator("exit_date")
    @classmethod
    def check_exit_date(cls, value: date, values) -> date:
        if value and "join_date" in values.data and value < values.data["join_date"]:
            raise ValueError("Exit date cannot be earlier than join date")
        return value
