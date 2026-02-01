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

    @staticmethod
    async def criar(
        db_session: DatabaseDependency, 
        ct_in: CentroTreinamentoIn
        ) -> CentroTreinamentoOut:

        ct_out = CentroTreinamentoOut(id=uuid4(), **ct_in.model_dump())
        ct_model = CentroTreinamentoModel(**ct_out.model_dump())

        db_session.add(ct_model)
        await db_session.commit()
        return ct_out

    @staticmethod
    async def listar_todos(db_session: DatabaseDependency) -> list[CentroTreinamentoOut]:
        result = await db_session.execute(select(CentroTreinamentoModel))
        centros = result.scalars().all()
        return [CentroTreinamentoOut.model_validate(ct) for ct in centros]

    @staticmethod
    async def buscar_por_id(
        id: UUID4, 
        db_session: DatabaseDependency
        ) -> CentroTreinamentoOut:

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
        # não retorna nada → rota 204
