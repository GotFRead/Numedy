from fastapi import FastAPI

from server.routes import router as base_router
from server.users.routes import router as user_router


import uvicorn
import asyncio

loop = asyncio.get_event_loop()


# __web_server__
app = FastAPI()

app.include_router(user_router)
app.include_router(base_router)



def run_server():
    uvicorn.run(f'main:app', host="0.0.0.0", port=8000,
                reload=False, loop='asyncio')


if __name__ == '__main__': 
    run_server()


