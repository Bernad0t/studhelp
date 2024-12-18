from sqlalchemy import ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.engine import Base
from db.sqhemas.enums.qualification import Qualification
from db.sqhemas.enums.role import Role


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login: Mapped[str]
    password: Mapped[bytes] = mapped_column(LargeBinary)
    name: Mapped[str]
    role: Mapped[Role]
    qualification: Mapped[Qualification | None]