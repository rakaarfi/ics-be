from fastapi import APIRouter

from src.infrastructure.api.ics_205 import (
                                ics_205, ics_205_preparation,
                                radio_channel)

router = APIRouter()

router.include_router(ics_205.router, prefix="/main")
router.include_router(radio_channel.router, prefix="/radio-channel")
router.include_router(ics_205_preparation.router, prefix="/preparation")