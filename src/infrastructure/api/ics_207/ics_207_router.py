from fastapi import APIRouter

from src.infrastructure.api.ics_207 import (ics_207_export_docx)

router = APIRouter()

router.include_router(ics_207_export_docx.router, prefix="/export-docx")
