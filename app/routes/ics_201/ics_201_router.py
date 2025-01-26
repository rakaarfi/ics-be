from fastapi import APIRouter

from app.routes.ics_201 import (actions_strategies_tactics, approval, chart,
                                ics_201, resource_summary)

router = APIRouter()

router.include_router(ics_201.router, prefix="/main")
router.include_router(chart.router, prefix="/chart")
router.include_router(resource_summary.router, prefix="/resource-summary")
router.include_router(
    actions_strategies_tactics.router, prefix="/actions-strategies-tactics"
)
router.include_router(approval.router, prefix="/approval")
