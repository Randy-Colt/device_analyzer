from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from api import api_router
from core.settings import Base, helper
from core.settings.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(debug=settings.debug, lifespan=lifespan)
app.include_router(api_router, prefix='/api/devices')


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, host='0.0.0.0')
