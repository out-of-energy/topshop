from fastapi import APIRouter
from app.api.endpoints import shops

api_router = APIRouter()

api_router.include_router(shops.router, prefix="/shops", tags=["shops"]) 