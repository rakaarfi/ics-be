from fastapi import APIRouter

from src.infrastructure.api.ics_204 import (
                                ics_204, ics_204_preparation,
                                personnel_assigned, equipment_assigned)

router = APIRouter()

router.include_router(ics_204.router, prefix="/main")
router.include_router(personnel_assigned.router, prefix="/personnel-assigned")
router.include_router(equipment_assigned.router, prefix="/equipment-assigned")
router.include_router(ics_204_preparation.router, prefix="/preparation")