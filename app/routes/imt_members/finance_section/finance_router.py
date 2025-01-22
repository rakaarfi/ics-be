from fastapi import APIRouter

from app.routes.imt_members.finance_section import (
    finance_section_chief,
    procurement_unit_leader,
    compensation_claim_unit_leader,
    cost_unit_leader,
    time_unit_leader,
)

router = APIRouter()

router.include_router(finance_section_chief.router, 
                        prefix="/finance-section-chief")
router.include_router(procurement_unit_leader.router, 
                        prefix="/procurement-unit-leader")
router.include_router(compensation_claim_unit_leader.router, 
                        prefix="/compensation-claim-unit-leader")
router.include_router(cost_unit_leader.router, 
                        prefix="/cost-unit-leader")
router.include_router(time_unit_leader.router, 
                        prefix="/time-unit-leader")
