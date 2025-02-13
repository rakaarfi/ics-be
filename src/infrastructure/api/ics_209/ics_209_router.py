from fastapi import APIRouter

from src.infrastructure.api.ics_209 import (
                                ics_209, ics_209_approval, ics_209_preparation,
                                ics_209_export_docx
                                )

router = APIRouter()

router.include_router(ics_209.router, prefix="/main")
router.include_router(ics_209_preparation.router, prefix="/preparation")
router.include_router(ics_209_approval.router, prefix="/approval")
router.include_router(ics_209_export_docx.router, prefix="/export-docx")