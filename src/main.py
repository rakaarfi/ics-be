import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from src.infrastructure.config.database import drop_table, init_db
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
from src.infrastructure.api.exception_handlers import (
    custom_http_exception_handler,
    validation_exception_handler,
    not_found_exception_handler,
    bad_request_exception_handler,
    unauthorized_exception_handler,
    forbidden_exception_handler,
    internal_server_error_handler,
)
from src.core.exceptions import (
    CustomHTTPException,
    NotFoundException,
    BadRequestException,
    UnauthorizedException,
    ForbiddenException,
)


app = FastAPI()

# Configurate CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://172.28.49.140:3000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurate logging
logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Set SQLAlchemy log level to WARNING
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


# Run the database setup on startup
@app.on_event("startup")
async def on_startup():
    # await drop_table()  # Uncomment this line if you want to drop the table when starting up
    await init_db()


# Add router to FastAPI
app.include_router(
    main_section_router, prefix="/main-section", tags=["IMT Members: Main Section"]
)
app.include_router(
    planning_section_router,
    prefix="/planning-section",
    tags=["IMT Members: Planning Section"],
)
app.include_router(
    logistic_section_router,
    prefix="/logistic-section",
    tags=["IMT Members: Logistic Section"],
)
app.include_router(
    finance_section_router,
    prefix="/finance-section",
    tags=["IMT Members: Finance Section"],
)
app.include_router(roster_router, prefix="/roster", tags=["IMT Roster"])
app.include_router(roster_table_router, prefix="/roster-table", tags=["IMT Table"])
app.include_router(
    incident_data_router, prefix="/incident-data", tags=["Incident Data"]
)
app.include_router(
    operational_period_router, prefix="/operational-period", tags=["Operational Period"]
)
app.include_router(upload_router, prefix="/upload", tags=["Upload"])
app.include_router(ics_201_router, prefix="/ics-201", tags=["ICS 201"])


# Add exception handlers
app.add_exception_handler(CustomHTTPException, custom_http_exception_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(BadRequestException, bad_request_exception_handler)
app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)
app.add_exception_handler(ForbiddenException, forbidden_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, internal_server_error_handler)