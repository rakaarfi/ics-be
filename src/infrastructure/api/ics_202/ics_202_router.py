from fastapi import APIRouter

from src.infrastructure.api.ics_202 import (
                                ics_202, ics_202_preparation, ics_202_approval,
                                ics_202_export_docx)

router = APIRouter()

router.include_router(ics_202.router, prefix="/main")
router.include_router(ics_202_preparation.router, prefix="/preparation")
router.include_router(ics_202_approval.router, prefix="/approval")
router.include_router(ics_202_export_docx.router, prefix="/export-docx")