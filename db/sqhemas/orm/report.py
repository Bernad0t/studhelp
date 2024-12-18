from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from db.engine import Base
from db.sqhemas.enums.workload import Workload


class ReportOrm(Base):
    __tablename__ = "report"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date_created: Mapped[datetime]
    time_reaction: Mapped[str]
    workload: Mapped[Workload]