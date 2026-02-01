from typing import Annotated
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from workout_api.configs.database import get_session

DatabaseDependency = Annotated[AsyncSession, Depends(get_session)]
# Define uma dependência para injeção de sessão de banco de dados no FastAPI.
# - Annotated → usado para adicionar metadados ao tipo AsyncSession.
# - AsyncSession → tipo de sessão assíncrona do SQLAlchemy.
# - Depends(get_session) → indica que a sessão será obtida pela função get_session.
# Essa dependência é utilizada nos controllers e services para acessar o banco de forma segura e controlada.
