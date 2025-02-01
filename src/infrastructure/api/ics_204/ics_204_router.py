from fastapi import APIRouter

from src.infrastructure.api.ics_204 import (
                                ics_204, personnel_assigned, equipment_assigned,
                                ics_204_preparation_os_chief, ics_204_preparation_ru_leader
                                )

router = APIRouter()

router.include_router(ics_204.router, prefix="/main")
router.include_router(personnel_assigned.router, prefix="/personnel-assigned")
router.include_router(equipment_assigned.router, prefix="/equipment-assigned")
router.include_router(ics_204_preparation_os_chief.router, prefix="/preparation-os-chief")
router.include_router(ics_204_preparation_ru_leader.router, prefix="/preparation-ru-leader")