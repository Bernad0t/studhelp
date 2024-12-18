from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.engine import async_session_factory
from db.sqhemas.orm.report import ReportOrm
from db.sqhemas.orm.staff import CallOrm, BrigadesOrm


async def get_tasks():
    async with async_session_factory() as session:
        query = (
            select(CallOrm)
            .options(selectinload(CallOrm.status_rel))
        )
        result = (await session.execute(query)).scalars().all()
        return result

async def get_reports():
    async with async_session_factory() as session:
        query = (
            select(ReportOrm)
        )
        result = (await session.execute(query)).scalars().all()
        return result