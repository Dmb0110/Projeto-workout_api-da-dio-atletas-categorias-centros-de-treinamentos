from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from workout_api.configs.settings import settings

engine = create_async_engine(settings.DB_URL, echo=False)
# Cria o engine assíncrono do SQLAlchemy.
# Usa a URL do banco definida em settings.DB_URL.
# echo=False desativa o log detalhado das queries.

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
# Cria uma fábrica de sessões assíncronas.
# - class_=AsyncSession → define que as sessões serão assíncronas.
# - expire_on_commit=False → mantém os objetos disponíveis após commit.

async def get_session() -> AsyncGenerator:
    # Função usada como dependência no FastAPI.
    # Cria uma sessão assíncrona de banco de dados.
    # Garante que a sessão seja aberta e fechada corretamente com "async with".
    async with async_session() as session:
        yield session
