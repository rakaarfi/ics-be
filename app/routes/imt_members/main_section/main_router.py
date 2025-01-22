from fastapi import APIRouter

from app.routes.imt_members.main_section import (
    incident_commander,
    deputy_incident_commander,
    human_capital_officer,
    legal_officer,
    liaison_officer,
    operation_section_chief,
    public_information_officer,
    safety_officer,
)

router = APIRouter()

router.include_router(incident_commander.router,
                        prefix="/incident-commander")
router.include_router(deputy_incident_commander.router,
                        prefix="/deputy-incident-commander")
router.include_router(safety_officer.router,
                        prefix="/safety-officer")
router.include_router(public_information_officer.router,
                        prefix="/public-information-officer")
router.include_router(liaison_officer.router,
                        prefix="/liaison-officer")
router.include_router(legal_officer.router,
                        prefix="/legal-officer")
router.include_router(human_capital_officer.router,
                        prefix="/human-capital-officer")
router.include_router(operation_section_chief.router,
                        prefix="/operation-section-chief")
