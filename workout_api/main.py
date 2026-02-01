from fastapi import FastAPI
from workout_api.routers import api_router

app = FastAPI(title='workoutApi')

'''
app = FastAPI(
    docs_url="/docs",         # Swagger UI
    redoc_url="/redoc",       # Redoc
    openapi_url="/openapi.json"
)
'''

app.include_router(api_router,prefix='')

#app.include_router(api_router, prefix='/api/v1')
'''
rotas que funcionam:
get atleta
post atleta
get atleta{id}
patch atleta{id}
delete atleta{id}

get categoria
post categoria
get categoria{id}
patch categoria{id}
delete categoria{id}

get centro treinamento-
post centro treinamento-
get centro treinamento{id}-
patch centro treinamento{id}-
delete centro treinamento{id}-

'''