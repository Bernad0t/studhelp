from typing import Annotated

from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import Response

from config import EXPIRE_ACCESS_TOKEN
from db.queryes.authorization import Register, Login
from db.queryes.dispatcher import get_calls, get_brigades
from db.queryes.med_stuff import get_tasks, get_reports
from db.queryes.startup import startup
from db.sqhemas.dto.report import ReportsDTO
from db.sqhemas.dto.staff import CallsDispatcher, CallsMedStuffDTO, BrigadesDTO
from db.sqhemas.dto.user import UserCreate, UserLogin
from utils.token_process import verify_token

app = FastAPI(
    title="My App",
    description="Description of my app.",
    version="1.0",
    docs_url='/docs',
    openapi_url='/openapi.json',
    redoc_url=None
)

origins = ["http://localhost:3000", "http://localhost:8080", "http://localhost:3001"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_token_from_cookie(request: Request) -> str:
    token = request.cookies.get("access_token")  # Извлекаем токен из куки
    if not token:
        raise HTTPException(status_code=401, detail="Token not found in cookies")
    return token

@app.on_event("startup")
async def startup_router():
    # await startup()
    pass

@app.get("/get-calls-dispatcher")
async def get_calls_dispatcher_router(token: str = Depends(get_token_from_cookie)):
    try:
        calls = await get_calls()
    except:
        return []
    return [CallsDispatcher.model_validate(i, from_attributes=True) for i in calls]


@app.get("/get-tasks-med")
async def get_tasks_med_router(token: str = Depends(get_token_from_cookie)):
    try:
        calls = await get_tasks()
    except:
        return []
    return [CallsMedStuffDTO.model_validate(i, from_attributes=True) for i in calls]


@app.get("/get-brigades")
async def get_brigades_router(token: str = Depends(get_token_from_cookie)):
    try:
        calls = await get_brigades()
    except:
        return []
    return [BrigadesDTO.model_validate(i, from_attributes=True) for i in calls]


@app.get("/get-reports")
async def get_reports_router(token: str = Depends(get_token_from_cookie)):
    try:
        calls = await get_reports()
    except:
        return []
    return [ReportsDTO.model_validate(i, from_attributes=True) for i in calls]


@app.post("/sign-up")
async def create_user(user: UserCreate, response: Response):
    dict_tokens = await Register(user)
    response.set_cookie(
        key="access_token",
        value=dict_tokens["access_token"],
        max_age=EXPIRE_ACCESS_TOKEN,  # Время жизни куки в секундах (например, 1 час)
        secure=False,  # Доступ только по HTTPS
        httponly=True,  # Запрещён доступ через JavaScript
    )

@app.post("/sign-in")
async def login_user(user: UserLogin, response: Response):
    dict_tokens = await Login(user)
    response.set_cookie(
        key="access_token",
        value=dict_tokens["access_token"],
        max_age=EXPIRE_ACCESS_TOKEN,  # Время жизни куки в секундах (например, 1 час)
        secure=False,  # Доступ только по HTTPS
        httponly=True,  # Запрещён доступ через JavaScript
    )