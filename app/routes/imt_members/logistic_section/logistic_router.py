from fastapi import APIRouter

from app.routes.imt_members.logistic_section import (
    communication_unit_leader, facility_unit_leader, food_unit_leader,
    logistic_section_chief, medical_unit_leader, supply_unit_leader,
    transportation_unit_leader)

router = APIRouter()

router.include_router(logistic_section_chief.router, prefix="/logistic-section-chief")
router.include_router(
    communication_unit_leader.router, prefix="/communication-unit-leader"
)
router.include_router(medical_unit_leader.router, prefix="/medical-unit-leader")
router.include_router(food_unit_leader.router, prefix="/food-unit-leader")
router.include_router(facility_unit_leader.router, prefix="/facility-unit-leader")
router.include_router(supply_unit_leader.router, prefix="/supply-unit-leader")
router.include_router(
    transportation_unit_leader.router, prefix="/transportation-unit-leader"
)
