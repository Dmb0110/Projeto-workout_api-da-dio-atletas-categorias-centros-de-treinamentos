from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, status,HTTPException
from pydantic import UUID4

from workout_api.atleta.schemas import AtletaIn,AtletaOut,AtletaUpdate
from workout_api.atleta.models import AtletaModel
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel

from workout_api.contrib.repository.dependencies import DatabaseDependency
from workout_api.atleta.service_atleta import AtletaService
from sqlalchemy.future import select

router = APIRouter()

@router.post(
    '/',
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(
    db_session: DatabaseDependency,
    atleta_in: AtletaIn = Body(...)
):
    return await AtletaService.criar_atleta(db_session, atleta_in)
    

@router.get(
    '/',
    summary='Consultar todos os atletas',
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaOut],
)
async def query(db_session: DatabaseDependency) -> list[AtletaOut]:
    return await AtletaService.listar_atletas(db_session)
 

@router.get(
    '/{id}',
    summary='Consultar um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get(
    id: UUID4,
    db_session: DatabaseDependency
):
    return await AtletaService.atleta_especifico(id, db_session)


@router.patch(
    '/{id}',
    summary='Editar um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def patch(
    id: UUID4, 
    db_session: DatabaseDependency,
    atleta_up: AtletaUpdate = Body(...)
) -> AtletaOut:
    return await AtletaService.atualizar_atleta(id, db_session,atleta_up)
 

@router.delete(
    '/{id}', 
    summary='Deletar um Atleta pelo id',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
    id: UUID4, 
    db_session: DatabaseDependency
) -> None:
    await AtletaService.deletar_atleta(id, db_session)
