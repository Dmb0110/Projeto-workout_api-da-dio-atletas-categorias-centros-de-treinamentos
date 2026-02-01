from fastapi import APIRouter
from workout_api.atleta.controller import router as atleta
from workout_api.categorias.controller import router as categorias
from workout_api.centro_treinamento.controller import router as centro_treinamento

api_router = APIRouter()
# Cria um roteador principal que vai agrupar todos os módulos da aplicação.

api_router.include_router(atleta, prefix='/atleta', tags=['atleta'])
# Inclui todas as rotas do módulo de atleta.
# prefix='/atleta' → todas as rotas começam com /atleta.
# tags=['atleta'] → organiza a documentação (Swagger/Redoc) sob a tag "atleta".

api_router.include_router(categorias, prefix='/categoria', tags=['categoria'])
# Inclui todas as rotas do módulo de categoria.
# prefix='/categoria' → todas as rotas começam com /categoria.
# tags=['categoria'] → organiza a documentação sob a tag "categoria".

api_router.include_router(centro_treinamento, prefix='/centro_treinamento', tags=['centro_treinamento'])
# Inclui todas as rotas do módulo de centro de treinamento.
# prefix='/centro_treinamento' → todas as rotas começam com /centro_treinamento.
# tags=['centro_treinamento'] → organiza a documentação sob a tag "centro_treinamento".
