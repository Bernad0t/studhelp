import json

from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from db.queryes.students import get_students, StudentsDTO, set_student, delete_student, update_student

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
async def get_students_router(page: int, per_page: int, search_template: str, order_by: str):
    result = await get_students(page, per_page, json.loads(search_template), order_by)
    # if len(order_by) != 0:
    #     result["students"].sort(key=lambda student: getattr(student, order_by))
    return json.dumps({"number_students": result["number_students"], "students":
            [StudentsDTO.model_validate(i, from_attributes=True).model_dump() for i in result["students"]]})


@app.post("/set-student")
async def set_student_router(data: str):
    data = json.loads(data)
    await set_student(data)


@app.delete("/delete-student")
async def delete_student_router(id: int):
    await delete_student(id)

@app.patch("/update-student")
async def update_student_router(data: str):
    data = json.loads(data)
    await update_student(data)
