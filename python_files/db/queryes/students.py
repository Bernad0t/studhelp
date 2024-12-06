import asyncio
import json
from pydantic import BaseModel

from sqlalchemy import select, delete, func

from db.engine import async_session_factory
from db.models.students import StudentsOrm

students = [
{"last_name": "Тху", "name": "Чинь", "fatherland": "Хоай", "grade": 3, "group": "5030102/20202", "institute": "Физмех"},
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

async def get_students(page: int, per_page: int):
    async with async_session_factory() as session:
        offset_value = (page - 1) * per_page
        number_rows = (
            select(func.count(StudentsOrm.id))
        )
        students = (
            select(StudentsOrm)
            .limit(per_page)
            .offset(offset_value)
        )
        res = (await session.execute(students)).scalars().all()
        number_rows = (await session.execute(number_rows)).scalars().first()
        return json.dumps({"number_students": number_rows, "students":
            [StudentsDTO.model_validate(i, from_attributes=True).model_dump() for i in res]})


async def set_students():
    async with async_session_factory() as session:
        query = (
            delete(StudentsOrm)
        )
        await session.execute(query)
        for i in students:
            session.add(StudentsOrm(**i))
        await session.commit()

if __name__ == "__main__":
    asyncio.run(set_students())