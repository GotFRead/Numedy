from fastapi import FastAPI
from server.routes import *

import uvicorn
import asyncio

loop = asyncio.get_event_loop()


# __web_server__
app = FastAPI()

app.include_router(router)


def run_server():
    uvicorn.run(f'server:app', host="0.0.0.0", port=8000,
                reload=False, loop='asyncio')




