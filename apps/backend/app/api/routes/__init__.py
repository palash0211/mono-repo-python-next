from fastapi import APIRouter
from app.schemas.response import APIResponse

from app.api.routes import items, users, auth

api_router = APIRouter()

@api_router.get("/", response_model=APIResponse)
def read_root():
    """Root endpoint"""
    return APIResponse(
        success=True,
        message="Welcome to the API",
        data={"version": "1.0.0"}
    )

# Include all sub-routers
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])

