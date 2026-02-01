from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL: str = Field(default='postgresql+asyncpg://postgres:davi9090@localhost/workout',
                        description='URL de conecçao como o banco de dados')

    class Config:
        env_file = '.env'

settings = Settings()
