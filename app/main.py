from fastapi import FastAPI
from app.routers import tasks
from app.models import Base
from app.database import async_engine

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
