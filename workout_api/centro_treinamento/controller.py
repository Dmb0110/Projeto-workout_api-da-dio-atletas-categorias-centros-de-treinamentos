from uuid import uuid4
from pydantic import UUID4
from fastapi import APIRouter, Body, HTTPException, status

from workout_api.centro_treinamento.schemas import CentroTreinamentoIn,CentroTreinamentoOut,CentroTreinamentoUpdate
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.service_centro_treinamento import CentroTreinamentoService
from workout_api.contrib.repository.dependencies import DatabaseDependency
from sqlalchemy.future import select

router = APIRouter()

@router.post(
        '/',
        summary='Criar um novo Centro de Treinamento',
        status_code=status.HTTP_201_CREATED,
        response_model=CentroTreinamentoOut,
)
async def post(
    db_session: DatabaseDependency,
    ct_in: CentroTreinamentoIn = Body(...)
) -> CentroTreinamentoOut:
    # Rota POST /
    # Cria um novo centro de treinamento no banco de dados a partir dos dados enviados no corpo da requisição.
    # Retorna o centro criado com status 201 (Created).
    return await CentroTreinamentoService.criar(db_session, ct_in)


@router.get(
    '/',
    summary='Consultar todos os centros de treinamento',
    status_code=status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOut],
)
async def query(db_session: DatabaseDependency) -> list[CentroTreinamentoOut]:
    # Rota GET /
    # Consulta todos os centros de treinamento cadastrados no banco de dados.
    # Retorna uma lista de centros com status 200 (OK).
    return await CentroTreinamentoService.listar_todos(db_session)


@router.get(
    '/{id}',
    summary='Consultar um Centro de Treinamento pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def query(
    id: UUID4, 
    db_session: DatabaseDependency
) -> CentroTreinamentoOut:
    # Rota GET /{id}
    # Consulta um centro de treinamento específico pelo seu UUID.
    # Retorna os dados do centro encontrado com status 200 (OK).
    return await CentroTreinamentoService.buscar_por_id(id, db_session)


@router.patch(
    '/{id}',
    summary='Editar um Centro de Treinamento pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def patch(
    id: UUID4, 
    db_session: DatabaseDependency, 
    ct_up: CentroTreinamentoUpdate = Body(...)
) -> CentroTreinamentoOut:
    # Rota PATCH /{id}
    # Atualiza parcialmente os dados de um centro de treinamento existente, identificado pelo UUID.
    # Retorna o centro atualizado com status 200 (OK).
    return await CentroTreinamentoService.atualizar(id, db_session, ct_up)


@router.delete(
    '/{id}', 
    summary='Deletar um Centro de Treinamento pelo id',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
    id: UUID4, 
    db_session: DatabaseDependency
) -> None:
    # Rota DELETE /{id}
    # Remove um centro de treinamento do banco de dados pelo seu UUID.
    # Não retorna corpo de resposta, apenas status 204 (No Content).
    await CentroTreinamentoService.deletar(id, db_session)
