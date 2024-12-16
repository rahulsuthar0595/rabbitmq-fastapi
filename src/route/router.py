from fastapi import APIRouter
from src.api.v1.views import order
router = APIRouter(prefix="/api/v1")

router.include_router(order.router, tags=["Order API"])
