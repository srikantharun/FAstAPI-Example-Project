from fastapi import APIRouter

from app.api.endpoints import items, users, login, categories

# Main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])