import asyncio
# from asyncio import WindowsSelectorEventLoopPolicy
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
load_dotenv()

#DATABASE
class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    SECRET_KEY_TOKEN: str
    ALGORITHM: str
    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file="../.env")

settings = Settings()
SECRET_KEY_TOKEN = settings.SECRET_KEY_TOKEN
ALGORITHM = settings.ALGORITHM
EXPIRE_ACCESS_TOKEN = 60  # min

#db users for roles
medic = "medic"
dispatcher = "dispatcher"