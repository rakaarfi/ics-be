# import logging
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from app.config.database import init_db, drop_table
# from app.routes.imt_members.main_section.main_router import router as main_section_router
# from app.routes.imt_members.planning_section.planning_router import router as planning_section_router
# from app.routes.imt_members.logistic_section.logistic_router import router as logistic_section_router
# from app.routes.imt_members.finance_section.finance_router import router as finance_section_router
# from app.routes.roster import router as roster_router
# from app.routes.roster_table import router as roster_table_router
# from app.routes.incident_data import router as incident_data_router
# from app.routes.operational_period import router as operational_period_router


# app = FastAPI()

# origins = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
#     "*"
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Konfigurasi logging
# logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(levelname)s - %(message)s")

# # Atur SQLAlchemy ke tingkat WARNING
# logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

# # Menjalankan setup database pada startup
# @app.on_event("startup")
# def on_startup():
#     # drop_table()
#     init_db()

# # Menambahkan router ke aplikasi FastAPI
# app.include_router(main_section_router, prefix="/main-section", tags=["IMT Members: Main Section"])
# app.include_router(planning_section_router, prefix="/planning-section", tags=["IMT Members: Planning Section"])
# app.include_router(logistic_section_router, prefix="/logistic-section", tags=["IMT Members: Logistic Section"])
# app.include_router(finance_section_router, prefix="/finance-section", tags=["IMT Members: Finance Section"])
# app.include_router(roster_router, prefix="/roster", tags=["IMT Roster"])
# app.include_router(roster_table_router, prefix="/roster-table", tags=["IMT Table"])
# app.include_router(incident_data_router, prefix="/incident-data", tags=["Incident Data"])
# app.include_router(operational_period_router, prefix="/operational-period", tags=["Operational Period"])


import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import drop_table, init_db
from app.routes.ics_201.export_docx import router as export_docx
from app.routes.ics_201.ics_201_router import router as ics_201_router
from app.routes.imt_members.finance_section.finance_router import \
    router as finance_section_router
from app.routes.imt_members.logistic_section.logistic_router import \
    router as logistic_section_router
from app.routes.imt_members.main_section.main_router import \
    router as main_section_router
from app.routes.imt_members.planning_section.planning_router import \
    router as planning_section_router
from app.routes.incident_data import router as incident_data_router
from app.routes.operational_period import router as operational_period_router
from app.routes.roster import router as roster_router
from app.routes.roster_table import router as roster_table_router
from app.routes.upload import router as upload_router

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
app.include_router(export_docx, prefix="/export-docx", tags=["Export Docx"])
