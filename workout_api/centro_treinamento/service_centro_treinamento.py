from uuid import uuid4
from fastapi import HTTPException, status
from sqlalchemy.future import select
from pydantic import UUID4

from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import (
    CentroTreinamentoIn,
    CentroTreinamentoOut,
    CentroTreinamentoUpdate,
)
from workout_api.contrib.repository.dependencies import DatabaseDependency

class CentroTreinamentoService:
    # Camada de serviço responsável pela lógica de negócio do recurso Centro de Treinamento.
    # Contém métodos estáticos para criar, listar, consultar, atualizar e deletar centros.

    @staticmethod
    async def criar(
        db_session: DatabaseDependency, 
        ct_in: CentroTreinamentoIn
    ) -> CentroTreinamentoOut:
        # Criação de um novo centro de treinamento:
        # 1. Constrói objeto de saída CentroTreinamentoOut com UUID.
        # 2. Cria modelo ORM CentroTreinamentoModel a partir dos dados.
        # 3. Persiste no banco e retorna o centro criado.
        ct_out = CentroTreinamentoOut(id=uuid4(), **ct_in.model_dump())
        ct_model = CentroTreinamentoModel(**ct_out.model_dump())

        db_session.add(ct_model)
        await db_session.commit()
        return ct_out


    @staticmethod
    async def listar_todos(db_session: DatabaseDependency) -> list[CentroTreinamentoOut]:
        # Listagem de todos os centros de treinamento:
        # Executa SELECT na tabela de centros.
        # Retorna lista de CentroTreinamentoOut validados a partir dos modelos ORM.
        result = await db_session.execute(select(CentroTreinamentoModel))
        centros = result.scalars().all()
        return [CentroTreinamentoOut.model_validate(ct) for ct in centros]


    @staticmethod
    async def buscar_por_id(
        id: UUID4, 
        db_session: DatabaseDependency
    ) -> CentroTreinamentoOut:
        # Consulta de um centro de treinamento específico:
        # Busca pelo UUID informado.
        # Se não encontrar, lança HTTPException 404.
        # Retorna o centro encontrado validado contra o schema de saída.
        ct = (
            await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
        ).scalars().first()

        if not ct:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Centro de Treinamento não encontrado no id: {id}"
            )

        return CentroTreinamentoOut.model_validate(ct)


    @staticmethod
    async def atualizar(
        id: UUID4, 
        db_session: DatabaseDependency, 
        ct_up: CentroTreinamentoUpdate
    ) -> CentroTreinamentoOut:
        # Atualização parcial de centro de treinamento:
        # 1. Busca centro pelo id.
        # 2. Se não encontrar, lança HTTPException 404.
        # 3. Aplica atualização apenas nos campos enviados (PATCH).
        # 4. Comita e atualiza objeto em memória.
        # 5. Retorna centro atualizado como CentroTreinamentoOut.
        ct: CentroTreinamentoModel = (
            await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
        ).scalars().first()

        if not ct:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Centro de Treinamento não encontrado no id: {id}"
            )

        ct_update = ct_up.model_dump(exclude_unset=True)
        for key, value in ct_update.items():
            setattr(ct, key, value)

        await db_session.commit()
        await db_session.refresh(ct)

        return CentroTreinamentoOut.model_validate(ct)


    @staticmethod
    async def deletar(
        id: UUID4, 
        db_session: DatabaseDependency
    ) -> None:
        # Exclusão de centro de treinamento:
        # 1. Busca centro pelo id.
        # 2. Se não encontrar, lança HTTPException 404.
        # 3. Remove registro do banco e comita.
        # Não retorna nada → rota responde com status 204 (No Content).
        ct: CentroTreinamentoModel = (
            await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
        ).scalars().first()

        if not ct:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Centro de Treinamento não encontrado no id: {id}"
            )

        await db_session.delete(ct)
        await db_session.commit()
