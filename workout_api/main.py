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



