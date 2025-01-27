from fastapi import APIRouter

from src.infrastructure.api.ics_208 import (
                                ics_208, ics_208_preparation)

router = APIRouter()

router.include_router(ics_208.router, prefix="/main")
router.include_router(ics_208_preparation.router, prefix="/preparation")