from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.engine import async_session_factory
from db.sqhemas.orm.staff import CallOrm, BrigadesOrm, CompositionsBrigadesOrm


async def get_calls():
    async with async_session_factory() as session:
        query = (
            select(CallOrm)
            .options(selectinload(CallOrm.status_rel))
        )
        result = (await session.execute(query)).scalars().all()
        return result


async def get_brigades():
    async with async_session_factory() as session:
        query = (
            select(BrigadesOrm)
            .join(BrigadesOrm.composition_rel, isouter=True)
            .options(
                selectinload(BrigadesOrm.car_rel),
                selectinload(BrigadesOrm.composition_rel)
                .contains_eager(CompositionsBrigadesOrm.nurse_rel),
                selectinload(BrigadesOrm.composition_rel)
                .contains_eager(CompositionsBrigadesOrm.driver_rel),
                selectinload(BrigadesOrm.composition_rel)
                .contains_eager(CompositionsBrigadesOrm.orderly_rel),
                selectinload(BrigadesOrm.composition_rel)
                .contains_eager(CompositionsBrigadesOrm.paramedic_rel)
            )
        )
        result = (await session.execute(query)).scalars().all()
        return result