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
    # Camada de serviço responsável pela lógica de negócio do recurso Atleta.
    # Contém métodos estáticos para criar, listar, consultar, atualizar e deletar atletas.
    
    @staticmethod
    async def criar_atleta(
            db_session: DatabaseDependency, 
            atleta_in: AtletaIn
            ) -> AtletaOut:
        # Criação de um novo atleta:
        # 1. Valida se a categoria informada existe no banco.
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

        # 2. Valida se o centro de treinamento informado existe no banco.
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

        # 3. Cria objeto de saída AtletaOut com id e data de criação.
        try:
            atleta_out = AtletaOut(
                id=uuid4(),
                created_at=datetime.now(timezone.utc),  # timezone-aware
                **atleta_in.model_dump()
            )
            # 4. Constrói modelo ORM AtletaModel e associa chaves estrangeiras.
            atleta_model = AtletaModel(
                **atleta_out.model_dump(exclude={"categoria", "centro_treinamento"})
            )
            atleta_model.categoria_id = categoria.pk_id
            atleta_model.centro_treinamento_id = centro_treinamento.pk_id

            # 5. Persiste no banco e retorna o atleta criado.
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
        # Listagem de todos os atletas:
        # Executa SELECT na tabela de atletas.
        atletas = (
            await db_session.execute(select(AtletaModel))
        ).scalars().all() 

        # Retorna lista de AtletaOut validados a partir dos modelos ORM.
        return [AtletaOut.model_validate(atleta) for atleta in atletas]
    

    @staticmethod
    async def atleta_especifico(
            id: UUID4,
            db_session: DatabaseDependency
            ) -> AtletaModel:
        # Consulta de um atleta específico:
        # Busca pelo UUID informado.
        atleta: AtletaOut = (
            await db_session.execute(select(AtletaModel).filter_by(id=id))
        ).scalars().first()

        # Se não encontrar, lança HTTPException 404.
        if not atleta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Atleta nao encontrado no id: {id}'
            )
    
        # Retorna o atleta encontrado.
        return atleta
    

    @staticmethod
    async def atualizar_atleta(
        id: UUID4,
        db_session: DatabaseDependency,
        atleta_up: AtletaUpdate
    ) -> AtletaOut:
        # Atualização parcial de atleta:
        # 1. Busca atleta pelo id.
        atleta: AtletaModel = (
            await db_session.execute(select(AtletaModel).filter_by(id=id))
        ).scalars().first()

        # 2. Se não encontrar, lança HTTPException 404.
        if not atleta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Atleta não encontrado no id: {id}"
            )

        # 3. Aplica atualização apenas nos campos enviados (PATCH).
        atleta_update = atleta_up.model_dump(exclude_unset=True)
        for key, value in atleta_update.items():
            setattr(atleta, key, value)

        # 4. Comita e atualiza objeto em memória.
        await db_session.commit()
        await db_session.refresh(atleta)

        # 5. Retorna atleta atualizado como AtletaOut.
        return AtletaOut.model_validate(atleta)


    @staticmethod
    async def deletar_atleta(
        id: UUID4, 
        db_session: DatabaseDependency
        )-> None:
        # Exclusão de atleta:
        # 1. Busca atleta pelo id.
        atleta: AtletaModel = (
            await db_session.execute(select(AtletaModel).filter_by(id=id))
        ).scalars().first()

        # 2. Se não encontrar, lança HTTPException 404.
        if not atleta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Atleta não encontrado no id: {id}"
            )

        # 3. Remove registro do banco e comita.
        await db_session.delete(atleta)
        await db_session.commit()
        # Não retorna nada → rota responde com status 204 (No Content).
