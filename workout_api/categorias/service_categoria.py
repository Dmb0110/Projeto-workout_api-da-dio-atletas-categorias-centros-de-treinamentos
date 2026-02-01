from uuid import uuid4
from pydantic import UUID4
from sqlalchemy import select
from fastapi import HTTPException, status

from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut, CategoriaUpdate
from workout_api.contrib.repository.dependencies import DatabaseDependency

class CategoriaService:
    # Camada de serviço responsável pela lógica de negócio do recurso Categoria.
    # Contém métodos estáticos para criar, listar, consultar, atualizar e deletar categorias.

    @staticmethod
    async def criar_categoria(
        db_session: DatabaseDependency,
        categoria_in: CategoriaIn
    ) -> CategoriaOut:
        # Criação de uma nova categoria:
        # 1. Constrói objeto de saída CategoriaOut com UUID.
        # 2. Cria modelo ORM CategoriaModel a partir dos dados.
        # 3. Persiste no banco e retorna a categoria criada.
        # Em caso de erro, lança HTTPException 500.
        try:
            categoria_out = CategoriaOut(
                id=uuid4(),
                **categoria_in.model_dump()
            )
            categoria_model = CategoriaModel(**categoria_out.model_dump())

            db_session.add(categoria_model)
            await db_session.commit()

            return categoria_out

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao criar categoria: {str(e)}"
            )
        

    @staticmethod
    async def listar_categorias(db_session: DatabaseDependency) -> list[CategoriaOut]:
        # Listagem de todas as categorias:
        # Executa SELECT na tabela de categorias.
        # Retorna lista de CategoriaOut validados a partir dos modelos ORM.
        result = await db_session.execute(select(CategoriaModel))
        categorias = result.scalars().all()
        return [CategoriaOut.model_validate(categoria) for categoria in categorias]


    @staticmethod
    async def buscar_por_id(
        id: UUID4, 
        db_session: DatabaseDependency
    ) -> CategoriaOut:
        # Consulta de uma categoria específica:
        # Busca pelo UUID informado.
        # Se não encontrar, lança HTTPException 404.
        # Retorna a categoria encontrada validada contra o schema de saída.
        categoria = (
            await db_session.execute(select(CategoriaModel).filter_by(id=id))
        ).scalars().first()

        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoria não encontrada no id: {id}"
            )

        return CategoriaOut.model_validate(categoria)


    @staticmethod
    async def trocar_categoria(
        id: UUID4, 
        db_session: DatabaseDependency,
        categoria_up: CategoriaUpdate
    ) -> CategoriaOut:
        # Atualização parcial de categoria:
        # 1. Busca categoria pelo id.
        # 2. Se não encontrar, lança HTTPException 404.
        # 3. Aplica atualização apenas nos campos enviados (PATCH).
        # 4. Comita e atualiza objeto em memória.
        # 5. Retorna categoria atualizada como CategoriaOut.
        categoria = (
            await db_session.execute(select(CategoriaModel).filter_by(id=id))
        ).scalars().first()

        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoria não encontrada no id: {id}"
            )
        
        categoria_update = categoria_up.model_dump(exclude_unset=True)
        for key, value in categoria_update.items():
            setattr(categoria, key, value)

        await db_session.commit()
        await db_session.refresh(categoria)

        return CategoriaOut.model_validate(categoria)


    @staticmethod
    async def deletar_categoria(
        id: UUID4, 
        db_session: DatabaseDependency
    ) -> None:
        # Exclusão de categoria:
        # 1. Busca categoria pelo id.
        # 2. Se não encontrar, lança HTTPException 404.
        # 3. Remove registro do banco e comita.
        # Não retorna nada → rota responde com status 204 (No Content).
        categoria: CategoriaModel = (
            await db_session.execute(select(CategoriaModel).filter_by(id=id))
        ).scalars().first()

        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoria não encontrada no id: {id}"
            )

        await db_session.delete(categoria)
        await db_session.commit()
