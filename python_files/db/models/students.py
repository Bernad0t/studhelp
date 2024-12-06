from sqlalchemy.orm import Mapped, mapped_column

from db.engine import Base


class StudentsOrm(Base):
    __tablename__ = "Students"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    last_name: Mapped[str]
    name: Mapped[str]
    fatherland: Mapped[str]
    grade: Mapped[int]
    group: Mapped[str]
    institute: Mapped[str]