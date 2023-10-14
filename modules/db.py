from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from databases import Database

DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@localhost/mydatabase"
database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_async_engine(DATABASE_URL, echo=True)
async_engine = create_async_engine(DATABASE_URL)


def get_session():
    return AsyncSession(bind=engine, expire_on_commit=False)


def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()
