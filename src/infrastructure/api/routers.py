from fastapi import FastAPI

from src.infrastructure.api.incident_data import router as incident_data_router
from src.infrastructure.api.ics_201.ics_201_router import router as ics_201_router
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
]

def configure_routers(app: FastAPI):
    for router, prefix, tags in routers:
        print(f"Router: {router}, Prefix: {prefix}, Tags: {tags}")
        app.include_router(router, prefix=prefix, tags=tags)

