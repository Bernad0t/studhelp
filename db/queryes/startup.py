import asyncio
from datetime import datetime

from sqlalchemy import delete, text
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from db.engine import async_session_factory, Base, async_engine
from db.sqhemas.enums.qualification import Qualification
from db.sqhemas.enums.role import Role
from db.sqhemas.enums.status_car import StatusCar
from db.sqhemas.enums.workload import Workload
from db.sqhemas.orm.report import ReportOrm
from db.sqhemas.orm.staff import CallOrm, CompositionsBrigadesOrm, CarsOrm, BrigadesOrm, StatusCallOrm
from db.sqhemas.orm.user import UsersOrm
from utils.password_process import get_hashed_password

dispatchers = [
    {"name": 'Иванов Иван', "login": 'ivanov', "password": 'password123', "role": Role.dispatcher},
    {"name": 'Петров Петр', "login": 'petrov', "password": 'password124', "role": Role.dispatcher},
    {"name": 'Сидоров Сидор', "login": 'sidrov', "password": 'password125', "role": Role.dispatcher},
    {"name": 'Кузнецов Николай', "login": 'kuz', "password": 'password126', "role": Role.dispatcher},
]

users = [
    {
        "login": "doctor_anna",
        "password": "anna_pass",
        "name": "Анна Иванова",
        "role": Role.medic,
        "qualification": Qualification.primary,
    },
    {
        "login": "medic_john",
        "password": "john_pass",
        "name": "Джон Смит",
        "role": Role.medic,
        "qualification": Qualification.med,
    },
    {
        "login": "med_worker",
        "password": "worker_pass",
        "name": "Иван Петров",
        "role": Role.medic,
        "qualification": Qualification.first,
    },
    {
        "login": "healthcare_nina",
        "password": "nina_pass",
        "name": "Нина Сидорова",
        "role": Role.medic,
        "qualification": None,  # Указание, если квалификация неизвестна
    },
]

compositions_brigades = [
    {
        "driver": 1,
        "paramedic": 2,
        "nurse": 3,
        "orderly": 4,
    },
    {
        "driver": 2,
        "paramedic": 3,
        "nurse": 4,
        "orderly": 1,
    },
    {
        "driver": 3,
        "paramedic": 4,
        "nurse": 1,
        "orderly": 2,
    },
    {
        "driver": 4,
        "paramedic": 1,
        "nurse": 2,
        "orderly": 3,
    },
]

calls = [
    {
        "time_call": datetime(2023, 12, 1, 10, 30),
        "type": "emergency",
        "status_id": 1,
        "dispatcher_id": 1,
        "brigade_id": 1,
    },
    {
        "time_call": datetime(2023, 12, 1, 11, 0),
        "type": "urgent",
        "status_id": 2,
        "dispatcher_id": 2,
        "brigade_id": 2,
    },
    {
        "time_call": datetime(2023, 12, 2, 14, 15),
        "type": "non-urgent",
        "status_id": 3,
        "dispatcher_id": 3,
        "brigade_id": 3,
    },
    {
        "time_call": datetime(2023, 12, 2, 16, 45),
        "type": "scheduled",
        "status_id": 1,
        "dispatcher_id": 4,
        "brigade_id": 4,
    },
]

# Status Calls
status_calls = [
    {"description": "Waiting for Assignment"},
    {"description": "Assigned to Brigade"},
    {"description": "In Progress"},
    {"description": "Completed"},
]

# Cars
cars = [
    {
        "status": StatusCar.free,
        "location": "Garage 1",
        "brigade_id": 1,
    },
    {
        "status": StatusCar.busy,
        "location": "On Call",
        "brigade_id": 2,
    },
    {
        "status": StatusCar.repair,
        "location": "Service Center",
        "brigade_id": 3,
    },
    {
        "status": StatusCar.free,
        "location": "Garage 2",
        "brigade_id": 4,
    },
]

# Brigades
brigades = [
    {
        "composition_id": 1,
    },
    {
        "composition_id": 2,
    },
    {
        "composition_id": 3,
    },
    {
        "composition_id": 4,
    },
]

reports = [
    {
        "date_created": datetime(2023, 12, 1, 10, 0),
        "time_reaction": "5 минут",
        "workload": Workload.low,
    },
    {
        "date_created": datetime(2023, 12, 2, 14, 30),
        "time_reaction": "10 минут",
        "workload": Workload.med,
    },
    {
        "date_created": datetime(2023, 12, 3, 9, 45),
        "time_reaction": "15 минут",
        "workload": Workload.high,
    },
    {
        "date_created": datetime(2023, 12, 4, 16, 20),
        "time_reaction": "7 минут",
        "workload": Workload.med,
    },
]


async def delete_all_records():
    async with async_session_factory() as session:
        # Получаем список всех таблиц из метаданных
        tables = Base.metadata.sorted_tables
        # Сначала удаляем таблицы, которые имеют связи с дочерними таблицами
        await session.execute(delete(CallOrm))  # Удаляем записи из таблицы call
        await session.execute(delete(UsersOrm))  # Удаляем записи из таблицы users
        await session.execute(delete(BrigadesOrm))  # Удаляем записи из таблицы brigades
        await session.execute(delete(StatusCallOrm))  # Удаляем записи из таблицы statuscall
        # Удаляем все записи из всех таблиц
        for table in tables:
            if table.name != "main_log":
                await session.execute(delete(table))

        await session.commit()

async def startup():
    await delete_all_records()
    async with async_engine.connect() as connection:
        await connection.execution_options(isolation_level="AUTOCOMMIT")
        await connection.execute(text("VACUUM"))
        tables = Base.metadata.sorted_tables

        # Удаляем все записи из всех таблиц
        for table in tables:
            if table.name == "main_log":
                continue
            column = table.columns[0]
            sequence_name = f"{table.name}_{column.name}_seq"
            await connection.execute(text(f"ALTER SEQUENCE {sequence_name} RESTART WITH 1;"))
    async with async_session_factory() as session:
        for user in users:
            new_user = UsersOrm(**{**user, "password": get_hashed_password(user["password"])})
            session.add(new_user)

        for user in dispatchers:
            new_user = UsersOrm(**{**user, "password": get_hashed_password(user["password"])})
            session.add(new_user)

        for status_call in status_calls:
            new_status_call = StatusCallOrm(**status_call)
            session.add(new_status_call)

            # Adding compositions_brigades data
        for composition in compositions_brigades:
            new_composition = CompositionsBrigadesOrm(**composition)
            session.add(new_composition)

            # Adding brigades data
        for brigade in brigades:
            new_brigade = BrigadesOrm(**brigade)
            session.add(new_brigade)

            # Adding cars data
        for car in cars:
            new_car = CarsOrm(**car)
            session.add(new_car)

            # Adding calls data
        for call in calls:
            new_call = CallOrm(**call)
            session.add(new_call)

        for report_data in reports:
            new_report = ReportOrm(**report_data)
            session.add(new_report)

        await session.commit()

if __name__ == "__main__":
    asyncio.run(startup())