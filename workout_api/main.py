from fastapi import FastAPI
from workout_api.routers import api_router

app = FastAPI(
    title='workoutAPI',
    docs_url="/docs",         # Define a URL para acessar a documentação interativa Swagger UI.
    redoc_url="/redoc",       # Define a URL para acessar a documentação alternativa Redoc.
    openapi_url="/openapi.json"  # Define a URL para acessar o schema OpenAPI em formato JSON.
)

# Inclui todas as rotas definidas no api_router.
# O prefix='' significa que as rotas serão registradas diretamente na raiz (sem prefixo adicional).
app.include_router(api_router, prefix='')
