from contextlib import asynccontextmanager
from fastapi import FastAPI
from models import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("START")
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    print("SHUTDOWN")