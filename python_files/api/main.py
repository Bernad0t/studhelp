from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from db.queryes.students import get_students

app = FastAPI(
    title="My App",
    description="Description of my app.",
    version="1.0",
    docs_url='/docs',
    openapi_url='/openapi.json',
    redoc_url=None
)

origins = ["http://localhost:3000", "http://localhost:3001"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    print("start")


@app.get("/")
async def get_students_router(page: int, per_page: int):
    return await get_students(page, per_page)
