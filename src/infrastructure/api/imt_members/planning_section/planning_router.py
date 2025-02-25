from fastapi import APIRouter

from src.infrastructure.api.imt_members.planning_section import (
    demobilization_unit_leader, documentation_unit_leader,
    environmental_unit_leader, planning_section_chief, resources_unit_leader,
    situation_unit_leader, technical_specialist)

router = APIRouter()

router.include_router(planning_section_chief.router, prefix="/planning-section-chief")
router.include_router(situation_unit_leader.router, prefix="/situation-unit-leader")
router.include_router(resources_unit_leader.router, prefix="/resources-unit-leader")
router.include_router(
    documentation_unit_leader.router, prefix="/documentation-unit-leader"
)
router.include_router(
    demobilization_unit_leader.router, prefix="/demobilization-unit-leader"
)
router.include_router(
    environmental_unit_leader.router, prefix="/environmental-unit-leader"
)
router.include_router(technical_specialist.router, prefix="/technical-specialist")
