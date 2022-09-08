import fastapi

from app.api.api_v1.endpoints import configurations, templates

api_router = fastapi.APIRouter()
api_router.include_router(configurations.router, prefix='/configurations')
api_router.include_router(templates.router, prefix='/templates')
