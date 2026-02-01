from uuid import uuid4
from pydantic import UUID4
from typing import List
from sqlalchemy import select
from fastapi import APIRouter, Body, status
from workout_api.categorias.schemas import CategoriaIn,CategoriaOut,CategoriaUpdate
from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.service_categoria import CategoriaService

from workout_api.contrib.repository.dependencies import DatabaseDependency

router = APIRouter()

@router.post(
        '/',
        summary='Criar uma nova Categoria',
        status_code=status.HTTP_201_CREATED,
        response_model=CategoriaOut,
)
async def criar(
    db_session: DatabaseDependency,
    categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:
    
    return await CategoriaService.criar_categoria(db_session, categoria_in)
    '''
    categoria_out = CategoriaOut(id=uuid4(),**categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())
    
    db_session.add(categoria_model)
    await db_session.commit()

    return categoria_out
    '''

@router.get(
    '/',
    summary='Consultar todas as categorias',
    status_code=status.HTTP_200_OK,
    response_model=list[CategoriaOut],
)
async def listar(db_session: DatabaseDependency) -> List[CategoriaOut]:
    return await CategoriaService.listar_categorias(db_session)
    '''
    categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))
).scalars().all()

    return categorias
    '''

@router.get(
    '/{id}',
    summary='Consultar uma Categoria pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def mostrar_um(
    id: UUID4,
    db_session: DatabaseDependency
) -> CategoriaOut:
    return await CategoriaService.buscar_por_id(id, db_session)
    
    '''
    categoria: CategoriaOut = (await db_session.execute(select(CategoriaModel).filter_by(id=id))
).scalars().first()
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Categoria nao encontrada nao id: {id}'
        )
    
    return categoria
'''

@router.patch(
    '/{id}',
    summary='Editar um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut,
)
async def trocar_um(
    id: UUID4, 
    db_session: DatabaseDependency, 
    categoria_up: CategoriaUpdate = Body(...)
) -> CategoriaOut:
    return await CategoriaService.trocar_categoria(id, db_session, categoria_up)
    
    '''
    categoria: CategoriaModel = (await db_session.execute(select(CategoriaModel).filter_by(id=id))
).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Categoria não encontrada no id: {id}'
        )
    
    categoria_update = categoria_up.model_dump(exclude_unset=True)
    for key, value in categoria_update.items():
        setattr(categoria, key, value)

    await db_session.commit()
    await db_session.refresh(categoria)

    return categoria
'''

@router.delete(
    '/{id}', 
    summary='Deletar um Categoria pelo id',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
    id: UUID4, 
    db_session: DatabaseDependency
) -> None:
    await CategoriaService.deletar_categoria(id, db_session)
    '''
    categoria: CategoriaModel = (await db_session.execute(select(CategoriaModel).filter_by(id=id))
).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Categoria não encontrada no id: {id}'
        )
    
    await db_session.delete(categoria)
    await db_session.commit()

    return {'mensagem':'categoria deletada com sucesso'}
'''
