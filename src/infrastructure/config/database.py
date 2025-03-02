import os
import logging

from decouple import config
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# from src.core.entities.ics_201_models import (ActionsStrategiesTactics, Ics201, IcsChart,
#                                 ResourceSummary)
# from src.core.entities.incident_data import IncidentData, OperationalPeriod
# from src.core.entities.roster import ImtRoster

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load database URL from .env
DATABASE_URL = config("DATABASE_URL")
print("Database URL:",DATABASE_URL)

# Create an asynchronous SQLAlchemy engine for PostgreSQL
engine = create_async_engine(DATABASE_URL, echo=False)

# Create a session factory for querying the DB
async_session_factory = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


# Asynchronous function to get database session
async def get_session():
    try:
        async with async_session_factory() as session:
            yield session
    except Exception as e:
        logger.error(f"Error getting session: {e}")
        raise


# Function to drop tables
async def drop_table():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)
            # await conn.run_sync(ResourceSummary.__table__.drop)
            # await conn.run_sync(ActionsStrategiesTactics.__table__.drop)
            # await conn.run_sync(IcsChart.__table__.drop)
            # await conn.run_sync(Ics201.__table__.drop)
        logger.info("Tables have been dropped successfully.")
    except Exception as e:
        logger.error(f"Error dropping tables: {e}")
        raise


# Function to create all tables based on the model
async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("Tables have been created successfully.")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise
