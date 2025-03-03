from fastapi import APIRouter

from src.infrastructure.api.ics_215a import (
                                ics_215a, ics_215a_subform, ics_215a_preparation_os_chief,
                                ics_215a_preparation_safety_officer, ics_215a_export_docx
                                )

router = APIRouter()

router.include_router(ics_215a.router, prefix="/main")
router.include_router(ics_215a_subform.router, prefix="/subform")
router.include_router(ics_215a_preparation_os_chief.router, prefix="/preparation-os-chief")
router.include_router(ics_215a_preparation_safety_officer.router, prefix="/preparation-safety-officer")
router.include_router(ics_215a_export_docx.router, prefix="/export-docx")