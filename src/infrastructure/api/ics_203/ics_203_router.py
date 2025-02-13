from fastapi import APIRouter

from src.infrastructure.api.ics_203 import (
                                ics_203, ics_203_preparation, ics_203_export_docx)

router = APIRouter()

router.include_router(ics_203.router, prefix="/main")
router.include_router(ics_203_preparation.router, prefix="/preparation")
router.include_router(ics_203_export_docx.router, prefix="/export-docx")