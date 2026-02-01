from datetime import datetime, timezone
from uuid import uuid4
from pydantic import UUID4
from fastapi import HTTPException, status
from sqlalchemy.future import select

from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.atleta.models import AtletaModel
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.repository.dependencies import DatabaseDependency

class AtletaService:
    
    @staticmethod
    async def criar_atleta(
            db_session: DatabaseDependency, 
            atleta_in: AtletaIn
            ) -> AtletaOut:
        # valida categoria
        categoria = (
            await db_session.execute(
                select(CategoriaModel).filter_by(nome=atleta_in.categoria.nome)
            )
        ).scalars().first()
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"A categoria {atleta_in.categoria.nome} não foi encontrada."
            )

        # valida centro de treinamento
        centro_treinamento = (
            await db_session.execute(
                select(CentroTreinamentoModel).filter_by(nome=atleta_in.centro_treinamento.nome)
            )
        ).scalars().first()
        if not centro_treinamento:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"O centro de treinamento {atleta_in.centro_treinamento.nome} não foi encontrado."
            )

        try:
            atleta_out = AtletaOut(
                id=uuid4(),
                created_at=datetime.now(timezone.utc),  # usar timezone-aware
                **atleta_in.model_dump()
            )
            atleta_model = AtletaModel(
                **atleta_out.model_dump(exclude={"categoria", "centro_treinamento"})
            )
            atleta_model.categoria_id = categoria.pk_id
            atleta_model.centro_treinamento_id = centro_treinamento.pk_id

            db_session.add(atleta_model)
            await db_session.commit()
            return atleta_out

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ocorreu um erro ao inserir os dados no banco: {str(e)}"
            )


    @staticmethod
    async def listar_atletas(db_session: DatabaseDependency) -> list[AtletaModel]:
        atletas = (
            await db_session.execute(select(AtletaModel))
            ).scalars().all() 

        return [AtletaOut.model_validate(atleta) for atleta in atletas]
    

    @staticmethod
    async def atleta_especifico(
            id: UUID4,
            db_session: DatabaseDependency
            ) -> AtletaModel:
         
        atleta: AtletaOut = (
            await db_session.execute(select(AtletaModel).filter_by(id=id))
            ).scalars().first()

        if not atleta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Atleta nao encontrado no id: {id}'
                )
    
        return atleta
    

    @staticmethod
    async def atualizar_atleta(
        id: UUID4,
        db_session: DatabaseDependency,
        atleta_up: AtletaUpdate
    ) -> AtletaOut:
        # busca atleta
        atleta: AtletaModel = (
            await db_session.execute(select(AtletaModel).filter_by(id=id))
        ).scalars().first()

        if not atleta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Atleta não encontrado no id: {id}"
            )

        # aplica atualização parcial
        atleta_update = atleta_up.model_dump(exclude_unset=True)
        for key, value in atleta_update.items():
            setattr(atleta, key, value)

        await db_session.commit()
        await db_session.refresh(atleta)

        return AtletaOut.model_validate(atleta)


    @staticmethod
    async def deletar_atleta(
        id: UUID4, 
        db_session: DatabaseDependency
        )-> None:
        
        atleta: AtletaModel = (
            await db_session.execute(select(AtletaModel).filter_by(id=id))
        ).scalars().first()

        if not atleta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Atleta não encontrado no id: {id}"
            )

        await db_session.delete(atleta)
        await db_session.commit()
        # não retorna nada → rota 204
