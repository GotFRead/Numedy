from fastapi import FastAPI

from server.routes import router as base_router
from server.users.routes import router as user_router
from server.warehouse.routes import router as product_router
from models.base import Base
from models.product import Product
from models.db_helper import DataBaseHelper
from models.db_helper import db_helper


from contextlib import asynccontextmanager

import uvicorn
import asyncio

loop = asyncio.get_event_loop()

# __lifespan__

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        

    yield


# __web_server__
app = FastAPI(lifespan=lifespan, debug=True)

app.include_router(user_router)
app.include_router(base_router)
app.include_router(product_router)

def run_server():
    uvicorn.run(f'main:app', host="0.0.0.0", port=8000, loop='asyncio')


if __name__ == '__main__': 
    run_server()


