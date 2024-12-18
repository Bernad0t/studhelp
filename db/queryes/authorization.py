from sqlalchemy import select, update

from db.engine import async_session_factory
from db.exception.authorization import USER_EXIST, USER_DONT_EXIST, UNCORRECT_DATA
from db.sqhemas.dto.user import UserCreate, UserLogin
from db.sqhemas.orm.db_special import SecretData
from db.sqhemas.orm.user import UsersOrm
from services.user import authorization_service
from utils.password_process import get_hashed_password, check_password
from utils.token_process import create_access_token
from cryptography.fernet import Fernet

# Генерация ключа: обычно следует выполнять один раз и хранить его в безопасном месте
key = Fernet.generate_key()
cipher = Fernet(key)


async def find_user_by_login(login: str) -> UsersOrm:
    async with async_session_factory() as session:
        query = (
            select(UsersOrm)
            .where(UsersOrm.login == login)
        )
        result = await session.execute(query)
        return result.scalars().first()


@authorization_service
async def Register(data: UserCreate):
    async with async_session_factory() as session:
        result = await find_user_by_login(data.login)
        if result:
            raise USER_EXIST
        hashed_password = get_hashed_password(data.password)
        data.password = hashed_password
        new_user = UsersOrm(**data.dict())
        session.add(new_user)
        await session.flush()
        dict_for_token = {'id': new_user.id, "role": data.role.value}
        access_token = create_access_token(dict_for_token)
        new_secret_data = SecretData(login=data.login, access_token=cipher.encrypt(b'access_token'))
        # session.add(new_secret_data) #  если прав недостаточно то ошибка
        await session.commit()
        return {"access_token": access_token}


@authorization_service
async def Login(data: UserLogin):
    async with async_session_factory() as session:
        result = await find_user_by_login(data.login)
        if not result:
            raise USER_DONT_EXIST
        if not check_password(data.password, result.password):
            raise UNCORRECT_DATA
        dict_for_token = {'id': result.id, "role": result.role.value}
        access_token = create_access_token(dict_for_token)
        query = (
            update(SecretData)
            .where(SecretData.login == data.login)
            .values(access_token=cipher.encrypt(b'access_token'))
        )
        # await session.execute(query) #  если прав недостаточно то ошибка
        return {"access_token": access_token}