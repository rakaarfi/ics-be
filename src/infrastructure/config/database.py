import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# from src.core.entities.ics_201_models import (ActionsStrategiesTactics, Ics201, IcsChart,
#                                 ResourceSummary)
# from src.core.entities.incident_data import IncidentData, OperationalPeriod
# from src.core.entities.roster import ImtRoster

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
        await conn.run_sync(SQLModel.metadata.drop_all)
        # await conn.run_sync(ResourceSummary.__table__.drop)
        # await conn.run_sync(ActionsStrategiesTactics.__table__.drop)
        # await conn.run_sync(IcsChart.__table__.drop)
        # await conn.run_sync(Ics201.__table__.drop)
    print("Tables have been dropped.")


# Function to create all tables based on the model
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Tables have been created.")
