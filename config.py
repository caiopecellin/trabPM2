from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from os import getenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_USER: str = getenv('DATABASE_USER')
    DATABASE_PASSWORD: str = getenv('DATABASE_PASSWORD')
    DATABASE_HOST: str = getenv('DATABASE_HOST')
    DATABASE_NAME: str = getenv('DATABASE_NAME')
    DATABASE_TYPE: str = getenv('DATABASE_TYPE')
    DATABASE_APP: str = getenv('DATABASE_APP')

    class Config:
        env_file = ".env"

    @property
    def mongo_details(self) -> str:
        return f"mongodb+srv://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_NAME}.{self.DATABASE_HOST}/?retryWrites=true&w=majority&appName={self.DATABASE_APP}"

settings = Settings()

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def get_database() -> AsyncIOMotorClient:
    return db.client

def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.mongo_details)

def close_mongo_connection():
    db.client.close()
