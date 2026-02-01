from uuid import uuid4
from pydantic import UUID4
from sqlalchemy import select
from fastapi import HTTPException, status
from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut, CategoriaUpdate
from workout_api.contrib.repository.dependencies import DatabaseDependency

class CategoriaService:

    @staticmethod
    async def criar_categoria(
        db_session: DatabaseDependency,
        categoria_in: CategoriaIn
    ) -> CategoriaOut:
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
        """
        Consulta todas as categorias no banco e retorna como lista de CategoriaOut.
        """
        result = await db_session.execute(select(CategoriaModel))
        categorias = result.scalars().all()
        # valida cada objeto do ORM contra o schema de saída
        return [CategoriaOut.model_validate(categoria) for categoria in categorias]


    @staticmethod
    async def buscar_por_id(
        id: UUID4, 
        db_session: DatabaseDependency
        ) -> CategoriaOut:
        """
        Consulta uma categoria pelo id.
        """
        categoria = (
            await db_session.execute(select(CategoriaModel).filter_by(id=id))
        ).scalars().first()

        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Categoria não encontrada no id: {id}"
            )

        # valida o objeto ORM contra o schema de saída
        return CategoriaOut.model_validate(categoria)


    @staticmethod
    async def trocar_categoria(
        id: UUID4, 
        db_session: DatabaseDependency,
        categoria_up: CategoriaUpdate
        ) -> CategoriaOut:
        """
        Atualizar parcialmente uma categoria pelo id.
        """
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

        #return categoria

        # valida o objeto ORM contra o schema de saída
        return CategoriaOut.model_validate(categoria)


    @staticmethod
    async def deletar_categoria(
        id: UUID4, 
        db_session: DatabaseDependency
    ) -> None:
        
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
        # não retorna nada → rota 204
