from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.engine import Base
from db.sqhemas.enums.status_car import StatusCar
from db.sqhemas.orm.user import UsersOrm


class CallOrm(Base):
    __tablename__ = "call"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    time_call: Mapped[datetime]
    type: Mapped[str]
    status_id: Mapped[int] = mapped_column(ForeignKey("statuscall.id", ondelete="SET NULL"), nullable=True)
    dispatcher_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    brigade_id: Mapped[int] = mapped_column(ForeignKey("brigades.id", ondelete="SET NULL"), nullable=True)

    status_rel: Mapped["StatusCallOrm"] = relationship()
    brigade_rel: Mapped["BrigadesOrm"] = relationship()


class StatusCallOrm(Base):
    __tablename__ = "statuscall"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str]

class CarsOrm(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[StatusCar]
    location: Mapped[str]
    brigade_id: Mapped[int] = mapped_column(ForeignKey("brigades.id", ondelete="SET NULL"), nullable=True)

    brigade_rel: Mapped["BrigadesOrm"] = relationship(
        back_populates="car_rel"
    )


class BrigadesOrm(Base):
    __tablename__ = "brigades"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    composition_id: Mapped[int] = mapped_column(ForeignKey("compositionsbrigades.id", ondelete="CASCADE"))

    composition_rel: Mapped["CompositionsBrigadesOrm"] = relationship()
    car_rel: Mapped["CarsOrm"] = relationship(
        back_populates="brigade_rel"
    )

class CompositionsBrigadesOrm(Base):
    __tablename__ = "compositionsbrigades"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    driver: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    paramedic: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    nurse: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    orderly: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    driver_rel: Mapped["UsersOrm"] = relationship("UsersOrm", foreign_keys=[driver])
    paramedic_rel: Mapped["UsersOrm"] = relationship("UsersOrm", foreign_keys=[paramedic])
    nurse_rel: Mapped["UsersOrm"] = relationship("UsersOrm", foreign_keys=[nurse])
    orderly_rel: Mapped["UsersOrm"] = relationship("UsersOrm", foreign_keys=[orderly])