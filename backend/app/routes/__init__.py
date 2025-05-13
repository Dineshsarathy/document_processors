from fastapi import APIRouter
from .auth import router as auth_router
from .documents import router as documents_router

# router = APIRouter()
# router.include_router(auth_router)
# router.include_router(documents_router)

router = APIRouter()
router.include_router(auth_router, prefix="/auth")
router.include_router(documents_router)

__all__ = ["router"]