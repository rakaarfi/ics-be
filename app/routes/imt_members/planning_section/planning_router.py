from fastapi import APIRouter

from app.routes.imt_members.planning_section import (
    planning_section_chief,
    situation_unit_leader,
    resources_unit_leader,
    documentation_unit_leader,
    demobilization_unit_leader,
    environmental_unit_leader,
    technical_specialist,
)

router = APIRouter()

router.include_router(planning_section_chief.router, 
                        prefix="/planning-section-chief")
router.include_router(situation_unit_leader.router, 
                        prefix="/situation-unit-leader")
router.include_router(resources_unit_leader.router, 
                        prefix="/resources-unit-leader")
router.include_router(documentation_unit_leader.router, 
                        prefix="/documentation-unit-leader")
router.include_router(demobilization_unit_leader.router, 
                        prefix="/demobilization-unit-leader")
router.include_router(environmental_unit_leader.router, 
                        prefix="/environmental-unit-leader")
router.include_router(technical_specialist.router, 
                        prefix="/technical-specialist")
