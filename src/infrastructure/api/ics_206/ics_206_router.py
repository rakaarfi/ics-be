from fastapi import APIRouter

from src.infrastructure.api.ics_206 import (
                                ics_206, ics_206_preparation,
                                hospitals, medical_aid_station,
                                transportation, ics_206_approval,
                                ics_206_export_docx)

router = APIRouter()

router.include_router(ics_206.router, prefix="/main")
router.include_router(hospitals.router, prefix="/hospitals")
router.include_router(medical_aid_station.router, prefix="/medical-aid-station")
router.include_router(transportation.router, prefix="/transportation")
router.include_router(ics_206_preparation.router, prefix="/preparation")
router.include_router(ics_206_approval.router, prefix="/approval")
router.include_router(ics_206_export_docx.router, prefix="/export-docx")