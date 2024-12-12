import asyncio
import json
from pydantic import BaseModel

from sqlalchemy import select, delete, func, and_, update

from db.engine import async_session_factory
from db.models.students import StudentsOrm

students = [
{"last_name": "Доан", "name": "Тхи", "fatherland": "Хоай Тхыон", "grade": 3, "group": "5030102/20202", "institute": "Физмех"},
{"last_name": "Тишковец", "name": "Сергей", "fatherland": "Евгеньевич", "grade": 3, "group": "5030102/20202", "institute": "Физмех"},
{"last_name": "Ткачев", "name": "Михаил", "fatherland": "Алексеевич", "grade": 3, "group": "5030102/20202", "institute": "ИКНТ"},
{"last_name": "Дрекалов", "name": "Никита", "fatherland": "Сергеевич", "grade": 3, "group": "5030102/20202", "institute": "Физмех"},
{"last_name": "Фролов", "name": "Иван", "fatherland": "Максимович", "grade": 3, "group": "5030102/20202", "institute": "Физмех"},
{"last_name": "Перцев", "name": "Дмитрий", "fatherland": "Михайлович", "grade": 3, "group": "5030102/20202", "institute": "Физмех"},
{"last_name": "Диденко", "name": "Евгений", "fatherland": "Павлович", "grade": 3, "group": "5030102/20202", "institute": "Физмех"},
{"last_name": "Соколов", "name": "Артем", "fatherland": "Иванович", "grade": 3, "group": "5030102/20202", "institute": "ИЭ"},
{"last_name": "Иванов", "name": "Иван", "fatherland": "Иванович", "grade": 3, "group": "5030102/20202", "institute": "Физмех"},
{"last_name": "Попов", "name": "Алексей", "fatherland": "Нахатович", "grade": 3, "group": "5030102/20202", "institute": "Физмех"},
{"last_name": "Брусилов", "name": "Алексей", "fatherland": "Михайлович", "grade": 3, "group": "5030102/20202", "institute": "Физмех"},
{"last_name": "Ягода", "name": "Михаил", "fatherland": "Алексеевич", "grade": 3, "group": "5030102/20202", "institute": "Физмех"},
{"last_name": "Ульянов", "name": "Владимир", "fatherland": "Михайлович", "grade": 3, "group": "5030102/20202", "institute": "ИКНК"},
{"last_name": "Соколова", "name": "Татьяна", "fatherland": "Сергеевна", "grade": 3, "group": "5030102/20202", "institute": "Физмех"},
{"last_name": "Ситникова", "name": "Мария", "fatherland": "Алексеевна", "grade": 3, "group": "5030102/20202", "institute": "Физмех"},
{"last_name": "Моор", "name": "Мария", "fatherland": "Максимовна", "grade": 3, "group": "5030102/20202", "institute": "ИЭИТ"},
]

class StudentsDTO(BaseModel):
    id: int
    last_name: str
    name: str
    fatherland: str
    grade: int
    group: str
    institute: str

async def get_students(page: int, per_page: int, search_template: dict, order_by: str):
    conditions = [
        getattr(StudentsOrm, key).like(f"%{value}%")
        for key, value in search_template.items()
        if value is not None and key != "grade"
    ]
    async with async_session_factory() as session:
        offset_value = (page - 1) * per_page
        number_rows = (
            select(func.count(StudentsOrm.id))
            .where(and_(*conditions))
        )
        query = select(StudentsOrm).where(and_(*conditions))

        if "grade" in search_template.keys() and isinstance(search_template["grade"], int):
            query = query.filter(StudentsOrm.grade == int(search_template["grade"]))
        if order_by and len(order_by) > 0:  # Добавляем сортировку только если передан параметр
            query = query.order_by(order_by)

        students = query.limit(per_page).offset(offset_value)
        res = (await session.execute(students)).scalars().all()
        number_rows = (await session.execute(number_rows)).scalars().first()
        return {"number_students": number_rows, "students": res}


async def set_student(data: dict):
    async with async_session_factory() as session:
        session.add(StudentsOrm(**data))
        await session.commit()


async def set_students():
    async with async_session_factory() as session:
        query = (
            delete(StudentsOrm)
        )
        await session.execute(query)
        for i in students:
            session.add(StudentsOrm(**i))
        await session.commit()


async def delete_student(id):
    async with async_session_factory() as session:
        query = (
            delete(StudentsOrm)
            .where(StudentsOrm.id == id)
        )
        await session.execute(query)
        await session.commit()


async def update_student(data: dict):
    async with async_session_factory() as session:
        query = (
            update(StudentsOrm)
            .where(StudentsOrm.id == data["id"])
            .values(data)
        )
        await session.execute(query)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(set_students())