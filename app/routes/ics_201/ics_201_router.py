from fastapi import APIRouter

from app.routes.ics_201 import (
    actions_strategies_tactics,
    chart,
    resource_summary,
    ics_201
)

router = APIRouter()

router.include_router(ics_201.router,
                        prefix="/main")
router.include_router(chart.router,
                        prefix="/chart")
router.include_router(resource_summary.router,
                        prefix="/resource-summary")
router.include_router(actions_strategies_tactics.router,
                        prefix="/actions-strategies-tactics")