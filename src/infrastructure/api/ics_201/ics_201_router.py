from fastapi import APIRouter

from src.infrastructure.api.ics_201 import (actions_strategies_tactics, chart,
                                ics_201, resource_summary, export_docx, ics_201_approval)

router = APIRouter()

router.include_router(ics_201.router, prefix="/main")
router.include_router(chart.router, prefix="/chart")
router.include_router(resource_summary.router, prefix="/resource-summary")
router.include_router(
    actions_strategies_tactics.router, prefix="/actions-strategies-tactics"
)
router.include_router(ics_201_approval.router, prefix="/approval")
router.include_router(export_docx.router, prefix="/export-docx")
