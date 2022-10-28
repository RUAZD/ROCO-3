from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.database import DataBase
from app.exceptions import CommonException
from app.forms import routers

app = FastAPI(title='ROCO "Цифра" кейс 3')


@app.on_event('startup')
async def startup() -> None:
    await DataBase.connect_db()


@app.on_event('shutdown')
async def shutdown() -> None:
    await DataBase.disconnect_db()


@app.exception_handler(CommonException)
async def handler_badrequest(requests: Request, exception: CommonException) -> JSONResponse:
    return JSONResponse(status_code=exception.code, content=dict(details=exception.message))


for router in routers:
    app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
