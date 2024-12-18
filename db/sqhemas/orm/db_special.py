from sqlalchemy import LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from db.engine import Base


class MainLog(Base):
    __tablename__ = 'main_log'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    operation_type: Mapped[str]
    user_operator: Mapped[str]
    changed_data: Mapped[str]

class SecretData(Base):
    __tablename__ = 'secret_data'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login: Mapped[str]
    access_token: Mapped[str] = mapped_column(LargeBinary)