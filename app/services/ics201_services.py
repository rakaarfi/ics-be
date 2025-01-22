from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.ics_201 import Ics201
from fastapi import HTTPException, status


async def save_map_sketch(session: AsyncSession, ics_id: int, filename: str):
    result = await session.execute(select(Ics201).where(Ics201.id == ics_id))
    ics_record = result.scalar_one_or_none()
    if not ics_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ics201 record with id {ics_id} not found"
        )
    ics_record.map_sketch = filename
    await session.commit()
    return ics_record
