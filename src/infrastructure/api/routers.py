from fastapi import FastAPI

from src.infrastructure.api.incident_data import router as incident_data_router
from src.infrastructure.api.ics_201.ics_201_router import router as ics_201_router
from src.infrastructure.api.ics_202.ics_202_router import router as ics_202_router
from src.infrastructure.api.ics_203.ics_203_router import router as ics_203_router
from src.infrastructure.api.ics_204.ics_204_router import router as ics_204_router
from src.infrastructure.api.ics_205.ics_205_router import router as ics_205_router
from src.infrastructure.api.ics_206.ics_206_router import router as ics_206_router
from src.infrastructure.api.ics_207.ics_207_router import router as ics_207_router
from src.infrastructure.api.ics_208.ics_208_router import router as ics_208_router
from src.infrastructure.api.ics_209.ics_209_router import router as ics_209_router
from src.infrastructure.api.imt_members.finance_section.finance_router import \
    router as finance_section_router
from src.infrastructure.api.imt_members.logistic_section.logistic_router import \
    router as logistic_section_router
from src.infrastructure.api.imt_members.main_section.main_router import \
    router as main_section_router
from src.infrastructure.api.imt_members.planning_section.planning_router import \
    router as planning_section_router
from src.infrastructure.api.operational_period import router as operational_period_router
from src.infrastructure.api.roster import router as roster_router
from src.infrastructure.api.roster_table import router as roster_table_router
from src.infrastructure.api.upload import router as upload_router

routers = [
    (main_section_router, "/main-section", ["IMT Members: Main Section"]),
    (planning_section_router, "/planning-section", ["IMT Members: Planning Section"]),
    (logistic_section_router, "/logistic-section", ["IMT Members: Logistic Section"]),
    (finance_section_router, "/finance-section", ["IMT Members: Finance Section"]),
    (roster_router, "/roster", ["IMT Roster"]),
    (roster_table_router, "/roster-table", ["IMT Table"]),
    (incident_data_router, "/incident-data", ["Incident Data"]),
    (operational_period_router, "/operational-period", ["Operational Period"]),
    (upload_router, "/upload", ["Upload"]),
    (ics_201_router, "/ics-201", ["ICS 201"]),
    (ics_202_router, "/ics-202", ["ICS 202"]),
    (ics_203_router, "/ics-203", ["ICS 203"]),
    (ics_204_router, "/ics-204", ["ICS 204"]),
    (ics_205_router, "/ics-205", ["ICS 205"]),
    (ics_206_router, "/ics-206", ["ICS 206"]),
    (ics_207_router, "/ics-207", ["ICS 207"]),
    (ics_208_router, "/ics-208", ["ICS 208"]),
    (ics_209_router, "/ics-209", ["ICS 209"]),
]

def configure_routers(app: FastAPI):
    for router, prefix, tags in routers:
        app.include_router(router, prefix=prefix, tags=tags)

