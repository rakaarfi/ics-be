# from sqlmodel import create_engine, SQLModel, Session
# from sqlalchemy.orm import sessionmaker
# from app.models.roster import ImtRoster
# from app.models.incident_data import IncidentData, OperationalPeriod
# import os

# # URL PostgreSQL connection string
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://rakaarfi:qwertyuiop@172.28.49.140:5432/ics_database")

# # Membuat engine SQLAlchemy untuk PostgreSQL
# engine = create_engine(DATABASE_URL, echo=False)

# # Membuat session factory untuk melakukan query ke DB
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Fungsi untuk menghapus tabel
# def drop_table():
#     # SQLModel.metadata.drop_all(bind=engine)
#     # ImtRoster.__table__.drop(bind=engine)
#     IncidentData.__table__.drop(bind=engine)
#     # OperationalPeriod.__table__.drop(bind=engine)
#     print("Tabel telah dihapus.")

# # Fungsi untuk membuat sesi database
# def get_session():
#     with SessionLocal() as session:
#         yield session
#     # with Session(engine) as session:
#     #     yield session

# # Fungsi untuk membuat semua tabel berdasarkan model
# def init_db():
#     SQLModel.metadata.create_all(bind=engine)

import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.models.ics_201_models import (ActionsStrategiesTactics, Ics201, IcsChart,
                                ResourceSummary)
# from app.models.incident_data import IncidentData, OperationalPeriod
# from app.models.roster import ImtRoster

# PostgreSQL connection string URL (use an async driver like asyncpg)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://rakaarfi:qwertyuiop@172.28.49.140:5432/ics_database",
)

# Create an asynchronous SQLAlchemy engine for PostgreSQL
engine = create_async_engine(DATABASE_URL, echo=False)

# Create a session factory for querying the DB
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


# Asynchronous function to get database session
async def get_session():
    async with async_session_factory() as session:
        yield session


# Function to drop tables
async def drop_table():
    async with engine.begin() as conn:
        #     await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(ResourceSummary.__table__.drop)
        await conn.run_sync(ActionsStrategiesTactics.__table__.drop)
        await conn.run_sync(IcsChart.__table__.drop)
        await conn.run_sync(Ics201.__table__.drop)
    print("Tables have been dropped.")


# Function to create all tables based on the model
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Tables have been created.")
