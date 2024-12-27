from fastapi import APIRouter
from src.api.v1.views import user
router = APIRouter(prefix="/api/v1")

router.include_router(user.router, tags=["User API"])
