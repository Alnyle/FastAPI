from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from config import db_settings

# create_async_engine: Creates an asynchronous connection to PostgreSQL.
# Instead of blocking your server while waiting for the database other requests can still run.

engine = create_async_engine(
    url=db_settings.POSTGRES_URL,
    echo=True, # I want to print the exceted sql query on the terminal
)



async def create_db_tables():
    async with engine.begin() as connection:
        from api.schemas.shipment import Shipment
        # from database.models import Seller
        await connection.run_sync(SQLModel.metadata.create_all)
        

# AsyncSession is a special class that allows you to interact with the database asynchronously.
# Represents one conversation with the database 

# A sessionmaker is a factory:
    # Instead of manually creating sessions,

    # Session 1
    # Session 2
    # Session 3

    # the factory creates them whenever needed.

async def get_session():

    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session
        
# Instead of writing
    # session: AsyncSession = Depends(get_session)        
    # Depends tells FastAPI: "Before calling this endpoint, execute another function and give me its result."
SessionDep = Annotated[AsyncSession, Depends(get_session)]
