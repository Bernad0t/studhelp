from pydantic import BaseModel

from db.sqhemas.enums.qualification import Qualification
from db.sqhemas.enums.role import Role


class UserLogin(BaseModel):
    login: str
    password: str

class UserData(BaseModel):
    role: Role
    name: str
    qualification: Qualification | None = None
class UserCreate(UserLogin, UserData):
    pass